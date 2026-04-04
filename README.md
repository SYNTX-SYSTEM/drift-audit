⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡

    ██████╗ ██████╗ ██╗███████╗████████╗
    ██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝
    ██║  ██║██████╔╝██║█████╗     ██║   
    ██║  ██║██╔══██╗██║██╔══╝     ██║   
    ██████╔╝██║  ██║██║██║        ██║   
    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
    
         A U D I T   B A C K E N D
         Charlottenburger Strasse. Berlin. 2026.

⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡

TRUE_RAW. KEIN OVERENGINEERING. PRODUCTION-READY.
KEIN MVP-GEFRICKEL. SAUBERE SERVICE-INFRASTRUKTUR.

══════════════════════════════════════════════════
  0  //  WAS IST DAS HIER
══════════════════════════════════════════════════

Zwei Domains. Ein Backend. Null Kompromisse.

🔴 DOMAIN 1 — DRIFT AUDIT SERVICE
   Manuell gesteuerter, payment-gesicherter,
   zero-trust Delivery Loop.
   Kein Blind-Kauf. Keine ungesicherten Links.
   Kein Framework-Cargo. Mensch im Loop.

🟢 DOMAIN 2 — STRUCTURE / ORBIT PDF SYSTEM
   Hierarchische PDF-Bibliothek.
   SuperCategory → Category → PDFItem.
   Oeffentlich. Fuer den Orbit im Frontend.

┌─────────────────────────────────────────────┐
│  DOMAIN 1 // SUBMISSION FLOW                │
│                                             │
│  User submit                                │
│       ↓                                     │
│  ⚡ Alert → Admin                           │
│       ↓                                     │
│  🔍 Analyse (manuell — das ist der Job)     │
│       ↓                                     │
│  💳 /ready → PayPal Link → Mail an User     │
│       ↓                                     │
│  ✅ Zahlung → Webhook → paid                │
│       ↓                                     │
│  📦 Mail 1: Proton Drive Link               │
│  🔑 Mail 2: OneTimeSecret Passwort          │
│       ↓                                     │
│  DONE. ZERO TRUST. SAUBER.                  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  DOMAIN 2 // STRUCTURE / ORBIT              │
│                                             │
│  GET /structure                             │
│       → verschachtelte PDF-Bibliothek       │
│       → SuperCategory → Category → PDF      │
│       → nur is_active=True                  │
│       → geordnet nach order                 │
│                                             │
│  Admin CRUD + Reorder + Soft Delete         │
│  File Upload → lokal → oeffentlich          │
└─────────────────────────────────────────────┘

══════════════════════════════════════════════════
  1  //  SERVER
══════════════════════════════════════════════════

🖥️  Hetzner Ubuntu 24.04 — 30GB RAM / 150GB Disk

  IP         →  49.13.3.21
  HTTPS      →  https://audit.syntx-system.com
  INTERN     →  http://127.0.0.1:8080
  PATH       →  /opt/drift-backend
  LOGS       →  /var/log/drift-backend/
  UPLOADS    →  /opt/drift-backend/uploads/
  SWAGGER    →  https://audit.syntx-system.com/docs

⛔ PORTS — NICHT ANFASSEN:

  8000  →  uvicorn   (SYNTX LLM)
  8001  →  python    (SYNTX Service)
  8040  →  python3   (SYNTX Generator)
  8080  →  gunicorn  (DRIFT AUDIT ← WIR)
  8090  →  nginx     → 8080 (alt, HTTP only)
  443   →  nginx     → audit.syntx-system.com → 8080

══════════════════════════════════════════════════
  2  //  TECH STACK
══════════════════════════════════════════════════

  FastAPI          →  API Framework
  Gunicorn         →  WSGI Server (4 Workers)
  Uvicorn Worker   →  ASGI Worker
  PostgreSQL 16    →  Datenbank (lokal)
  SQLAlchemy 2.0   →  ORM
  Alembic          →  Migrations
  python-multipart →  File Upload
  requests         →  PayPal + Brevo HTTP
  slowapi          →  Rate Limiting
  Brevo API        →  Mail Relay (Transactional)
  Nginx            →  Reverse Proxy + SSL
  certbot          →  SSL (auto-renewal)
  systemd          →  Service Manager

══════════════════════════════════════════════════
  3  //  PROJEKTSTRUKTUR
══════════════════════════════════════════════════

