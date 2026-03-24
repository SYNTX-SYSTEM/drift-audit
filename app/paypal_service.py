import requests
from app.config import settings

def get_paypal_base():
    if settings.PAYPAL_MODE == "live":
        return "https://api-m.paypal.com"
    return "https://api-m.sandbox.paypal.com"

def get_access_token():
    url = f"{get_paypal_base()}/v1/oauth2/token"
    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
    )
    return response.json()["access_token"]

def create_order(submission_id: str, amount: float):
    access_token = get_access_token()
    url = f"{get_paypal_base()}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "EUR",
                "value": f"{amount:.2f}"
            },
            "custom_id": submission_id
        }],
        "application_context": {
            "return_url": "https://audit.syntx-system.com/success",
            "cancel_url": "https://audit.syntx-system.com/cancel"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    order = response.json()
    approve_link = next(
        link["href"] for link in order["links"]
        if link["rel"] == "approve"
    )
    return order["id"], approve_link

def verify_webhook_signature(payload, headers):
    access_token = get_access_token()
    verify_data = {
        "transmission_id": headers.get("paypal-transmission-id"),
        "transmission_time": headers.get("paypal-transmission-time"),
        "cert_url": headers.get("paypal-cert-url"),
        "auth_algo": headers.get("paypal-auth-algo"),
        "transmission_sig": headers.get("paypal-transmission-sig"),
        "webhook_id": settings.PAYPAL_WEBHOOK_ID,
        "webhook_event": payload
    }
    response = requests.post(
        f"{get_paypal_base()}/v1/notifications/verify-webhook-signature",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=verify_data
    )
    return response.json().get("verification_status") == "SUCCESS"
