release: python manage.py migrate
release: python manage.py runserver
web: gunicorn --worker-tmp-dir /dev/shm ecommerce.wsgi