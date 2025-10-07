# Task Management System

## Create Virtual environment and activate it
- python -m venv venv
- venv/scripts/activate

## Clone git repository
git clone https://github.com/AKSHAY-KR99/lbs.git 

## Install requirements
pip install -r requirements.txt

## Apply Migrations
- python manage.py migrate
- python manage.py migrate django_celery_beat

## Create super admin
python manage.py createsuperuser

## Run Server
- python manage.py runserver
- run redis server on port 6380
- on another terminal run celery worker using the command: celery -A library_management_system worker --loglevel=info -P solo
- Another terminal run celery beat: celery -A library_management_system beat --loglevel=info

## server running on http://127.0.0.1:8000/

Postman collection attached with mail and git repository