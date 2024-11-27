python3 --version
python3 -m venv main_env
source main_env/bin/activate
pip3 install django
pip3 install 
# django-admin startproject cleansmrs
cd .. #must be out side django directory, so Clean SMRs/here, not Clean SMRs/django
django-admin startproject cleansmrs django
cd django
python3 manage.py runserver
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
# Username: admin
# Email address: admin@cleansmrs.com
# Password: 123456@Aa
python3 manage.py startapp catalog
pip3 install drf-spectacular
python3 manage.py spectacular --file schema.yml