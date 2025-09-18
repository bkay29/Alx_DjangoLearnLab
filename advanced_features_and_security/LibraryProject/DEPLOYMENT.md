# Deployment Guide for LibraryProject

This document explains how to deploy **LibraryProject** securely in both development and production environments.

---

## 1. Environment Variables

Before running in production, configure environment variables.
#Production mode is enabled when DJANGO_DEBUG=False:

```bash
# Security
export DJANGO_SECRET_KEY="replace-with-strong-secret-key"
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="localhost, 127.0.0.1, [::1]"


# Run security checks
python manage.py check --deploy

#Development mode
export DJANGO_DEBUG=True
python manage.py runserver


# Database (example: PostgreSQL via dj-database-url or settings.py)
export DATABASE_URL="postgres://user:password@host:5432/dbname"
