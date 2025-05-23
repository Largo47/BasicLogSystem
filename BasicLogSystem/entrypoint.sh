#!/bin/bash

# Collect static files if needed
python manage.py collectstatic --no-input

# Migrate DB if changes needed
python manage.py migrate --no-input
