from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@router.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})


@router.get("/results/{file_id}", response_class=HTMLResponse)
async def results_page(request: Request, file_id: str):
    sessions = getattr(request.app.state, "sessions", {})
    session_data = sessions.get(file_id, {})
    if not session_data:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "Session not found."},
        )
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "file_id": file_id, "data": session_data},
    )


@router.get("/download/{file_id}/{format}", response_class=HTMLResponse)
async def download_file(request: Request, file_id: str, format: str):
    from fastapi.responses import FileResponse
    sessions = getattr(request.app.state, "sessions", {})
    session_data = sessions.get(file_id, {})
    if not session_data:
        return HTMLResponse("Not found", status_code=404)

    path = (
        session_data.get("docx_path")
        if format == "docx"
        else session_data.get("pdf_path")
    )
    if not path or not __import__("os").path.exists(path):
        return HTMLResponse("File not ready", status_code=404)

    filename = f"optimized_resume.{format}"
    return FileResponse(path, filename=filename, media_type="application/octet-stream")