import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, to_email, msg.as_string())

def send_pending_email(to_email: str, submission_id: str):
    send_email(
        to_email,
        "Drift Audit – Eingang bestätigt",
        f"""Deine Anfrage ist eingegangen.

Submission-ID: {submission_id}

Wir analysieren deinen Content und melden uns sobald dein Audit fertig ist.
Du erhältst dann einen Link zur Zahlung und danach dein Ergebnis.

— SYNTX System"""
    )

def send_admin_alert(submission_id: str, url: str, email: str, language: str = None, has_file: bool = False):
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
→ Admin Dashboard öffnen:
https://audit.syntx-system.com/docs

Wenn du fertig bist:
PATCH /admin/submissions/{submission_id}/ready
  ?proton_link=...
  ?delivery_password=...

— SYNTX Drift Audit System"""
    )

def send_ready_email(to_email: str, paypal_link: str):
    send_email(
        to_email,
        "Drift Audit – Dein Audit ist fertig",
        f"""Dein Audit ist fertig.

Jetzt bezahlen und dein Ergebnis erhalten:

→ {paypal_link}

Nach der Zahlung erhältst du automatisch:
  1. Den Link zu deinem Audit-Dokument
  2. Das Passwort in einer separaten Mail

— SYNTX System"""
    )

def send_delivery_link(to_email: str, proton_link: str):
    send_email(
        to_email,
        "Drift Audit – Dein Ergebnis",
        f"""Dein Audit ist verfügbar.

→ {proton_link}

Das Passwort erhältst du in einer separaten Mail.

— SYNTX System"""
    )

def send_delivery_password(to_email: str, password: str):
    send_email(
        to_email,
        "Drift Audit – Dein Zugangspasswort",
        f"""Dein Passwort für das Audit-Dokument:

{password}

— SYNTX System"""
    )
