#!/usr/bin/env bash
set -euo pipefail

# Run database migrations and collect static files, then start Gunicorn.
# This allows Render to apply migrations automatically during deployment
# (useful when Render Shell is unavailable).

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn with the PORT provided by Render (default to 10000)
exec gunicorn Auto_Insurance_Claims_Fraud_Detection.wsgi:application --bind 0.0.0.0:${PORT:-10000}
