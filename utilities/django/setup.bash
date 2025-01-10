python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
django-admin startproject system django
python3 manage.py startapp pages
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py spectacular --file schema.yaml
stripe login
stripe listen --forward-to localhost:8000/webhook
python manage.py collectstatic