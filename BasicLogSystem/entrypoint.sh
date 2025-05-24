#!/bin/bash

# Collect static files
python manage.py collectstatic --no-input

# Make initial DB migration
python manage.py migrate --no-input

# Add a default super user
python manage.py createsuperuser --no-input --username root --email nothing@nothing.com || true