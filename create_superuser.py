import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Election.settings')
django.setup()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'yadhu@example.com', '3032')
    print("✅ Superuser created!")
else:
    print("✅ Superuser already exists!")