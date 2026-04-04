import requests
from app.config import settings
from app.translations import get_translation

def send_email(to_email: str, subject: str, body: str):
    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": settings.BREVO_API_KEY,
            "Content-Type": "application/json"
        },
        json={
            "sender": {"name": "SYNTX Drift Audit", "email": settings.FROM_EMAIL},
            "to": [{"email": to_email}],
            "subject": subject,
            "textContent": body
        }
    )
    if response.status_code not in (200, 201):
        raise Exception(f"Brevo API error: {response.status_code} {response.text}")

def send_pending_email(to_email: str, submission_id: str, language: str = "EN", db=None):
    send_email(
        to_email,
        get_translation(language, "pending_subject", db=db),
        get_translation(language, "pending_body", db=db, submission_id=submission_id)
    )

def send_admin_alert(submission_id: str, url: str, email: str, language: str = None, has_file=None):
    file_info = f"✔ {has_file}" if has_file else "✗ Kein PDF"
    lang_info = language if language else "nicht angegeben"
    send_email(
        settings.FROM_EMAIL,
        f"⚡ NEUE SUBMISSION — {email}",
        f"""NEUE DRIFT AUDIT SUBMISSION
══════════════════════════════

ID:        {submission_id}
EMAIL:     {email}
URL:       {url}
SPRACHE:   {lang_info}
DATEI:     {file_info}
STATUS:    pending

══════════════════════════════
— SYNTX Drift Audit System"""
    )

def send_ready_email(to_email: str, paypal_link: str, language: str = "EN", db=None):
    send_email(
        to_email,
        get_translation(language, "ready_subject", db=db),
        get_translation(language, "ready_body", db=db, paypal_link=paypal_link)
    )

def send_delivery_link(to_email: str, proton_link: str, language: str = "EN", db=None):
    send_email(
        to_email,
        get_translation(language, "delivery_link_subject", db=db),
        get_translation(language, "delivery_link_body", db=db, proton_link=proton_link)
    )

def send_delivery_password(to_email: str, password: str, language: str = "EN", db=None):
    send_email(
        to_email,
        get_translation(language, "delivery_password_subject", db=db),
        get_translation(language, "delivery_password_body", db=db, password=password)
    )
