# Social Media API - Deployment Guide

This guide covers deploying the Social Media API to production environments.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Variables](#environment-variables)
3. [Heroku Deployment](#heroku-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
6. [Docker Deployment](#docker-deployment)
7. [Database Setup](#database-setup)
8. [Static Files](#static-files)
9. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Pre-Deployment Checklist

Before deploying, ensure you have completed these steps:

- [ ] Set `DEBUG=False` in production
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Configure static file serving
- [ ] Set up HTTPS/SSL
- [ ] Review security settings
- [ ] Run `python manage.py check --deploy`

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgres://user:password@host:5432/dbname

# Optional
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
SECURE_SSL_REDIRECT=True
```

### Generate a Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git repository initialized

### Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=".herokuapp.com"
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create Superuser (Optional)**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Open App**
   ```bash
   heroku open
   ```

---

## DigitalOcean Deployment

### Using App Platform

1. Connect your GitHub repository
2. Configure build settings:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command: `gunicorn social_media_api.wsgi`
3. Add environment variables
4. Deploy

### Using Droplet

1. **Create Ubuntu Droplet**

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/your-repo/social_media_api.git
   cd social_media_api
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location /static/ {
           alias /path/to/social_media_api/staticfiles/;
       }

       location /media/ {
           alias /path/to/social_media_api/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **Create Systemd Service**
   ```ini
   # /etc/systemd/system/social_media_api.service
   [Unit]
   Description=Social Media API
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/social_media_api
   ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 social_media_api.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl enable social_media_api
   sudo systemctl start social_media_api
   sudo systemctl restart nginx
   ```

---

## AWS Elastic Beanstalk

### Using EB CLI

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize**
   ```bash
   eb init -p python-3.11 social-media-api
   ```

3. **Create Environment**
   ```bash
   eb create production
   ```

4. **Configure Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your-key DEBUG=False
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_media_api.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - DATABASE_URL=postgres://postgres:postgres@db:5432/social_media_api
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=social_media_api
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

### Build and Run

```bash
docker-compose up --build
```

---

## Database Setup

### PostgreSQL (Recommended)

1. **Install PostgreSQL**
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create Database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE social_media_api;
   CREATE USER apiuser WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE social_media_api TO apiuser;
   ```

3. **Set DATABASE_URL**
   ```bash
   DATABASE_URL=postgres://apiuser:your_password@localhost:5432/social_media_api
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

---

## Static Files

### Collect Static Files

```bash
python manage.py collectstatic
```

### Using WhiteNoise (Included)

WhiteNoise is already configured in settings.py to serve static files efficiently.

### Using AWS S3 (Optional)

1. Install boto3: `pip install boto3 django-storages`
2. Add to settings.py:
   ```python
   AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_REGION_NAME = 'us-east-1'
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
   ```

---

## Monitoring & Maintenance

### Health Check Endpoint

Add to your URLs:
```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

### Logging

Logs are configured to output to console and file. Check:
- Console output (in production logs)
- `logs/django.log` (local file)

### Regular Maintenance Tasks

1. **Database Backups**
   ```bash
   # Heroku
   heroku pg:backups:capture
   
   # Local PostgreSQL
   pg_dump social_media_api > backup.sql
   ```

2. **Update Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   python manage.py migrate
   ```

3. **Monitor Performance**
   - Use tools like New Relic, Sentry, or Datadog
   - Set up alerts for errors and performance issues

4. **Security Updates**
   - Regularly update Django and dependencies
   - Run `python manage.py check --deploy` periodically

---

## Troubleshooting

### Common Issues

1. **500 Error in Production**
   - Check DEBUG is False
   - Verify ALLOWED_HOSTS includes your domain
   - Check logs for specific errors

2. **Static Files Not Loading**
   - Run `collectstatic`
   - Verify WhiteNoise is in MIDDLEWARE
   - Check STATIC_ROOT path

3. **Database Connection Failed**
   - Verify DATABASE_URL format
   - Check database server is running
   - Verify credentials

4. **CORS Errors**
   - Add frontend domain to CORS_ALLOWED_ORIGINS
   - Check CORS_ALLOW_CREDENTIALS setting

---

## Live URL

After deployment, your API will be available at:
- Heroku: `https://your-app-name.herokuapp.com/api/`
- Custom Domain: `https://yourdomain.com/api/`

### Test Deployment

```bash
curl https://your-app-url/api/posts/
```
