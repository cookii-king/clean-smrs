# step 1
sudo apt-get update -y
# sudo apt-get upgrade -y
sudo apt install python3 python3-venv python3-pip -y
sudo apt install tree nginx supervisor -y

# step 2
echo "http://$(curl -s ifconfig.me)"

# step 3
# Clone the repository if not already cloned
if [ ! -d "clean-smrs" ]; then
    echo "Cloning the repository..."
    git clone https://github.com/cookii-king/clean-smrs.git
fi

# step 4
cd clean-smrs
python3 --version
python3 -m venv venv
source venv/bin/activate
# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

# step 5
cd django
# Apply migrations
echo "Applying migrations in Django..."
python3 manage.py makemigrations
python3 manage.py migrate


# step 6
# Create a superuser
echo "Creating superuser..."
# python3 manage.py createsuperuser --username admin --email admin@cleansmrs.com
# Username: admin
# Email address: admin@cleansmrs.com
# Password: 123456@Aa
python3 manage.py create_superuser_if_none
# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 7
# Define the source and destination paths
gunicorn_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/gunicorn.conf"
gunicorn_server_conf_setup="/etc/supervisor/conf.d/gunicorn.conf"
nginx_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/nginx.conf"
nginx_server_conf_setup="/etc/nginx/nginx.conf"
django_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/django.conf"
django_server_conf_setup="/etc/nginx/sites-available/django.conf"
env_file="/home/ubuntu/clean-smrs/django/.env"

# Copy Gunicorn configuration
echo "Copying Gunicorn configuration file..."
sudo cp "$gunicorn_utilities_conf_setup" "$gunicorn_server_conf_setup" || { echo "Failed to copy Gunicorn configuration"; exit 1; }

# Create log directory for Gunicorn
sudo mkdir -p /var/log/gunicorn

# Update and copy Nginx configuration
echo "Updating user directive in nginx.conf to run as root..."
sed -i "s/^user .*/user root;/" "$nginx_utilities_conf_setup"
sudo cp "$nginx_utilities_conf_setup" "$nginx_server_conf_setup" || { echo "Failed to copy Nginx configuration"; exit 1; }

# Define the current and new IP addresses
current_ip="35.165.93.124"
new_ip="$(curl -s ifconfig.me)"

# Replace the IP address in the django.conf file
echo "Updating IP address in django.conf..."
sed -i "s/$current_ip/$new_ip/g" "$django_utilities_conf_setup"
sudo cp "$django_utilities_conf_setup" "$django_server_conf_setup" || { echo "Failed to copy Django configuration"; exit 1; }

# Update DJANGO_URL and DJANGO_SERVER_IP in the .env file
echo "Updating DJANGO_URL and DJANGO_SERVER_IP in .env..."
sed -i "s|DJANGO_URL=http://$current_ip|DJANGO_URL=http://$new_ip|g" "$env_file"
sed -i "s|DJANGO_SERVER_IP=$current_ip|DJANGO_SERVER_IP=$new_ip|g" "$env_file"

# Enable the Nginx site configuration
sudo ln -sf /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled

# Test Nginx configuration
sudo nginx -t || { echo "Nginx configuration test failed"; exit 1; }

# Restart Nginx
echo "Restarting Nginx..."
sudo service nginx restart || { echo "Failed to restart Nginx"; exit 1; }

# Reload Supervisor configuration
echo "Reloading Supervisor..."
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
sudo supervisorctl restart guni:gunicorn
sudo supervisorctl status
sudo service nginx restart

