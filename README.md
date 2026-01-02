# Script Orbit (Django) — Showcase Build

This repository is a **sanitized review pack** of the Script Orbit website backend, built with **Django**.

## What it demonstrates
- Portfolio + project pages (Projects, Categories, Images)
- Blog content (slugged posts, rich text via CKEditor)
- Careers / Jobs (Job categories + applications)
- Authenticated preview flow for client template previews
- Django Admin customizations for content management
- SEO basics (meta fields, sitemaps, robots.txt)

## Tech
- Django (templates + admin)
- SQLite for local development (optional Postgres via env vars)
- django-ckeditor (rich text + uploads)
- django-cors-headers (optional; keep disabled unless you add an API)

## Local setup

1) Create a virtualenv and install deps:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Configure environment variables:
- Copy `.env.example` → `.env`
- Set `DJANGO_SECRET_KEY`

3) Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Notes on security
- Secrets are loaded from `.env` (never commit real credentials)
- `DEBUG`, `ALLOWED_HOSTS`, and `X_FRAME_OPTIONS` are env-driven for safer defaults
