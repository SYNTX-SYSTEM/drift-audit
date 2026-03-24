# ⚡ DRIFT AUDIT BACKEND
### SYNTX SYSTEM — CHARLOTTENBURGER DOKUMENTATION
**TRUE_RAW. KEIN OVERENGINEERING. PRODUCTION-READY.**

---

## 0️⃣ WAS IST DAS HIER

Ein **manuell-gesteuerter, payment-gesicherter, zero-trust Delivery Loop** für den SYNTX Drift Audit Service.

Kein Blind-Kauf. Keine ungesicherten Links. Kein Framework-Cargo.
```
SUBMIT
User gibt ein → du bekommst Alert → User bekommt "pending"
        ↓
ANALYSE
Du machst die Arbeit. Manuell. Das ist der Job.
        ↓
GATE
Admin triggert "fertig" → User bekommt Mail mit PayPal Link
        ↓
PAYMENT
User zahlt → Webhook → status = paid
        ↓
DELIVERY
Mail 1: Proton Drive Link
Mail 2: Passwort (separat — zero-trust)
        ↓
DONE ✔
```

---

## 1️⃣ SERVER

**Hetzner Ubuntu 24.04 — 30GB RAM / 150GB Disk**
```
IP:     49.13.3.21
HTTPS:  https://audit.syntx-system.com
Port:   8080 (Gunicorn intern)
Path:   /opt/drift-backend
Logs:   /var/log/drift-backend/
```

**Belegte Ports (NICHT ANFASSEN):**
```
8000 → uvicorn (SYNTX LLM)
8001 → python (SYNTX Service)
8040 → python3 (SYNTX Service)
8080 → gunicorn (DRIFT AUDIT ← WIR)
8090 → nginx proxy → 8080 (alt, HTTP only)
443  → nginx → audit.syntx-system.com → 8080
```

---

## 2️⃣ TECH STACK
```
FastAPI          — API Framework
Gunicorn         — WSGI Server (4 Workers)
Uvicorn Worker   — ASGI Worker
PostgreSQL 16    — Datenbank (lokal)
SQLAlchemy 2.0   — ORM
Alembic          — Migrations
python-multipart — File Upload
requests         — PayPal HTTP
slowapi          — Rate Limiting
smtplib          — Mail (stdlib)
Brevo SMTP       — Mail Relay
Nginx            — Reverse Proxy + SSL
certbot          — SSL Zertifikate
systemd          — Service Manager
```

---

## 3️⃣ PROJEKTSTRUKTUR
```
/opt/drift-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py          ← FastAPI App + Router + CORS
│   ├── config.py        ← Settings aus .env
│   ├── database.py      ← SQLAlchemy Engine + Session
│   ├── models.py        ← Submission + PaymentEvent
│   ├── schemas.py       ← Pydantic Response Models
│   ├── services.py      ← Business Logic + State Machine
│   ├── storage.py       ← File Handling (lokal)
│   ├── email_service.py ← Alle Mail-Funktionen
│   ├── paypal_service.py← PayPal REST API
│   └── api/
│       ├── __init__.py
│       ├── submit.py    ← POST /submit
│       ├── admin.py     ← Admin Endpoints (Token-Auth)
│       └── payment.py   ← PayPal Webhook
│
├── alembic/
│   ├── env.py
│   └── versions/
│       └── dbd2d72bb804_initial.py
│
├── alembic.ini
├── .env                 ← SECRETS (nie committen!)
├── .gitignore
├── run.sh               ← Gunicorn Start Script
└── venv/
```

---

## 4️⃣ DATENBANK

**PostgreSQL 16 lokal**
```
DB:     driftaudit
User:   driftuser
Host:   localhost
```

**Tables:**
```sql
-- SUBMISSIONS
id               UUID PRIMARY KEY
url              VARCHAR NOT NULL
email            VARCHAR NOT NULL
file_path        VARCHAR
language         VARCHAR
status           ENUM (pending|in_progress|awaiting_payment|paid|delivered)
payment_order_id VARCHAR
proton_link      VARCHAR
delivery_password VARCHAR
created_at       TIMESTAMP
updated_at       TIMESTAMP

-- PAYMENT_EVENTS (idempotent)
id               VARCHAR PRIMARY KEY
provider         VARCHAR
event_type       VARCHAR
payload          JSONB
processed        BOOLEAN
created_at       TIMESTAMP
```

---

## 5️⃣ STATUS STATE MACHINE
```
pending → in_progress → awaiting_payment → paid → delivered
```
```python
VALID_TRANSITIONS = {
    "pending":           ["in_progress"],
    "in_progress":       ["awaiting_payment"],
    "awaiting_payment":  ["paid"],
    "paid":              ["delivered"]
}
```

---

