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

# aws commands
sudo apt-get update -y
git clone https://github.com/cookii-king/clean-smrs.git
ls -lrt
# total 4
# drwxrwxr-x 8 ubuntu ubuntu 4096 Jan  5 21:50 clean-smrs
cd clean-smrs
ls -lrt
# total 24
# -rw-rw-r-- 1 ubuntu ubuntu 4167 Jan  5 21:50 README.md
# drwxrwxr-x 6 ubuntu ubuntu 4096 Jan  5 21:50 django
# drwxrwxr-x 6 ubuntu ubuntu 4096 Jan  5 21:50 flask
# drwxrwxr-x 4 ubuntu ubuntu 4096 Jan  5 21:50 utilities
# -rw-rw-r-- 1 ubuntu ubuntu  200 Jan  5 21:50 requirements.txt
# sudo apt install python3-pip -y
sudo apt install python3 python3-venv python3-pip -y
# pip install django
python3 --version
# python3 -m venv .venv
python3 -m venv venv
# source .venv/bin/activate
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
# python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com
# Username: admin
# Email address: admin@cleansmrs.com
# Password: 123456@Aa
python3 manage.py runserver 0.0.0.0:8000
python manage.py collectstatic


# to enable https
sudo apt install tree -y
sudo apt install nginx -y
sudo apt-get install supervisor
cd /etc/supervisor/conf.d/
sudo touch gunicorn.conf
sudo nano gunicorn.conf
sudo mkdir /var/log/gunicorn
sudo supervisorctl reread
# guni: available
sudo supervisorctl update
# guni: added process group
sudo supervisorctl status
# guni:gunicorn                    RUNNING   pid 18950, uptime 0:00:33
sudo nano nginx.conf
cd sites-available
sudo touch django.conf
sudo nano django.conf
sudo nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
sudo ln django.conf /etc/nginx/sites-enabled
sudo service nginx restart
sudo apt-get install certbot -y
sudo apt-get install python3-certbot-nginx -y
# we can't use the servers public ip address to generate the ssl certificate with certbot we need a domain name like (cleansmrs.com, or cleansmrs.org)...
# sudo certbot --nginx -d 35.165.93.124 --config /etc/nginx/sites-available/django.conf
# sudo certbot --nginx -d cleansmrs.com --config /etc/nginx/sites-available/django.conf
