from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.logger import logger
from database import ContactSubmission


def create_contact(
    db: Session,
    full_name: str,
    email: str,
    phone: str | None,
    subject: str,
    message: str,
) -> ContactSubmission:
    """Create contact submission with exception handling & transaction safety."""
    submission = ContactSubmission(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )
    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)
        logger.info(f"Successfully created contact submission ID #{submission.id} from '{full_name}'")
        return submission
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error(f"Database error while saving contact message from '{full_name}': {exc}", exc_info=True)
        raise exc


def get_all_contacts(db: Session) -> list[ContactSubmission]:
    """Retrieve all contact submissions ordered by creation timestamp."""
    try:
        return db.query(ContactSubmission).order_by(ContactSubmission.created_at.desc()).all()
    except SQLAlchemyError as exc:
        logger.error(f"Database error while querying contact messages: {exc}", exc_info=True)
        return []
