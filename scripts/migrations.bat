cd ../backend/django

call venv/scripts/activate

python manage.py makemigrations
python manage.py migrate

cmd