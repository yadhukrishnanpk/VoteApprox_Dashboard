"""
WSGI config for Election project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import subprocess
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Election.settings')

try:
    print("Docker Startup: Running database migrations...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)
    
    print("Docker Startup: Checking for superuser creation...")
    subprocess.run(["python", "createsuperuser.py"], check=True)
except Exception as e:
    print(f"Docker Startup Automation skipped/failed: {e}")

application = get_wsgi_application()
