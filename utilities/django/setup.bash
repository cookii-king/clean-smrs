#!/bin/bash

# Check Python version
echo "Checking Python version..."
python3 --version

# Set up a virtual environment
echo "Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Navigate to the project root directory
cd ..

# Create Django project and app if they don't exist
if [ ! -d "django" ]; then
    echo "Creating Django project..."
    mkdir django
    django-admin startproject system django
    cd django
    python3 manage.py startapp pages
else
    cd django
fi

# Apply migrations
echo "Applying migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Run the Django development server
echo "Running Django development server..."
python3 manage.py runserver 0.0.0.0:8000

# Create a superuser
echo "Creating superuser..."
python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com

# Generate API schema
echo "Generating API schema..."
python3 manage.py spectacular --file schema.yaml

# Stripe setup (requires Stripe CLI)
echo "Setting up Stripe..."
stripe login
stripe listen --forward-to localhost:8000/webhook
stripe trigger customer.created

# Update package lists and install necessary packages
echo "Updating package lists and installing necessary packages..."
sudo apt-get update -y
sudo apt install python3 python3-venv python3-pip -y
sudo apt install tree -y
sudo apt install nginx -y
sudo apt-get install supervisor -y

# Clone the repository if not already cloned
if [ ! -d "clean-smrs" ]; then
    echo "Cloning the repository..."
    git clone https://github.com/cookii-king/clean-smrs.git
fi

# Navigate to the project directory
cd clean-smrs

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Apply migrations
echo "Applying migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser
echo "Creating superuser..."
python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Configure Supervisor for Gunicorn
echo "Configuring Supervisor for Gunicorn..."
sudo touch /etc/supervisor/conf.d/gunicorn.conf
sudo nano /etc/supervisor/conf.d/gunicorn.conf

# Create log directory for Gunicorn
sudo mkdir -p /var/log/gunicorn

# Reload Supervisor configuration
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status

# Configure Nginx
echo "Configuring Nginx..."
sudo nano /etc/nginx/nginx.conf
cd /etc/nginx/sites-available
sudo touch django.conf
sudo nano django.conf

# Test Nginx configuration
sudo nginx -t

# Enable the Nginx site configuration
sudo ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled

# Restart Nginx
sudo service nginx restart

# Install Certbot for SSL
echo "Installing Certbot for SSL..."
sudo apt-get install certbot -y
sudo apt-get install python3-certbot-nginx -y

# Note: SSL certificate generation requires a domain name
# sudo certbot --nginx -d yourdomain.com --config /etc/nginx/sites-available/django.conf

# Reset and update the repository
echo "Resetting and updating the repository..."
git reset --hard HEAD
git clean -fd
git pull origin main

# Restart services
echo "Restarting services..."
sudo supervisorctl restart guni:gunicorn
sudo supervisorctl status
sudo systemctl restart nginx

gunicorn -w 4 -b 0.0.0.0:8000 system.wsgi:application