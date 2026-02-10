import os
import sys
from pathlib import Path

# Add the parent directory to the path so Django can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creyp.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Get the Django WSGI application
application = get_wsgi_application()