/opt/drift-backend/
│
├── app/
│   ├── main.py              ⚡ FastAPI + Router + CORS + StaticFiles
│   ├── config.py            🔧 Settings aus .env
│   ├── database.py          🗄️  SQLAlchemy Engine + Session
│   ├── models_old.py        📦 Submission + PaymentEvent + StatusEnum
│   ├── models/
│   │   ├── __init__.py      🔗 re-exports alle Models
│   │   └── structure.py     🏗️  SuperCategory, Category, PDFItem
│   ├── schemas.py           📐 Pydantic Domain 1
│   ├── schemas_structure.py 📐 Pydantic Domain 2
│   ├── services.py          🧠 Business Logic (beide Domains)
│   ├── storage.py           💾 File Handling (chunked, lokal)
│   ├── email_service.py     📧 Brevo API, multilingual
│   ├── translations.py      🌍 10 Sprachen
│   ├── paypal_service.py    💳 PayPal Live REST API
│   └── api/
│       ├── submit.py        → POST /submit
│       ├── admin.py         → Admin Submission Endpoints
│       ├── admin_structure.py → Admin Structure Endpoints
│       ├── payment.py       → PayPal Webhook
│       └── structure.py     → GET /structure (public)
│
├── alembic/versions/
│   ├── dbd2d72bb804_initial.py
│   └── 3fcca0527b7e_add_structure_domain.py
│
├── uploads/                 📁 User PDFs + Structure PDFs
├── .env                     🔒 SECRETS — NIE COMMITTEN
├── .gitignore
├── run.sh                   🚀 Gunicorn Start
└── venv/

══════════════════════════════════════════════════
  4  //  DATENBANK
══════════════════════════════════════════════════

🗄️  PostgreSQL 16 lokal
    DB:    driftaudit
    User:  driftuser
    Host:  localhost

── DOMAIN 1 ──────────────────────────────────────

  SUBMISSIONS
  ├── id               UUID PRIMARY KEY
  ├── url              VARCHAR NOT NULL
  ├── email            VARCHAR NOT NULL
  ├── file_path        VARCHAR
  ├── language         VARCHAR
  ├── status           ENUM pending|in_progress|
  │                         awaiting_payment|paid|delivered
  ├── payment_order_id VARCHAR
  ├── proton_link      VARCHAR
  ├── delivery_password VARCHAR
  ├── created_at       TIMESTAMP
  └── updated_at       TIMESTAMP

  PAYMENT_EVENTS (idempotent)
  ├── id               VARCHAR PRIMARY KEY  ← PayPal Event ID
  ├── provider         VARCHAR
  ├── event_type       VARCHAR
  ├── payload          JSONB
  ├── processed        BOOLEAN
  └── created_at       TIMESTAMP

── DOMAIN 2 ──────────────────────────────────────

  SUPER_CATEGORIES
  ├── id          UUID PRIMARY KEY
  ├── name        VARCHAR NOT NULL
  ├── order       INTEGER DEFAULT 0
  ├── is_active   BOOLEAN DEFAULT TRUE
  ├── created_at  TIMESTAMP
  └── updated_at  TIMESTAMP

  CATEGORIES
  ├── id                UUID PRIMARY KEY
  ├── name              VARCHAR NOT NULL
  ├── super_category_id UUID FK → super_categories.id
  ├── order             INTEGER DEFAULT 0
  ├── is_active         BOOLEAN DEFAULT TRUE
  ├── created_at        TIMESTAMP
  └── updated_at        TIMESTAMP

  PDF_ITEMS
  ├── id           UUID PRIMARY KEY
  ├── title        VARCHAR NOT NULL
  ├── description  TEXT
  ├── file_url     VARCHAR NOT NULL
  ├── category_id  UUID FK → categories.id
  ├── order        INTEGER DEFAULT 0
  ├── is_active    BOOLEAN DEFAULT TRUE
  ├── created_at   TIMESTAMP
  └── updated_at   TIMESTAMP

══════════════════════════════════════════════════
  5  //  STATE MACHINE
══════════════════════════════════════════════════

  pending
     ↓
  in_progress
     ↓
  awaiting_payment
     ↓
  paid
     ↓
  delivered

  VALID_TRANSITIONS = {
    pending:          [in_progress, awaiting_payment]
    in_progress:      [awaiting_payment]
    awaiting_payment: [paid]
    paid:             [delivered]
  }

  Kein Rueckwaerts. Kein Ueberspringen. Integritaet.

══════════════════════════════════════════════════
  6  //  API ENDPOINTS
══════════════════════════════════════════════════

