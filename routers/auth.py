from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from core.config import settings
from core.logger import logger
from core.templates import templates

router = APIRouter()


@router.get("/login")
def login_page(request: Request, error: str = None):
    """Render the login page with optional error message."""
    return templates.TemplateResponse(request, "login.html", {"error": error})


@router.post("/login")
async def login_process(request: Request):
    """Validate credentials and set admin session cookie with security logging."""
    client_ip = request.client.host if request.client else "Unknown"
    try:
        form = await request.form()
        username = (form.get("username") or "").strip()
        password = (form.get("password") or "").strip()

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            logger.info(f"Successful admin login for user '{username}' from IP: {client_ip}")
            resp = RedirectResponse(url="/admin", status_code=303)
            resp.set_cookie(
                key="admin_session",
                value=settings.ADMIN_USERNAME,
                httponly=True,
                max_age=86400,
            )
            return resp

        logger.warning(f"Failed admin login attempt for username '{username}' from IP: {client_ip}")
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Invalid credentials"},
        )
    except Exception as exc:
        logger.error(f"Error processing login request from IP {client_ip}: {exc}", exc_info=True)
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "An error occurred during authentication. Please try again."},
        )


@router.get("/logout")
def logout(request: Request):
    """Clear admin session and redirect home."""
    client_ip = request.client.host if request.client else "Unknown"
    logger.info(f"Admin logout requested from IP: {client_ip}")
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie(key="admin_session")
    return resp
