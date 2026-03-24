from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import submit, admin, payment

app = FastAPI(title="Drift Audit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://deinedomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submit.router)
app.include_router(admin.router)
app.include_router(payment.router)
