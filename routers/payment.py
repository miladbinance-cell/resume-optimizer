import stripe
import uuid
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import (
    STRIPE_SECRET_KEY,
    STRIPE_PUBLISHABLE_KEY,
    PRICE_RESUME_OPTIMIZE,
    PRICE_PREMIUM,
    PRICE_RESUME_OPTIMIZE_CENTS,
    PRICE_PREMIUM_CENTS,
    NOWPAYMENTS_API_KEY,
    BASE_URL,
)
from services.nowpayments import create_invoice

stripe.api_key = STRIPE_SECRET_KEY
templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/payment", tags=["payment"])


def _has_stripe() -> bool:
    return bool(STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY and "placeholder" not in STRIPE_SECRET_KEY)


def _has_crypto() -> bool:
    return bool(NOWPAYMENTS_API_KEY and "placeholder" not in NOWPAYMENTS_API_KEY)


@router.get("/checkout/{file_id}")
async def checkout_page(request: Request, file_id: str):
    """Show checkout page with plan selection and payment methods"""
    return templates.TemplateResponse(
        "checkout.html",
        {
            "request": request,
            "file_id": file_id,
            "stripe_ready": _has_stripe(),
            "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
            "crypto_ready": _has_crypto(),
            "price_basic": PRICE_RESUME_OPTIMIZE,
            "price_premium": PRICE_PREMIUM,
        },
    )


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: Request,
    file_id: str = Form(...),
    plan: str = Form("basic"),
    method: str = Form("stripe"),
    email: str = Form(""),
):
    """
    Create payment session — supports Stripe and NowPayments (crypto).
    """
    price = PRICE_RESUME_OPTIMIZE if plan == "basic" else PRICE_PREMIUM
    price_cents = PRICE_RESUME_OPTIMIZE_CENTS if plan == "basic" else PRICE_PREMIUM_CENTS
    plan_name = "ATS-Optimized Resume" if plan == "basic" else "Resume + Cover Letter + LinkedIn"

    # Save email to session
    sessions = getattr(request.app.state, "sessions", {})
    if file_id in sessions and email:
        sessions[file_id]["email"] = email

    # ── CRYPTO (NowPayments) ──
    if method == "crypto":
        try:
            invoice = create_invoice(
                amount=price,
                order_id=file_id,
                order_description=plan_name,
            )
            invoice_url = invoice.get("invoice_url", "")
            return RedirectResponse(url=invoice_url, status_code=303)
        except Exception as e:
            return templates.TemplateResponse(
                "checkout.html",
                {
                    "request": request,
                    "file_id": file_id,
                    "error": f"Crypto payment error: {str(e)}",
                    "stripe_ready": _has_stripe(),
                    "crypto_ready": _has_crypto(),
                    "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
                    "price_basic": PRICE_RESUME_OPTIMIZE,
                    "price_premium": PRICE_PREMIUM,
                },
            )

    # ── STRIPE ──
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": plan_name,
                            "description": "AI-powered resume optimization service",
                        },
                        "unit_amount": price_cents,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{BASE_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}&file_id={file_id}&plan={plan}&method=stripe",
            cancel_url=f"{BASE_URL}/payment/cancel?file_id={file_id}",
            metadata={"file_id": file_id, "plan": plan},
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return templates.TemplateResponse(
            "checkout.html",
            {
                "request": request,
                "file_id": file_id,
                "error": f"Payment error: {str(e)}",
                "stripe_ready": _has_stripe(),
                "crypto_ready": _has_crypto(),
                "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
                "price_basic": PRICE_RESUME_OPTIMIZE,
                "price_premium": PRICE_PREMIUM,
            },
        )


@router.get("/success", response_class=HTMLResponse)
async def payment_success(
    request: Request,
    session_id: str = "",
    file_id: str = "",
    plan: str = "basic",
    method: str = "stripe",
):
    """Payment success page"""
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "file_id": file_id,
            "plan": plan,
            "session_id": session_id,
            "method": method,
        },
    )


@router.get("/cancel", response_class=HTMLResponse)
async def payment_cancel(request: Request, file_id: str = ""):
    """Payment cancelled page"""
    return templates.TemplateResponse(
        "cancel.html",
        {"request": request, "file_id": file_id},
    )