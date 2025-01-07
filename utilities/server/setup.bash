# step 1
sudo apt-get update -y
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
python3 manage.py create_superuser_if_none
# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# step 7
# Define the source and destination paths
gunicorn_utilities_conf_setup="utilities/django/gunicorn.conf"
gunicorn_server_conf_setup="/etc/supervisor/conf.d/gunicorn.conf"
echo "Copying configuration files from utilities..."
sudo cp "$gunicorn_utilities_conf_setup" "$gunicorn_server_conf_setup"
# sudo nano /etc/supervisor/conf.d/gunicorn.conf

# step 8
# Define the source and destination paths
gunicorn_utilities_conf_setup="utilities/django/gunicorn.conf"
gunicorn_server_conf_setup="/etc/supervisor/conf.d/gunicorn.conf"
echo "Copying configuration files from utilities..."
sudo cp "$gunicorn_utilities_conf_setup" "$gunicorn_server_conf_setup"
# Create log directory for Gunicorn
sudo mkdir -p /var/log/gunicorn
nginx_utilities_conf_setup="utilities/django/nginx.conf"
nginx_server_conf_setup="/etc/nginx/nginx.conf"
echo "Updating user directive in nginx.conf to run as root..."
sed -i "s/^user .*/user root;/" "$nginx_utilities_conf_setup"
sudo cp "$nginx_utilities_conf_setup" "$nginx_server_conf_setup"

django_utilities_conf_setup="utilities/django/django.conf"
django_server_conf_setup="/etc/nginx/sites-available/django.conf"
# Define the current and new IP addresses
current_ip="35.165.93.124"
new_ip="$(curl -s ifconfig.me)"  # Replace with the actual new IP address
# Replace the IP address in the configuration file
echo "Updating IP address in django.conf..."
sed -i "s/$current_ip/$new_ip/g" "$django_utilities_conf_setup"

sudo cp "$django_utilities_conf_setup" "$django_server_conf_setup"
# Enable the Nginx site configuration
sudo ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled
sudo nginx -t
# Restart Nginx
sudo service nginx restart
# Reload Supervisor configuration
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status

