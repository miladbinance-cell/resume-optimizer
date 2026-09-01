import json
import stripe
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from config import STRIPE_WEBHOOK_SECRET, STRIPE_SECRET_KEY
from services.ai_optimizer import optimize_resume, generate_cover_letter
from services.doc_generator import generate_docx, generate_pdf
from services.email_service import send_results_email
from services.nowpayments import verify_ipn_signature

stripe.api_key = STRIPE_SECRET_KEY
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


# ──────────────────────────────────────────────────────
# Stripe Webhook
# ──────────────────────────────────────────────────────
@router.post("/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return JSONResponse({"error": "Invalid signature"}, status_code=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_stripe_payment(session, request)

    return JSONResponse({"status": "ok"})


# ──────────────────────────────────────────────────────
# NowPayments IPN Webhook (Crypto)
# ──────────────────────────────────────────────────────
@router.post("/nowpayments")
async def nowpayments_webhook(request: Request):
    """
    Handle NowPayments IPN (Instant Payment Notification) callback.
    Docs: https://documenter.getpostman.com/view/7907941/S1a32n38#71c58a0b-9305-4ab9-be31-eea796e9e5e0
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    # Verify signature
    signature = request.headers.get("x-nowpayments-sig", "")
    if not verify_ipn_signature(data, signature):
        return JSONResponse({"error": "Invalid signature"}, status_code=400)

    payment_status = data.get("payment_status", "")
    order_id = data.get("order_id", "")

    # Only process completed payments
    if payment_status in ("finished", "confirmed", "complete"):
        await handle_crypto_payment(data, order_id, request)

    return JSONResponse({"status": "ok"})


# ──────────────────────────────────────────────────────
# Shared payment processing
# ──────────────────────────────────────────────────────
async def handle_stripe_payment(session: dict, request: Request):
    """Process Stripe payment: optimize resume, generate docs, send email"""
    file_id = session.get("metadata", {}).get("file_id", "")
    plan = session.get("metadata", {}).get("plan", "basic")
    customer_email = session.get("customer_details", {}).get("email", "")
    await _process_order(file_id, plan, customer_email, request)


async def handle_crypto_payment(data: dict, order_id: str, request: Request):
    """Process crypto payment: optimize resume, generate docs, send email"""
    file_id = order_id
    # Get email from session (passed during checkout)
    sessions = getattr(request.app.state, "sessions", {})
    session_data = sessions.get(file_id, {})
    customer_email = session_data.get("email", "")
    # Determine plan from price
    price_paid = float(data.get("price_amount", 0))
    plan = "premium" if price_paid >= 39 else "basic"
    await _process_order(file_id, plan, customer_email, request)


async def _process_order(
    file_id: str,
    plan: str,
    customer_email: str,
    request: Request,
):
    """Core processing: AI optimization, doc generation, email delivery"""
    if not file_id:
        return

    sessions = getattr(request.app.state, "sessions", {})
    session_data = sessions.get(file_id, {})

    if not session_data:
        return

    resume_text = session_data.get("resume_text", "")
    job_title = session_data.get("job_title", "")
    company = session_data.get("company", "")
    job_description = session_data.get("job_description", "")

    # AI processing
    results = {}

    optimized = await optimize_resume(resume_text, job_description, job_title, company)
    results["optimized_resume"] = optimized

    if plan == "premium":
        cover_letter = await generate_cover_letter(
            resume_text, job_description, job_title, company
        )
        results["cover_letter"] = cover_letter

    # Generate documents
    docx_path = generate_docx(results, file_id)
    pdf_path = generate_pdf(results, file_id)

    # Store results
    session_data["results"] = results
    session_data["docx_path"] = docx_path
    session_data["pdf_path"] = pdf_path
    session_data["paid"] = True
    session_data["email"] = customer_email

    # Send email
    if customer_email:
        from config import BASE_URL
        download_url = f"{BASE_URL}/results/{file_id}"
        await send_results_email(customer_email, download_url, file_id, plan)