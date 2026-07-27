<div>

# Job Tracker

A production-ready Django application for tracking job applications through the hiring process.

</div>

## Overview

Job Tracker helps users manage job applications end to end — from creating and updating entries to tracking status changes. Built with Django and containerized with Docker, it demonstrates a modern backend stack: asynchronous task processing with Celery, PostgreSQL, Redis, Nginx, Gunicorn, and CI/CD deployment to AWS EC2.

<br>

## Features

**Authentication**
Registration, login/logout, email-based auth, password validation

**Job Management**
Create, edit, delete, and view applications · track status (Applied, Accepted, Rejected)

**Dashboard**
All applications in one place · success messages · responsive Bootstrap UI

**Background Tasks**
Celery workers · Redis broker · Celery Beat scheduling

**Validation**
Duplicate prevention · server-side form validation · custom model rules

<br>

## Stack

| Layer | Tools |
|---|---|
| Backend | Python, Django, Django ORM |
| Database | PostgreSQL |
| Task Queue | Celery, Redis, Celery Beat |
| Web Server | Gunicorn, Nginx |
| DevOps | Docker, Docker Compose, GitHub Actions, AWS EC2 |
| Frontend | HTML, CSS, Bootstrap |

<br>

## Architecture

**CI/CD**

```
push to main → GitHub Actions → SSH into EC2 → git pull → docker compose up -d --build
```

**Containers**

| Service | Role |
|---|---|
| `web` | Django + Gunicorn |
| `nginx` | Reverse proxy |
| `db` | PostgreSQL |
| `redis` | Message broker |
| `celery` | Background worker |
| `celery-beat` | Scheduled tasks |

<br>

## Getting Started

```bash
git clone https://github.com/<your-username>/jobtracker.git
cd jobtracker
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost
```

Run the stack:

```bash
docker compose up --build
```

Then visit `http://localhost`.

<br>

## Commands

```bash
# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic

# View logs
docker compose logs -f

# Stop containers
docker compose down
```

<br>

## Roadmap

- HTTPS with Let's Encrypt
- Kubernetes deployment
- Email follow-up reminders
- Dashboard analytics
- Resume upload support

<br>

## License

MIT