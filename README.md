# ProCare Physiotherapy Website

A FastAPI-based marketing website for ProCare Physiotherapy in Naranpura, Ahmedabad.

## Getting started locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   . .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Copy the sample environment file and update SMTP values if needed:
   ```bash
   copy .env.example .env
   ```
3. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
4. Open http://127.0.0.1:8000

## Environment variables

The app reads values from `.env`. Update the following before using email notifications:

- `CLINIC_EMAIL`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`

## Deployment to Render

1. Push this project to a GitHub repo.
2. In Render, create a new Web Service and connect the repository.
3. Use the included `render.yaml` file.
4. Set environment variables in the Render dashboard if needed.
5. Deploy.

## Notes

- The site uses SQLite in the project root as `procare.db`.
- Page content uses placeholder clinic details where exact personal information was not supplied by the client brief.
- Email sending is skipped gracefully if the SMTP values are not configured.
