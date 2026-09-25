from fastapi import HTTPException, Request, status
from core.config import settings


def get_current_admin_cookie(request: Request) -> str:
    """Validate admin session cookie.
    Redirects to /login if not authenticated.
    """
    cookie = request.cookies.get("admin_session")
    if cookie != settings.ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )
    return settings.ADMIN_USERNAME
