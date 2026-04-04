from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import submit, admin, payment
from app.api.structure import router as structure_router
from app.api.admin_structure import router as admin_structure_router
from app.api.admin_mail import router as admin_mail_router
import os

app = FastAPI(title="Drift Audit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://audit.syntx-system.com", "https://admin.syntx-system.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(submit.router)
app.include_router(admin.router)
app.include_router(payment.router)
app.include_router(structure_router)
app.include_router(admin_structure_router)
app.include_router(admin_mail_router)
