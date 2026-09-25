from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_page_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_about_page_returns_200():
    response = client.get("/about")
    assert response.status_code == 200


def test_services_page_returns_200():
    response = client.get("/services")
    assert response.status_code == 200


def test_testimonials_page_returns_200():
    response = client.get("/testimonials")
    assert response.status_code == 200


def test_contact_page_returns_200():
    response = client.get("/contact")
    assert response.status_code == 200


def test_home_form_submission_succeeds():
    response = client.post(
        "/submit-lead",
        data={
            "full_name": "Anika Patel",
            "phone": "+91 98765 43210",
            "email": "anika@example.com",
            "preferred_date": "2026-09-15",
            "service": "Manual Therapy",
            "symptoms": "Lower back pain after lifting and sitting for long hours.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Thank you" in response.text or "appointment request" in response.text.lower()


def test_contact_form_submission_succeeds():
    response = client.post(
        "/submit-contact",
        data={
            "full_name": "Harsh Mehta",
            "email": "harsh@example.com",
            "phone": "+91 99887 76655",
            "subject": "Query about knee rehab",
            "message": "I am interested in physiotherapy for recurring knee pain.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "message has been sent successfully" in response.text.lower()


def test_login_invalid_credentials_handled_gracefully():
    response = client.post(
        "/login",
        data={"username": "wrong_user", "password": "wrong_password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Invalid credentials" in response.text


def test_incomplete_lead_submission_returns_error_message():
    response = client.post(
        "/submit-lead",
        data={
            "full_name": "Incomplete User",
            # Missing phone, email, preferred_date, service, symptoms
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Please complete all appointment fields" in response.text
