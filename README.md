# ⚡ DRIFT AUDIT BACKEND
### SYNTX SYSTEM — CHARLOTTENBURGER DOKUMENTATION
**TRUE_RAW. KEIN OVERENGINEERING. PRODUCTION-READY.**

---

## 0 WAS IST DAS HIER

Zwei Domains. Ein Backend. Null Kompromisse.

Domain 1 - Drift Audit Service:
Ein manuell-gesteuerter, payment-gesicherter, zero-trust Delivery Loop.
Kein Blind-Kauf. Keine ungesicherten Links. Kein Framework-Cargo.

Domain 2 - Structure / Orbit PDF System:
Eine hierarchische PDF-Bibliothek (SuperCategory > Category > PDFItem).
Oeffentlich abrufbar. Fuer den Orbit im Frontend.

DOMAIN 1 - SUBMISSION FLOW
User submit -> Alert an Admin -> User bekommt pending
Admin analysiert (manuell)
Admin triggert /ready -> PayPal Link -> Mail an User
User zahlt -> Webhook -> status = paid
Mail 1: Proton Drive Link
Mail 2: OneTimeSecret Passwort
DONE

DOMAIN 2 - STRUCTURE / ORBIT
GET /structure -> verschachtelte PDF-Bibliothek
Admin CRUD -> SuperCategory / Category / PDFItem
File Upload -> lokal auf Server -> oeffentlich abrufbar

---

## 1 SERVER

Hetzner Ubuntu 24.04 - 30GB RAM / 150GB Disk

IP:         49.13.3.21
HTTPS:      https://audit.syntx-system.com
Intern:     http://127.0.0.1:8080
Path:       /opt/drift-backend
Logs:       /var/log/drift-backend/
Uploads:    /opt/drift-backend/uploads/
Swagger:    https://audit.syntx-system.com/docs

Belegte Ports (NICHT ANFASSEN):
8000 -> uvicorn  (SYNTX LLM)
8001 -> python   (SYNTX Service)
8040 -> python3  (SYNTX Generator)
8080 -> gunicorn (DRIFT AUDIT - WIR)
8090 -> nginx    -> 8080 (alt, HTTP only)
443  -> nginx    -> audit.syntx-system.com -> 8080

---

## 2 TECH STACK

FastAPI          - API Framework
Gunicorn         - WSGI Server (4 Workers)
Uvicorn Worker   - ASGI Worker
PostgreSQL 16    - Datenbank (lokal)
SQLAlchemy 2.0   - ORM
Alembic          - Migrations
python-multipart - File Upload
requests         - PayPal + Brevo HTTP
slowapi          - Rate Limiting
Brevo API        - Mail Relay (Transactional)
Nginx            - Reverse Proxy + SSL
certbot          - SSL Zertifikate (auto-renewal)
systemd          - Service Manager

---

## 3 PROJEKTSTRUKTUR

/opt/drift-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              <- FastAPI App + Router + CORS + StaticFiles
│   ├── config.py            <- Settings aus .env
│   ├── database.py          <- SQLAlchemy Engine + Session
│   ├── models_old.py        <- Submission + PaymentEvent + StatusEnum
│   ├── models/
│   │   ├── __init__.py      <- re-exports alle Models
│   │   └── structure.py     <- SuperCategory, Category, PDFItem
│   ├── schemas.py           <- Pydantic Response Models
│   ├── services.py          <- Business Logic (beide Domains)
│   ├── storage.py           <- File Handling (chunked, lokal)
│   ├── email_service.py     <- Brevo API, multilingual
│   ├── translations.py      <- 10 Sprachen EN/DE/ZH/ES/HI/AR/PT/BN/RU/JA
│   ├── paypal_service.py    <- PayPal Live REST API
│   └── api/
│       ├── __init__.py
│       ├── submit.py        <- POST /submit
│       ├── admin.py         <- Admin Submission Endpoints
│       ├── admin_structure.py <- Admin Structure Endpoints
│       ├── payment.py       <- PayPal Webhook
│       └── structure.py     <- GET /structure (public)
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── dbd2d72bb804_initial.py
│       └── 3fcca0527b7e_add_structure_domain.py
├── alembic.ini
├── uploads/                 <- User PDFs + Structure PDFs
├── .env                     <- SECRETS (nie committen!)
├── .gitignore
├── run.sh                   <- Gunicorn Start Script
└── venv/

---

## 4 DATENBANK

PostgreSQL 16 lokal
DB:     driftaudit
User:   driftuser
Host:   localhost

DOMAIN 1 - Tables:

SUBMISSIONS
id               UUID PRIMARY KEY
url              VARCHAR NOT NULL
email            VARCHAR NOT NULL
file_path        VARCHAR
language         VARCHAR
status           ENUM pending|in_progress|awaiting_payment|paid|delivered
payment_order_id VARCHAR
proton_link      VARCHAR
delivery_password VARCHAR
created_at       TIMESTAMP
updated_at       TIMESTAMP