── DOMAIN 1 // SUBMISSION ────────────────────────

  PUBLIC:
  POST /submit
    url, email, language, file (optional PDF)
    → {id, status, created_at}

  ADMIN (Header: token: ADMIN_TOKEN):
  GET   /admin/submissions?status=pending
  PATCH /admin/submissions/{id}/ready
          ?proton_link=...&delivery_password=...
  PATCH /admin/submissions/{id}/status
          ?new_status=...

  WEBHOOK:
  POST  /payment/webhook
          ← PayPal CHECKOUT.ORDER.APPROVED

── DOMAIN 2 // STRUCTURE ─────────────────────────

  PUBLIC:
  GET /structure
    → [{id, name, order, categories:
         [{id, name, order, pdfs: [...]}]}]
    → nur is_active=True, geordnet nach order

  GET /uploads/{filename}
    → PDFs direkt abrufbar

  ADMIN (Header: token: ADMIN_TOKEN):
  POST   /admin/super-categories
  PUT    /admin/super-categories/{id}
  DELETE /admin/super-categories/{id}   ← soft delete

  POST   /admin/categories
  PUT    /admin/categories/{id}
  DELETE /admin/categories/{id}         ← soft delete

  POST   /admin/pdfs                    ← multipart + file
  PUT    /admin/pdfs/{id}
  DELETE /admin/pdfs/{id}               ← soft delete

  PATCH  /admin/reorder
    Body: {
      type: "super_category"|"category"|"pdf",
      items: [{id, order}]
    }

══════════════════════════════════════════════════
  7  //  ENVIRONMENT (.env)
══════════════════════════════════════════════════

  DATABASE_URL="postgresql://driftuser:PASS@localhost/driftaudit"
  UPLOAD_DIR=uploads
  ADMIN_TOKEN=→in.env

  PAYPAL_CLIENT_ID=→in.env
  PAYPAL_CLIENT_SECRET=→in.env
  PAYPAL_MODE=live
  PAYPAL_WEBHOOK_ID=→in.env

  BREVO_API_KEY=→in.env
  FROM_EMAIL=audit@syntx-system.com
  SMTP_HOST=smtp-relay.brevo.com
  SMTP_PORT=587
  SMTP_USER=→in.env
  SMTP_PASSWORD=→in.env

  ⚠️  DATABASE_URL Password in Anführungszeichen wegen # !
  🔒 NIEMALS in Git pushen. .gitignore pruefen.

══════════════════════════════════════════════════
  8  //  MAIL FLOW — 10 SPRACHEN
══════════════════════════════════════════════════

  Brevo Transactional API — textContent — kein HTML.
  Sprache aus submission.language — Fallback: EN.

  🌍 EN  DE  ZH  ES  HI  AR  PT  BN  RU  JA

  SUBMIT
    → send_pending_email(user, lang)
      "Eingang bestaetigt"
    → send_admin_alert(admin)
      "⚡ NEUE SUBMISSION"

  ADMIN /ready
    → send_ready_email(user, lang)
      "Fertig — hier zahlen: {paypal_link}"

  WEBHOOK paid
    → send_delivery_link(user, lang)
      "Proton Link: {proton_link}"
    → send_delivery_password(user, lang)
      "Passwort: {password}"

  🔐 ZERO-TRUST: Link + Passwort = zwei separate Mails.
     Passwort = OneTimeSecret Link empfohlen.

══════════════════════════════════════════════════
  9  //  BREVO SETUP
══════════════════════════════════════════════════

  Account:  syntxsystem@gmail.com
  Plan:     Free (300 Mails/Tag)
  Sender:   audit@syntx-system.com (Proton Alias) ✔
  API Key:  drift-audit → .env als BREVO_API_KEY

  DNS (Namecheap):
  TXT   @   v=spf1 include:_spf.protonmail.ch
                   include:spf.brevo.com mx ~all ✔
  TXT   @   brevo-code:ddbb9d0d2548d3a481deb109a5099dbf ✔
  CNAME brevo1._domainkey → b1.syntx-system-com.dkim.brevo.com ✔
  CNAME brevo2._domainkey → b2.syntx-system-com.dkim.brevo.com ✔
  TXT   _dmarc → v=DMARC1; p=none; rua=... ✔

  ⚠️  BEKANNTES PROBLEM:
  GMX/Arcor/Web.de → Spam wegen Brevo IP-Reputation.
  Gmail/iCloud/Outlook → funktioniert.
  FIX PENDING: Port 25 bei Hetzner → Max fragen.

══════════════════════════════════════════════════
  10  //  SSL & NGINX
