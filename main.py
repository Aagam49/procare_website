from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from core.logger import logger
from core.templates import templates
from database import init_db
from routers import admin, auth, public

# Initialize database schema safely
try:
    logger.info("Initializing database tables...")
    init_db()
    logger.info("Database initialized successfully.")
except Exception as exc:
    logger.critical(f"Critical error initializing database: {exc}", exc_info=True)
    raise exc

# Application setup
app = FastAPI(title="ProCare Physiotherapy", version="1.0.0")

# Static files mounting
app.mount("/static", StaticFiles(directory="static"), name="static")

# Router registration
app.include_router(public.router)
app.include_router(auth.router)
app.include_router(admin.router)


# Global Exception Handlers (Security Hardening & Graceful Error Recovery)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle custom HTTP exceptions cleanly."""
    if exc.status_code == status.HTTP_303_SEE_OTHER:
        headers = dict(exc.headers) if exc.headers else {}
        return Response(status_code=exc.status_code, headers=headers)

    logger.warning(f"HTTPException [{exc.status_code}] on path '{request.url.path}': {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def global_unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all unhandled exception handler (OWASP Information Disclosure Protection)."""
    logger.error(f"Unhandled 500 Exception on path '{request.url.path}': {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )
