python3 --version
python3 -m venv .venv
source .venv/bin/activate
touch main.py
flask --app main.py run --debug
#windows python -m flask --app main.py run --debug


# to enable https
sudo apt-get update -y
sudo apt install tree -y
sudo apt install nginx -y
git clone https://github.com/cookii-king/clean-smrs.git
ls -lrt
cd clean-smrs
ls -lrt
sudo apt install python3 python3-venv python3-pip -y
python3 --version
python3 -m venv venv
ls -lrt
source venv/bin/activate
pip install -r requirements.txt

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
git pull origin main
