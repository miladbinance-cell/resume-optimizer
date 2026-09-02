import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import UPLOAD_DIR, MAX_UPLOAD_SIZE_MB
from services.resume_parser import extract_text_from_file

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/upload", tags=["upload"])


@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/resume")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_title: str = Form(""),
    company: str = Form(""),
    job_description: str = Form(""),
):
    # Validate file size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "error": f"File too large. Maximum size is {MAX_UPLOAD_SIZE_MB}MB.",
            },
        )

    # Save file
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] if file.filename else ".pdf"
    safe_filename = f"{file_id}{ext}"
    filepath = os.path.join(UPLOAD_DIR, safe_filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    # Extract text
    resume_text = extract_text_from_file(filepath, ext)

    # Store in session (simplified — in production use Redis)
    session_data = {
        "file_id": file_id,
        "filename": file.filename,
        "resume_text": resume_text,
        "job_title": job_title,
        "company": company,
        "job_description": job_description,
    }

    # Store session data (using a simple dict for MVP)
    request.app.state.sessions = getattr(request.app.state, "sessions", {})
    request.app.state.sessions[file_id] = session_data

    return templates.TemplateResponse(
        "preview.html",
        {
            "request": request,
            "file_id": file_id,
            "resume_text": resume_text[:3000],
            "job_title": job_title,
            "company": company,
            "job_description": job_description[:500],
        },
    )


@router.post("/ats-check")
async def ats_check(
    request: Request,
    file: UploadFile = File(...),
):
    """Free ATS Score Checker - analyzes resume only, no payment needed"""
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        return templates.TemplateResponse(
            "ats_check.html",
            {"request": request, "error": f"File too large. Max {MAX_UPLOAD_SIZE_MB}MB."},
        )

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] if file.filename else ".pdf"
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

    with open(filepath, "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_file(filepath, ext)

    # AI Scoring
    from services.ai_optimizer import score_resume_ats
    score_data = await score_resume_ats(resume_text)

    return templates.TemplateResponse(
        "ats_result.html",
        {"request": request, "score_data": score_data, "resume_text": resume_text[:2000]},
    )