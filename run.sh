#!/bin/bash
source /opt/drift-backend/venv/bin/activate
cd /opt/drift-backend
exec gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8080 \
  --access-logfile /var/log/drift-backend/access.log \
  --error-logfile /var/log/drift-backend/error.log
