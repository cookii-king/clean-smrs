python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd .. #must be out side django directory, so Clean SMRs/here, not Clean SMRs/django
mkdir django
django-admin startproject system django
cd django
python3 manage.py startapp pages
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

python3 manage.py createsuperuser
# python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com
# Username: admin
# Email address: admin@cleansmrs.com
# Password: 123456@Aa
python3 manage.py spectacular --file schema.yaml
# python3 manage.py spectacular --file schema.json

stripe login
stripe listen --forward-to localhost:8000/webhook
stripe trigger customer.created
