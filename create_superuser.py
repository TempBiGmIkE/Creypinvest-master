#!/usr/bin/env python
"""
Helper script to create a superuser for local development.
Run this after activating the virtual environment and unsetting DATABASE_URL.
"""
import os
import django

# Ensure we use SQLite, not remote DB
os.environ.setdefault('DATABASE_URL', '')
os.environ['DJANGO_SETTINGS_MODULE'] = 'creyp.settings'

django.setup()

from django.contrib.auth.models import User

username = 'jordan'
email = 'statewarrior@gmail.com'
password = 'Password123!'

if User.objects.filter(username=username).exists():
    print(f"✅ Superuser '{username}' already exists.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
