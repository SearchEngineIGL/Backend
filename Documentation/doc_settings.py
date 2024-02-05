
import os
import sys

# Add the path to your Django project
sys.path.insert(0, os.path.abspath('E:/Backend'))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'  # Replace 'your_project.settings' with the actual settings module

# Initialize Django
import django
django.setup()
