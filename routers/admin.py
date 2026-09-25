import csv
import io

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session

from core.logger import logger
from core.security import get_current_admin_cookie
from core.templates import templates
from crud.contacts import get_all_contacts
from crud.leads import get_all_leads
from database import get_db
from services.content_service import clinic_details

router = APIRouter()


@router.get("/admin", response_class=Response)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_admin_cookie),
):
    try:
        logger.info(f"Admin dashboard accessed by '{username}'")
        leads = get_all_leads(db)
        contacts = get_all_contacts(db)
        return templates.TemplateResponse(
            request,
            "admin_dashboard.html",
            {
                "leads": leads,
                "contacts": contacts,
                "clinic": clinic_details(),
            },
        )
    except Exception as exc:
        logger.error(f"Error rendering admin dashboard for '{username}': {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load admin dashboard.",
        )


@router.get("/admin/export")
def export_leads_csv(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_admin_cookie),
):
    try:
        logger.info(f"Leads CSV export initiated by admin user '{username}'")
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "id",
            "full_name",
            "phone",
            "email",
            "preferred_date",
            "service",
            "symptoms",
            "created_at",
        ])
        leads = get_all_leads(db)
        for lead in leads:
            writer.writerow([
                lead.id,
                lead.full_name,
                lead.phone,
                lead.email,
                lead.preferred_date,
                lead.service,
                lead.symptoms,
                lead.created_at.isoformat() if lead.created_at else "",
            ])
        logger.info(f"Exported {len(leads)} leads to CSV for '{username}'")
        response = StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
        )
        response.headers["Content-Disposition"] = "attachment; filename=leads.csv"
        return response
    except Exception as exc:
        logger.error(f"Error exporting leads CSV for '{username}': {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate CSV export.",
        )
