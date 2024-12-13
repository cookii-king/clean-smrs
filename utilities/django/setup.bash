python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd .. #must be out side django directory, so Clean SMRs/here, not Clean SMRs/django
django-admin startproject cleansmrs_system django
cd django
python3 manage.py runserver
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
# Username: admin
# Email address: admin@cleansmrs.com
# Password: 123456@Aa
python3 manage.py startapp accounts
python3 manage.py startapp cleansmrs_system
python3 manage.py startapp payments
python3 manage.py startapp shop
python3 manage.py spectacular --file schema.yaml
python3 manage.py spectacular --file schema.json