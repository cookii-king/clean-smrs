#!/bin/bash

# Check Python version
echo "Checking Python version..."
python3 --version

# Set up a virtual environment for Flask
echo "Setting up virtual environment for Flask..."
python3 -m venv .venv
source .venv/bin/activate

# Create a main.py file if it doesn't exist
if [ ! -f main.py ]; then
    touch main.py
fi

# Run Flask in debug mode (for development only)
echo "Running Flask in debug mode..."
flask --app main.py run --debug

# Update package lists and install necessary packages
echo "Updating package lists and installing necessary packages..."
sudo apt-get update -y
sudo apt install tree -y
sudo apt install nginx -y

# Clone the repository
echo "Cloning the repository..."
git clone https://github.com/cookii-king/clean-smrs.git

# Navigate to the project directory
cd clean-smrs

# Install Python and virtual environment for Django
echo "Installing Python and setting up virtual environment for Django..."
sudo apt install python3 python3-venv python3-pip -y
python3 --version
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# Install and configure Supervisor for process management
echo "Installing Supervisor..."
sudo apt-get install supervisor -y

# Create and edit Gunicorn configuration
echo "Configuring Gunicorn with Supervisor..."
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

# Pull the latest changes from the repository
echo "Pulling latest changes from the repository..."
git pull origin main

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn -w 4 -b 0.0.0.0:8000 main:app

sudo chmod +x /home/ubuntu/clean-smrs/utilities/server/setup.bash
sudo bash /home/ubuntu/clean-smrs/utilities/server/setup.bash

flask --app main.py run --debug