PAYMENT_EVENTS (idempotent event storage)
id               VARCHAR PRIMARY KEY  <- PayPal Event ID
provider         VARCHAR
event_type       VARCHAR
payload          JSONB
processed        BOOLEAN
created_at       TIMESTAMP

DOMAIN 2 - Tables:

SUPER_CATEGORIES
id          UUID PRIMARY KEY
name        VARCHAR NOT NULL
order       INTEGER DEFAULT 0
is_active   BOOLEAN DEFAULT TRUE
created_at  TIMESTAMP
updated_at  TIMESTAMP

CATEGORIES
id                  UUID PRIMARY KEY
name                VARCHAR NOT NULL
super_category_id   UUID FK -> super_categories.id
order               INTEGER DEFAULT 0
is_active           BOOLEAN DEFAULT TRUE
created_at          TIMESTAMP
updated_at          TIMESTAMP

PDF_ITEMS
id           UUID PRIMARY KEY
title        VARCHAR NOT NULL
description  TEXT
file_url     VARCHAR NOT NULL
category_id  UUID FK -> categories.id
order        INTEGER DEFAULT 0
is_active    BOOLEAN DEFAULT TRUE
created_at   TIMESTAMP
updated_at   TIMESTAMP

---

## 5 STATUS STATE MACHINE (Domain 1)

pending -> in_progress -> awaiting_payment -> paid -> delivered

VALID_TRANSITIONS = {
    "pending":           ["in_progress", "awaiting_payment"],
    "in_progress":       ["awaiting_payment"],
    "awaiting_payment":  ["paid"],
    "paid":              ["delivered"]
}

Kein Ueberspringen rueckwaerts. Integritaet.

---

## 6 API ENDPOINTS

DOMAIN 1 - SUBMISSION

PUBLIC:
POST /submit
  Fields: url, email, language, file (optional PDF)
  Response: {id, status, created_at}

ADMIN (Header: token: ADMIN_TOKEN):
GET   /admin/submissions?status=pending
PATCH /admin/submissions/{id}/ready?proton_link=...&delivery_password=...
PATCH /admin/submissions/{id}/status?new_status=...

WEBHOOK:
POST /payment/webhook  <- PayPal sendet CHECKOUT.ORDER.APPROVED

DOMAIN 2 - STRUCTURE

PUBLIC:
GET /structure
  Response: [{id, name, order, categories: [{id, name, order, pdfs: [...]}]}]
  Nur is_active=True, geordnet nach order

GET /uploads/{filename}  <- PDFs oeffentlich abrufbar

ADMIN (Header: token: ADMIN_TOKEN):
POST   /admin/super-categories
PUT    /admin/super-categories/{id}
DELETE /admin/super-categories/{id}  <- soft delete

POST   /admin/categories
PUT    /admin/categories/{id}
DELETE /admin/categories/{id}        <- soft delete

POST   /admin/pdfs  <- multipart/form-data mit file
PUT    /admin/pdfs/{id}
DELETE /admin/pdfs/{id}              <- soft delete

PATCH  /admin/reorder
  Body: {type: "super_category"|"category"|"pdf", items: [{id, order}]}

---

## 7 ENVIRONMENT (.env)

DATABASE_URL="postgresql://driftuser:PASS@localhost/driftaudit"
UPLOAD_DIR=uploads
ADMIN_TOKEN=->in.env  (openssl rand -base64 32)
PAYPAL_CLIENT_ID=->in.env
PAYPAL_CLIENT_SECRET=->in.env
PAYPAL_MODE=live
PAYPAL_WEBHOOK_ID=->in.env
BREVO_API_KEY=->in.env
FROM_EMAIL=audit@syntx-system.com
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=->in.env
SMTP_PASSWORD=->in.env

WICHTIG: DATABASE_URL Password in Anführungszeichen wegen # Zeichen!
WICHTIG: NIEMALS in Git pushen. .gitignore pruefen.

---

## 8 MAIL FLOW (10 Sprachen)

Alle Mails via Brevo Transactional API (textContent - kein HTML).
Sprache kommt aus submission.language - Fallback: EN.

Unterstuetzte Sprachen: EN, DE, ZH, ES, HI, AR, PT, BN, RU, JA

SUBMIT
  -> send_pending_email(user, language)     "Eingang bestaetigt"
  -> send_admin_alert(admin)                "NEUE SUBMISSION - email"

ADMIN /ready
  -> send_ready_email(user, language)       "Fertig - hier zahlen: {paypal_link}"

WEBHOOK paid
  -> send_delivery_link(user, language)     "Proton Link: {proton_link}"
  -> send_delivery_password(user, language) "Passwort: {password}"

Zero-Trust Delivery:
Link und Passwort kommen in zwei separaten Mails.
Passwort = OneTimeSecret Link empfohlen.

---

## 9 BREVO SETUP

Account: syntxsystem@gmail.com
Plan: Free (300 Mails/Tag)
Sender: audit@syntx-system.com (Proton Alias)
API Key: drift-audit <- in .env als BREVO_API_KEY

