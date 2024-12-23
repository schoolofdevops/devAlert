#!/bin/sh

set -e

echo "Current directory: $(pwd)"
echo "Listing current directory:"
ls -la

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput -v 2

echo "Checking static files after collection:"
ls -la staticfiles/

echo "Content of staticfiles/rest_framework:"
ls -la staticfiles/rest_framework/

# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