## 6️⃣ API ENDPOINTS
```
POST /submit                              ← User Submit
GET  /admin/submissions?status=pending    ← Admin Liste
PATCH /admin/submissions/{id}/ready       ← Admin: Audit fertig
PATCH /admin/submissions/{id}/status      ← Admin: Status manuell
POST /payment/webhook                     ← PayPal Webhook
GET  /docs                                ← Swagger UI
```

---

## 7️⃣ ENVIRONMENT (.env)
```bash
DATABASE_URL="postgresql://driftuser:PASS@localhost/driftaudit"
UPLOAD_DIR=uploads
ADMIN_TOKEN=changeme_supersecret

SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=a5d75a001@smtp-brevo.com
SMTP_PASSWORD=→in.env
FROM_EMAIL=audit@syntx-system.com

PAYPAL_CLIENT_ID=→in.env
PAYPAL_CLIENT_SECRET=→in.env
PAYPAL_MODE=sandbox
PAYPAL_WEBHOOK_ID=2AY34742FW5483355
```

**⚠ DATABASE_URL Password in Anführungszeichen wegen # Zeichen!**
**⚠ NIEMALS in Git pushen.**

---

## 8️⃣ MAIL FLOW
```
SUBMIT
  → send_pending_email(user)     "Eingang bestätigt"
  → send_admin_alert(admin)      "Neue Submission"

ADMIN /ready
  → send_ready_email(user)       "Fertig — hier zahlen"

WEBHOOK paid
  → send_delivery_link(user)     "Proton Link"
  → send_delivery_password(user) "Passwort"
```

**Absender:** `audit@syntx-system.com` (Proton Alias)
**Relay:** Brevo SMTP (300 Mails/Tag kostenlos)

---

## 9️⃣ BREVO SETUP

**Account:** syntxsystem@gmail.com
**Plan:** Free (300 Mails/Tag)
**Status:** Domain verifiziert ✔

**DNS Records (Namecheap):**
```
TXT   @                  brevo-code:ddbb9d0d2548d3a481deb109a5099dbf ✔
CNAME brevo1._domainkey  b1.syntx-system-com.dkim.brevo.com ✔
CNAME brevo2._domainkey  b2.syntx-system-com.dkim.brevo.com ✔
TXT   _dmarc             v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com ✔
```

---

## 🔟 SSL & NGINX

**Domain:** `audit.syntx-system.com` → A Record → `49.13.3.21`
**Zertifikat:** Let's Encrypt via certbot (auto-renewal) ✔
**Config:** `/etc/nginx/sites-available/audit.syntx-system.com`
**Swagger:** `https://audit.syntx-system.com/docs`

---

## 1️⃣1️⃣ PAYPAL SETUP

**App:** DRIFT AUDIT (Sandbox)
**Webhook URL:** `https://audit.syntx-system.com/payment/webhook`
**Webhook ID:** `2AY34742FW5483355`
**Event:** `CHECKOUT.ORDER.APPROVED`
**Status:** API Auth pending (Account Aktivierung)

---

## 1️⃣2️⃣ SYSTEMD SERVICE
```bash
systemctl start|stop|restart drift-backend
journalctl -u drift-backend -f
```

**run.sh:**
```bash
exec gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8080
```

---

## 1️⃣3️⃣ DEPLOYMENT (von null)
```bash
cd /opt && mkdir drift-backend && cd drift-backend
python3 -m venv venv && source venv/bin/activate
pip install fastapi uvicorn gunicorn sqlalchemy psycopg2-binary \
    python-dotenv pydantic alembic python-multipart requests stripe slowapi
apt install postgresql -y
sudo -u postgres psql -c "CREATE USER driftuser WITH PASSWORD 'PASS';"
sudo -u postgres psql -c "CREATE DATABASE driftaudit OWNER driftuser;"
# .env befüllen
alembic upgrade head
systemctl enable drift-backend && systemctl start drift-backend
```

---

## 1️⃣4️⃣ TODO
```
☐ PayPal API Auth (Account Aktivierung abwarten)
☐ End-to-End Payment Flow testen
☐ ADMIN_TOKEN stärken
☐ PayPal Webhook Signature Verification (Production-Pflicht)
☐ CORS allow_origins auf echte Domain setzen
☐ PayPal Mode: sandbox → live
```

---

## 1️⃣5️⃣ SYSTEM EIGENSCHAFTEN
```
✔ HTTPS (audit.syntx-system.com)
✔ SSL via certbot (auto-renewal)
✔ Mail Flow komplett (Brevo + Proton)
✔ Zero-Trust Delivery (Link + Passwort getrennt)
✔ Idempotente Webhook-Verarbeitung
✔ Status State Machine
✔ Background Tasks
✔ Systemd Autostart
✔ PostgreSQL lokal
✔ Git Repository
```

---

## ⚡ SYNTX SYSTEM — DRIFT AUDIT V1
**Charlottenburger Strasse. Berlin. 2026.**
*Kein MVP-Gefrickel. Saubere Service-Infrastruktur.*
