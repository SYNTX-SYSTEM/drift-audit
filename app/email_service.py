import smtplib
from email.mime.text import MIMEText
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
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
        f"Deine Anfrage ist eingegangen.\n\nSubmission-ID: {submission_id}\n\nWir melden uns sobald dein Audit fertig ist."
    )

def send_admin_alert(submission_id: str, url: str, email: str):
    send_email(
        settings.FROM_EMAIL,
        "Neuer Drift Audit Eingang",
        f"Neue Submission:\n\nID: {submission_id}\nURL: {url}\nEmail: {email}"
    )

def send_ready_email(to_email: str, paypal_link: str):
    send_email(
        to_email,
        "Drift Audit – Dein Audit ist fertig",
        f"Dein Audit ist fertig.\n\nJetzt bezahlen und Ergebnis erhalten:\n{paypal_link}"
    )

def send_delivery_link(to_email: str, proton_link: str):
    send_email(
        to_email,
        "Drift Audit – Dein Ergebnis",
        f"Dein Audit ist verfügbar:\n\n{proton_link}"
    )

def send_delivery_password(to_email: str, password: str):
    send_email(
        to_email,
        "Drift Audit – Dein Zugangspasswort",
        f"Dein Passwort für das Audit-Dokument:\n\n{password}"
    )
