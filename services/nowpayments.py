"""
NowPayments Crypto Payment Service
https://nowpayments.io — API documentation: https://documenter.getpostman.com/view/7907941/S1a32n38
"""
import hashlib
import hmac
import json
import requests
from config import NOWPAYMENTS_API_KEY, NOWPAYMENTS_IPN_SECRET, BASE_URL


def create_invoice(
    amount: float,
    order_id: str,
    order_description: str = "ResumeAI Optimization",
    currency: str = None,
) -> dict:
    """
    Create a NowPayments invoice for crypto payment.
    Returns the invoice data including payment URL.
    """
    if currency is None:
        import os
        currency = os.getenv("NOWPAYMENTS_CURRENCY", "usdttrc20")
    url = "https://api.nowpayments.io/v1/invoice"
    payload = {
        "price_amount": amount,
        "price_currency": "usd",
        "pay_currency": currency,
        "order_id": order_id,
        "order_description": order_description,
        "ipn_callback_url": f"{BASE_URL}/webhooks/nowpayments",
        "success_url": f"{BASE_URL}/payment/success?file_id={order_id}&method=crypto",
        "cancel_url": f"{BASE_URL}/payment/cancel?file_id={order_id}",
    }
    headers = {
        "x-api-key": NOWPAYMENTS_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def get_payment_status(payment_id: str) -> dict:
    """Check payment status by payment_id"""
    url = f"https://api.nowpayments.io/v1/payment/{payment_id}"
    headers = {"x-api-key": NOWPAYMENTS_API_KEY}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def verify_ipn_signature(data: dict, received_signature: str) -> bool:
    """
    Verify IPN callback signature from NowPayments.
    Uses HMAC-SHA512 with the IPN secret key.
    In development mode with localhost, skips verification for testing.
    """
    from config import BASE_URL
    # In local dev mode, skip signature verification
    if "localhost" in BASE_URL or "127.0.0.1" in BASE_URL:
        return True
    if not NOWPAYMENTS_IPN_SECRET:
        return True

    # Sort the data by key and convert to JSON
    sorted_data = json.dumps(data, sort_keys=True, separators=(",", ":"))
    expected = hmac.new(
        NOWPAYMENTS_IPN_SECRET.encode(),
        sorted_data.encode(),
        hashlib.sha512,
    ).hexdigest()

    return hmac.compare_digest(expected, received_signature)


def get_minimum_payment_amount(currency: str = "usdt") -> float:
    """Get minimum payment amount for a currency"""
    try:
        url = f"https://api.nowpayments.io/v1/min-amount?currency_from={currency}"
        headers = {"x-api-key": NOWPAYMENTS_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return float(data.get("min_amount", 1))
    except Exception:
        return 1.0  # Default fallback


def get_available_currencies() -> list:
    """Get available cryptocurrencies"""
    try:
        url = "https://api.nowpayments.io/v1/currencies?fixed_rate=true"
        headers = {"x-api-key": NOWPAYMENTS_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get("currencies", [])
    except Exception:
        return []