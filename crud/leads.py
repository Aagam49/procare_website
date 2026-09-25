from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.logger import logger
from database import LeadSubmission


def create_lead(
    db: Session,
    full_name: str,
    phone: str,
    email: str,
    preferred_date: str,
    service: str,
    symptoms: str,
    source: str = "homepage",
) -> LeadSubmission:
    """Create lead submission with exception handling & transaction safety."""
    submission = LeadSubmission(
        full_name=full_name,
        phone=phone,
        email=email,
        preferred_date=preferred_date,
        service=service,
        symptoms=symptoms,
        source=source,
    )
    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)
        logger.info(f"Successfully created lead submission ID #{submission.id} for '{full_name}'")
        return submission
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error(f"Database error while saving lead submission for '{full_name}': {exc}", exc_info=True)
        raise exc


def get_all_leads(db: Session) -> list[LeadSubmission]:
    """Retrieve all lead submissions ordered by creation timestamp."""
    try:
        return db.query(LeadSubmission).order_by(LeadSubmission.created_at.desc()).all()
    except SQLAlchemyError as exc:
        logger.error(f"Database error while querying lead submissions: {exc}", exc_info=True)
        return []
