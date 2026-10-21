import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME")
password = os.environ.get("ADMIN_PASSWORD")
email = os.environ.get("ADMIN_EMAIL", "")

if not username or not password:
    raise RuntimeError("Admin credentials are missing")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print("Superuser created successfully")
else:
    print("This username already exists")
