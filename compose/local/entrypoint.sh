#!/usr/bin/env bash
set -e

python manage.py makemigrations rental --noinput || true
python manage.py migrate --noinput

python - <<'PY'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created:", username)
else:
    print("Superuser exists:", username)
PY

python manage.py runserver 0.0.0.0:8000
