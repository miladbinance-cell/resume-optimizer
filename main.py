"""
ResumeAI — AI-Powered Resume Optimizer
FastAPI application entry point
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import UPLOAD_DIR, ENVIRONMENT

# Create upload directory
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("static", exist_ok=True)

app = FastAPI(
    title="ResumeAI",
    description="AI-powered resume optimization for ATS systems",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": ENVIRONMENT}


# Import and register routers
from routers import pages, upload, payment, webhooks as webhook_routes

app.include_router(pages.router)
app.include_router(upload.router)
app.include_router(payment.router)
app.include_router(webhook_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)