DNS Records (Namecheap):
TXT   @                  v=spf1 include:_spf.protonmail.ch include:spf.brevo.com mx ~all
TXT   @                  brevo-code:ddbb9d0d2548d3a481deb109a5099dbf
CNAME brevo1._domainkey  b1.syntx-system-com.dkim.brevo.com
CNAME brevo2._domainkey  b2.syntx-system-com.dkim.brevo.com
TXT   _dmarc             v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com

Bekanntes Problem:
GMX/Arcor/Web.de landen im Spam wegen Brevo IP-Reputation.
Gmail/iCloud/Outlook funktionieren.
Loesung pending: Port 25 (Hetzner) -> direkter SMTP (Max fragen).

---

## 10 SSL & NGINX

Domain: audit.syntx-system.com -> A Record -> 49.13.3.21
Zertifikat: Let's Encrypt via certbot (auto-renewal)
Config: /etc/nginx/sites-available/audit.syntx-system.com

server {
    listen 443 ssl http2;
    server_name audit.syntx-system.com;
    location / {
        proxy_pass http://127.0.0.1:8080;
        client_max_body_size 20M;
    }
}

---

## 11 PAYPAL SETUP (Live)

App: DRIFT-AUDIT (Live)
Account: mirror@syntx-system.com
Webhook URL: https://audit.syntx-system.com/payment/webhook
Webhook ID: 3YH07794KV8190429
Event: CHECKOUT.ORDER.APPROVED
Mode: live
Preis: 49.00 EUR (hardcoded in admin.py)

---

## 12 SYSTEMD SERVICE

File: /etc/systemd/system/drift-backend.service

systemctl start|stop|restart drift-backend
journalctl -u drift-backend -f
tail -f /var/log/drift-backend/error.log
tail -f /var/log/drift-backend/access.log

run.sh:
exec gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8080 \
  --access-logfile /var/log/drift-backend/access.log \
  --error-logfile /var/log/drift-backend/error.log

---

## 13 DEPLOYMENT (von null)

cd /opt && mkdir drift-backend && cd drift-backend
python3 -m venv venv && source venv/bin/activate

pip install fastapi uvicorn gunicorn sqlalchemy psycopg2-binary \
    python-dotenv pydantic alembic python-multipart requests slowapi

apt install postgresql -y
sudo -u postgres psql -c "CREATE USER driftuser WITH PASSWORD 'PASS';"
sudo -u postgres psql -c "CREATE DATABASE driftaudit OWNER driftuser;"

mkdir uploads
# .env befüllen (DATABASE_URL in Anführungszeichen!)

alembic upgrade head

systemctl daemon-reload
systemctl enable drift-backend
systemctl start drift-backend

certbot --nginx -d audit.syntx-system.com

---

## 14 ADMIN WORKFLOW (taeglich)

1. Neue Submissions checken:
   GET /admin/submissions?status=pending

2. Analyse machen (manuell)

3. Proton Drive Link erstellen
   OneTimeSecret fuer Passwort generieren: onetimesecret.com

4. Audit fertig triggern:
   PATCH /admin/submissions/{id}/ready
     ?proton_link=https://...
     ?delivery_password=https://onetimesecret.com/...

5. User zahlt via PayPal
   Webhook setzt status=paid automatisch
   Delivery Mails gehen automatisch raus

6. Status auf delivered setzen:
   PATCH /admin/submissions/{id}/status?new_status=delivered

Admin Dashboard HTML:
Standalone HTML-Datei - lokal im Browser oeffnen.
Spricht direkt mit API via Token-Auth.
Endpoint: https://audit.syntx-system.com

---

## 15 TODO

Port 25 bei Hetzner freischalten (Max fragen)
Direkter SMTP -> GMX/Arcor/Web.de Deliverability fixen
PayPal Webhook Signature Verification
CORS allow_origins erweitern wenn Frontend deployed
Preis konfigurierbar machen (aktuell hardcoded 49.00 EUR)
Repo privat schalten wenn stable

---

## 16 SYSTEM EIGENSCHAFTEN

Zwei Domains (Submission + Structure)
HTTPS audit.syntx-system.com + SSL auto-renewal
Mail Flow komplett (Brevo API, 10 Sprachen)
Zero-Trust Delivery (Link + Passwort getrennt)
Idempotente Webhook-Verarbeitung
Status State Machine (5 States)
Background Tasks (non-blocking)
Systemd Autostart + Restart
PostgreSQL lokal (150GB Disk, 30GB RAM)
File Upload + Static File Serving
Soft Delete (is_active=False)
Reorder (bulk order update)
Git Repository github.com/SYNTX-SYSTEM/drift-audit
Admin Dashboard (standalone HTML)

---

## SYNTX SYSTEM - DRIFT AUDIT V1
Charlottenburger Strasse. Berlin. 2026.
Kein MVP-Gefrickel. Saubere Service-Infrastruktur.