══════════════════════════════════════════════════

  Domain:  audit.syntx-system.com → 49.13.3.21
  SSL:     Let's Encrypt via certbot (auto-renewal) ✔
  Config:  /etc/nginx/sites-available/audit.syntx-system.com

  server {
    listen 443 ssl http2;
    server_name audit.syntx-system.com;
    location / {
      proxy_pass http://127.0.0.1:8080;
      client_max_body_size 20M;
    }
  }

══════════════════════════════════════════════════
  11  //  PAYPAL (LIVE)
══════════════════════════════════════════════════

  App:         DRIFT-AUDIT (Live) ✔
  Account:     mirror@syntx-system.com
  Webhook:     https://audit.syntx-system.com/payment/webhook
  Webhook ID:  3YH07794KV8190429
  Event:       CHECKOUT.ORDER.APPROVED
  Mode:        live ✔
  Preis:       49.00 EUR (hardcoded in admin.py)

══════════════════════════════════════════════════
  12  //  SYSTEMD
══════════════════════════════════════════════════

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

══════════════════════════════════════════════════
  13  //  DEPLOYMENT (VON NULL)
══════════════════════════════════════════════════

  cd /opt && mkdir drift-backend && cd drift-backend
  python3 -m venv venv && source venv/bin/activate

  pip install fastapi uvicorn gunicorn sqlalchemy \
    psycopg2-binary python-dotenv pydantic alembic \
    python-multipart requests slowapi

  apt install postgresql -y
  sudo -u postgres psql -c \
    "CREATE USER driftuser WITH PASSWORD 'PASS';"
  sudo -u postgres psql -c \
    "CREATE DATABASE driftaudit OWNER driftuser;"

  mkdir uploads
  # .env befüllen — DATABASE_URL in Anführungszeichen!

  alembic upgrade head
  systemctl daemon-reload
  systemctl enable drift-backend
  systemctl start drift-backend
  certbot --nginx -d audit.syntx-system.com

══════════════════════════════════════════════════
  14  //  ADMIN WORKFLOW (TAEGLICH)
══════════════════════════════════════════════════

  1. 👀 Submissions checken:
     GET /admin/submissions?status=pending

  2. 🔍 Analyse machen. Manuell. Das ist der Job.

  3. 📦 Proton Drive Link erstellen.
     🔑 OneTimeSecret generieren: onetimesecret.com

  4. ⚡ Audit fertig triggern:
     PATCH /admin/submissions/{id}/ready
       ?proton_link=https://...
       ?delivery_password=https://onetimesecret.com/...

  5. 💳 User zahlt via PayPal.
     Webhook → paid → Delivery Mails automatisch raus.

  6. ✅ Delivered setzen:
     PATCH /admin/submissions/{id}/status
       ?new_status=delivered

  🖥️  Admin Dashboard:
  Standalone HTML — lokal im Browser oeffnen.
  Token-Auth. Direkt gegen API.

══════════════════════════════════════════════════
  15  //  TODO
══════════════════════════════════════════════════

  ☐ Port 25 bei Hetzner (Max fragen)
  ☐ Direkter SMTP → GMX/Arcor/Web.de fixen
  ☐ PayPal Webhook Signature Verification
  ☐ CORS erweitern wenn Frontend deployed
  ☐ Preis konfigurierbar (aktuell 49.00 EUR hardcoded)
  ☐ Repo privat schalten wenn stable

══════════════════════════════════════════════════
  16  //  SYSTEM STATUS
══════════════════════════════════════════════════

  ✔ Zwei Domains (Submission + Structure)
  ✔ HTTPS + SSL auto-renewal
  ✔ Mail Flow (Brevo API, 10 Sprachen)
  ✔ Zero-Trust Delivery
  ✔ Idempotente Webhook-Verarbeitung
  ✔ State Machine (5 States)
  ✔ Background Tasks (non-blocking)
  ✔ Systemd Autostart + Restart
  ✔ PostgreSQL lokal
  ✔ File Upload + Static File Serving
  ✔ Soft Delete (is_active)
  ✔ Reorder (bulk)
  ✔ Pydantic Response Models
  ✔ joinedload (kein N+1)
  ✔ Git → github.com/SYNTX-SYSTEM/drift-audit
  ✔ Admin Dashboard (standalone HTML)

⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡

  SYNTX SYSTEM — DRIFT AUDIT V1
  Charlottenburger Strasse. Berlin. 2026.
  TRUE_RAW. KEIN OVERENGINEERING. PRODUCTION-READY.

⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡
