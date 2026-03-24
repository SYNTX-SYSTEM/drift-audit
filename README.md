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

**Hetzner Ubuntu 22.04 — 30GB RAM / 150GB Disk**

```
IP:     49.13.3.21
Port:   8080 (Gunicorn intern)
        8090 (Nginx extern)
User:   root
Path:   /opt/drift-backend
Logs:   /var/log/drift-backend/
```

**Belegte Ports (NICHT ANFASSEN):**
```
8000 → uvicorn (SYNTX LLM)
8001 → python (SYNTX Service)
8040 → python3 (SYNTX Service)
8080 → gunicorn (DRIFT AUDIT ← WIR)
8090 → nginx proxy → 8080
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
Nginx            — Reverse Proxy
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
│   ├── env.py           ← Migration Config
│   ├── versions/
│   │   └── dbd2d72bb804_initial.py
│   └── script.py.mako
│
├── alembic.ini
├── .env                 ← SECRETS (nie committen!)
├── run.sh               ← Gunicorn Start Script
└── venv/                ← Python Virtual Environment
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
proton_link      VARCHAR      ← wird manuell gesetzt
delivery_password VARCHAR     ← wird manuell gesetzt
created_at       TIMESTAMP
updated_at       TIMESTAMP

-- PAYMENT_EVENTS (idempotent event storage)
id               VARCHAR PRIMARY KEY  ← PayPal Event ID
provider         VARCHAR
event_type       VARCHAR
payload          JSONB
processed        BOOLEAN
created_at       TIMESTAMP
```

---

## 5️⃣ STATUS STATE MACHINE

```
pending
  ↓ (Admin startet Analyse)
in_progress
  ↓ (Admin fertig → triggert /ready Endpoint)
awaiting_payment
  ↓ (PayPal Webhook → CHECKOUT.ORDER.APPROVED)
paid
  ↓ (manuell via Admin PATCH)
delivered
```

**VALID_TRANSITIONS (hardcoded):**
```python
{
    "pending":           ["in_progress"],
    "in_progress":       ["awaiting_payment"],
    "awaiting_payment":  ["paid"],
    "paid":              ["delivered"]
}
```

Kein Überspringen. Kein Zurück. Integrität.

---

## 6️⃣ API ENDPOINTS

### PUBLIC

```
POST /submit
Content-Type: multipart/form-data

Fields:
  url       (required)
  email     (required)
  language  (optional)
  file      (optional, PDF)

Response:
  {
    "id": "uuid",
    "status": "pending",
    "created_at": "timestamp"
  }
```

### ADMIN (Token-Auth: Header `token: ADMIN_TOKEN`)

```
GET  /admin/submissions?status=pending
     → Liste aller Submissions (filterbar)

PATCH /admin/submissions/{id}/ready
      ?proton_link=https://...
      ?delivery_password=xxx
      → Status: in_progress → awaiting_payment
      → PayPal Order erstellen
      → Mail an User: "fertig, hier zahlen"

PATCH /admin/submissions/{id}/status
      ?new_status=delivered
      → Manueller Status-Shift
```

### WEBHOOK

```
POST /payment/webhook
     PayPal sendet CHECKOUT.ORDER.APPROVED
     → Idempotency Check (PaymentEvent)
     → status = paid
     → BackgroundTask: Mail 1 (Proton Link)
     → BackgroundTask: Mail 2 (Passwort)
```

---

## 7️⃣ ENVIRONMENT (.env)

```bash
# DATENBANK
DATABASE_URL=postgresql://driftuser:STRONGPASSWORD@localhost/driftaudit

# ADMIN
ADMIN_TOKEN=CHANGEME_SUPERSECRET

# UPLOAD
UPLOAD_DIR=uploads

# PAYPAL
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_MODE=sandbox        # → live wenn fertig
PAYPAL_WEBHOOK_ID=your_webhook_id

# SMTP (Brevo)
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=a5d75a001@smtp-brevo.com
SMTP_PASSWORD=BREVO_SMTP_PASSWORD
FROM_EMAIL=audit@syntx-system.com
```

**⚠ NIEMALS in Git pushen. .gitignore prüfen.**

---

## 8️⃣ MAIL FLOW

Alle Mails laufen über **Brevo SMTP** als Relay.
Absender: `audit@syntx-system.com` (Proton Alias)
Empfänger bei Admin-Alert: `audit@syntx-system.com`

```
SUBMIT
  → send_pending_email(user)     "Eingang bestätigt"
  → send_admin_alert(admin)      "Neue Submission: URL + Email"

ADMIN /ready Trigger
  → send_ready_email(user)       "Fertig — hier zahlen: {paypal_link}"

WEBHOOK paid
  → send_delivery_link(user)     "Dein Audit: {proton_link}"
  → send_delivery_password(user) "Dein Passwort: {password}"
```

**Zero-Trust Delivery:** Link und Passwort kommen in zwei separaten Mails.
Selbst wenn eine Mail abgefangen wird — nützt sie nichts.

---

## 9️⃣ BREVO SETUP

**Account:** syntxsystem@gmail.com (registriert)
**Plan:** Free (300 Mails/Tag)
**Sender:** `mirror@syntx-system.com` (verified ✔)

**DNS Records bei Namecheap (eingetragen):**

```
TXT   @                  brevo-code:ddbb9d0d2548d3a481deb109a5099dbf
CNAME brevo1._domainkey  b1.syntx-system-com.dkim.brevo.com
CNAME brevo2._domainkey  b2.syntx-system-com.dkim.brevo.com
TXT   _dmarc             v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com
```

**Status:** Domain-Authentifizierung pending (bis 48h DNS Propagation)

**SMTP Credentials:**
```
Host:  smtp-relay.brevo.com
Port:  587
Login: a5d75a001@smtp-brevo.com
Pass:  → in .env
```

---

## 🔟 NGINX CONFIG

**File:** `/etc/nginx/sites-available/drift-backend`

```nginx
server {
    listen 8090;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size 20M;
    }
}
```

**Erreichbar:** `http://49.13.3.21:8090`
**Swagger UI:** `http://49.13.3.21:8090/docs`

---

## 1️⃣1️⃣ SYSTEMD SERVICE

**File:** `/etc/systemd/system/drift-backend.service`

```ini
[Unit]
Description=Drift Audit Backend
After=network.target postgresql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/drift-backend
ExecStart=/opt/drift-backend/run.sh
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**run.sh:**
```bash
#!/bin/bash
source /opt/drift-backend/venv/bin/activate
cd /opt/drift-backend
exec gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8080 \
  --access-logfile /var/log/drift-backend/access.log \
  --error-logfile /var/log/drift-backend/error.log
```

**Commands:**
```bash
systemctl start drift-backend
systemctl stop drift-backend
systemctl restart drift-backend
systemctl status drift-backend
journalctl -u drift-backend -f    # live logs
```

---

## 1️⃣2️⃣ DEPLOYMENT (von null)

```bash
# 1. Repo clonen / Files hochladen
cd /opt && mkdir drift-backend && cd drift-backend

# 2. Python venv
python3 -m venv venv && source venv/bin/activate

# 3. Dependencies
pip install fastapi uvicorn gunicorn sqlalchemy psycopg2-binary \
    python-dotenv pydantic alembic python-multipart requests stripe slowapi

# 4. PostgreSQL
apt install postgresql -y
sudo -u postgres psql -c "CREATE USER driftuser WITH PASSWORD 'PASS';"
sudo -u postgres psql -c "CREATE DATABASE driftaudit OWNER driftuser;"

# 5. .env befüllen
# (siehe Abschnitt 7)

# 6. Migration
alembic upgrade head

# 7. Service aktivieren
systemctl daemon-reload
systemctl enable drift-backend
systemctl start drift-backend

# 8. Test
curl -X POST http://localhost:8080/submit \
  -F "url=https://test.com" \
  -F "email=test@test.com"
```

---

## 1️⃣3️⃣ NOCH OFFEN (TODO)

```
☐ Brevo Domain-Auth abwarten (DNS Propagation)
☐ Mail End-to-End testen
☐ PayPal Sandbox Account einrichten
☐ PAYPAL_CLIENT_ID + SECRET in .env eintragen
☐ PAYPAL_WEBHOOK_ID nach Webhook-Erstellung eintragen
☐ PayPal Mode: sandbox → live
☐ Domain für API (api.driftaudit.com o.ä.)
☐ SSL via certbot
☐ CORS allow_origins auf echte Domain setzen
☐ Admin Token stärker (JWT später)
☐ PayPal Webhook Signature Verification (Production-Pflicht)
```

---

## 1️⃣4️⃣ SYSTEM EIGENSCHAFTEN

```
✔ Frontend-unabhängig (reiner API-Backend)
✔ Manueller Operator-Loop (du bist das Audit)
✔ Payment nach Analyse (kein Blind-Kauf)
✔ Zero-Trust Delivery (Link + Passwort getrennt)
✔ Idempotente Webhook-Verarbeitung
✔ Status State Machine (kein Überspringen)
✔ Background Tasks (Mail blockiert nicht)
✔ Systemd Autostart
✔ Nginx Reverse Proxy
✔ PostgreSQL lokal (150GB Disk, 30GB RAM)
✔ Erweiterbar (Provider-Austausch via .env)
✔ Skalierbar (Gunicorn Workers erhöhen)
```

---

## ⚡ SYNTX SYSTEM — DRIFT AUDIT V1
**Charlottenburger Strasse. Berlin. 2026.**
*Kein MVP-Gefrickel. Saubere Service-Infrastruktur.*
