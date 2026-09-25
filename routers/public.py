from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from core.logger import logger
from core.templates import templates
from crud.contacts import create_contact
from crud.leads import create_lead
from database import get_db
from services.content_service import (
    clinic_details,
    process_steps,
    service_catalog,
    stat_cards,
    testimonials,
)
from services.email_service import send_email_notification

router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "services": service_catalog(),
            "stats": stat_cards(),
            "testimonials": testimonials(),
            "process": process_steps(),
            "clinic": clinic_details(),
        },
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html",
        {
            "clinic": clinic_details(),
        },
    )


@router.get("/services")
def services_page(request: Request):
    return templates.TemplateResponse(
        request,
        "services.html",
        {
            "services": service_catalog(),
            "clinic": clinic_details(),
        },
    )


@router.get("/testimonials")
def testimonials_page(request: Request):
    return templates.TemplateResponse(
        request,
        "testimonials.html",
        {
            "testimonials": testimonials(),
            "clinic": clinic_details(),
        },
    )


@router.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(
        request,
        "contact.html",
        {
            "clinic": clinic_details(),
            "services": service_catalog(),
        },
    )


@router.post("/submit-lead")
async def submit_lead(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "Unknown"
    try:
        form = await request.form()
        full_name = (form.get("full_name") or "").strip()
        phone = (form.get("phone") or "").strip()
        email = (form.get("email") or "").strip()
        preferred_date = (form.get("preferred_date") or "").strip()
        service = (form.get("service") or "").strip()
        symptoms = (form.get("symptoms") or "").strip()

        if not all([full_name, phone, email, preferred_date, service, symptoms]):
            logger.warning(f"Incomplete appointment lead submission attempt from IP {client_ip}")
            return RedirectResponse(
                url=f"/?error={quote('Please complete all appointment fields.')}",
                status_code=303,
            )

        create_lead(
            db=db,
            full_name=full_name,
            phone=phone,
            email=email,
            preferred_date=preferred_date,
            service=service,
            symptoms=symptoms,
            source="homepage",
        )

        message = (
            "New appointment enquiry from ProCare Physiotherapy\n\n"
            f"Name: {full_name}\nPhone: {phone}\nEmail: {email}\n"
            f"Preferred date: {preferred_date}\nService: {service}\n\n"
            f"Symptoms: {symptoms}"
        )

        send_email_notification("New Appointment Enquiry - ProCare Physiotherapy", message)

        logger.info(f"Lead submission completed for '{full_name}' ({email}) from IP {client_ip}")
        return RedirectResponse(
            url=f"/?success={quote('Thank you! Your appointment request has been received. Our team will contact you soon.')}",
            status_code=303,
        )
    except Exception as exc:
        logger.error(f"Failed to process lead submission from IP {client_ip}: {exc}", exc_info=True)
        return RedirectResponse(
            url=f"/?error={quote('An unexpected error occurred while processing your request. Please try again.')}",
            status_code=303,
        )


@router.post("/submit-contact")
async def submit_contact(request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "Unknown"
    try:
        form = await request.form()
        full_name = (form.get("full_name") or "").strip()
        email = (form.get("email") or "").strip()
        phone = (form.get("phone") or "").strip()
        subject = (form.get("subject") or "").strip()
        message = (form.get("message") or "").strip()

        if not all([full_name, email, subject, message]):
            logger.warning(f"Incomplete contact submission attempt from IP {client_ip}")
            return RedirectResponse(
                url=f"/contact?error={quote('Please complete all fields to send your message.')}",
                status_code=303,
            )

        create_contact(
            db=db,
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        email_message = (
            "New contact message from the ProCare website\n\n"
            f"Name: {full_name}\nEmail: {email}\nPhone: {phone or 'Not provided'}\n"
            f"Subject: {subject}\n\nMessage: {message}"
        )
        send_email_notification("Website Contact Message - ProCare Physiotherapy", email_message)

        logger.info(f"Contact submission completed for '{full_name}' ({email}) from IP {client_ip}")
        return RedirectResponse(
            url=f"/contact?success={quote('Your message has been sent successfully. We will get back to you soon.')}",
            status_code=303,
        )
    except Exception as exc:
        logger.error(f"Failed to process contact submission from IP {client_ip}: {exc}", exc_info=True)
        return RedirectResponse(
            url=f"/contact?error={quote('An unexpected error occurred while processing your message. Please try again.')}",
            status_code=303,
        )


@router.get("/robots.txt")
def robots(request: Request) -> Response:
    base = str(request.base_url).rstrip("/")
    return Response(
        content=f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n",
        media_type="text/plain",
    )


@router.get("/sitemap.xml")
def sitemap(request: Request) -> Response:
    base = str(request.base_url).rstrip("/")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{base}/</loc></url>
  <url><loc>{base}/about</loc></url>
  <url><loc>{base}/services</loc></url>
  <url><loc>{base}/testimonials</loc></url>
  <url><loc>{base}/contact</loc></url>
</urlset>
"""
    return Response(content=xml, media_type="application/xml")
