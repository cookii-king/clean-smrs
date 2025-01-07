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

# step 7
# Choose between Django and Flask
echo "Choose the application to configure:"
echo "1) Django"
echo "2) Flask"
read -p "Enter the number of your choice: " choice

# Step 7: Use the argument to choose between Django and Flask
choice=$1

if [ "$choice" -eq 1 ]; then
    # Django Configuration
    echo "Configuring Django..."
    # Define the source and destination paths for Django
    django_gunicorn_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/gunicorn.conf"
    django_gunicorn_server_conf_setup="/etc/supervisor/conf.d/gunicorn.conf"
    django_nginx_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/nginx.conf"
    django_nginx_server_conf_setup="/etc/nginx/nginx.conf"
    django_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/django/django.conf"
    django_server_conf_setup="/etc/nginx/sites-available/django.conf"
    django_env_file="/home/ubuntu/clean-smrs/django/.env"
    # Copy Gunicorn configuration
    echo "Copying Gunicorn configuration file..."
    sudo cp "$django_gunicorn_utilities_conf_setup" "$django_gunicorn_server_conf_setup" || { echo "Failed to copy Gunicorn configuration"; exit 1; }
    # Create log directory for Gunicorn
    sudo mkdir -p /var/log/gunicorn
    # Update and copy Nginx configuration
    echo "Updating user directive in nginx.conf to run as root..."
    sed -i "s/^user .*/user root;/" "$django_nginx_utilities_conf_setup"
    sudo cp "$django_nginx_utilities_conf_setup" "$django_nginx_server_conf_setup" || { echo "Failed to copy Nginx configuration"; exit 1; }
    # Define the current and new IP addresses
    current_ip="35.165.93.124"
    new_ip="$(curl -s ifconfig.me)"
    # Replace the IP address in the django.conf file
    echo "Updating IP address in django.conf..."
    sed -i "s/$current_ip/$new_ip/g" "$django_utilities_conf_setup"
    sudo cp "$django_utilities_conf_setup" "$django_server_conf_setup" || { echo "Failed to copy Django configuration"; exit 1; }
    # Update DJANGO_URL and DJANGO_SERVER_IP in the .env file
    echo "Updating DJANGO_URL and DJANGO_SERVER_IP in .env..."
    sed -i "s|DJANGO_URL=http://$current_ip|DJANGO_URL=http://$new_ip|g" "$django_env_file"
    sed -i "s|DJANGO_SERVER_IP=$current_ip|DJANGO_SERVER_IP=$new_ip|g" "$django_env_file"
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
elif [ "$choice" -eq 2 ]; then
    # Flask Configuration
    echo "Configuring Flask..."
    # Define the source and destination paths for Flask
    flask_gunicorn_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/flask/gunicorn.conf"
    flask_gunicorn_server_conf_setup="/etc/supervisor/conf.d/gunicorn.conf"
    flask_nginx_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/flask/nginx.conf"
    flask_nginx_server_conf_setup="/etc/nginx/nginx.conf"
    flask_utilities_conf_setup="/home/ubuntu/clean-smrs/utilities/flask/flask.conf"
    flask_server_conf_setup="/etc/nginx/sites-available/flask.conf"
    flask_env_file="/home/ubuntu/clean-smrs/flask/.env"
    # Copy Gunicorn configuration
    echo "Copying Gunicorn configuration file..."
    sudo cp "$flask_gunicorn_utilities_conf_setup" "$flask_gunicorn_server_conf_setup" || { echo "Failed to copy Gunicorn configuration"; exit 1; }
    # Create log directory for Gunicorn
    sudo mkdir -p /var/log/gunicorn
    # Update and copy Nginx configuration
    echo "Updating user directive in nginx.conf to run as root..."
    sed -i "s/^user .*/user root;/" "$flask_nginx_utilities_conf_setup"
    sudo cp "$flask_nginx_utilities_conf_setup" "$flask_nginx_server_conf_setup" || { echo "Failed to copy Nginx configuration"; exit 1; }
    # Define the current and new IP addresses
    current_ip="35.165.93.124"
    new_ip="$(curl -s ifconfig.me)"
    # Replace the IP address in the flask.conf file
    echo "Updating IP address in flask.conf..."
    sed -i "s/$current_ip/$new_ip/g" "$flask_utilities_conf_setup"
    sudo cp "$flask_utilities_conf_setup" "$flask_server_conf_setup" || { echo "Failed to copy Flask configuration"; exit 1; }
    # Update FLASK_URL and FLASK_SERVER_IP in the .env file
    echo "Updating FLASK_URL and FLASK_SERVER_IP in .env..."
    sed -i "s|FLASK_URL=http://$current_ip|FLASK_URL=http://$new_ip|g" "$flask_env_file"
    sed -i "s|FLASK_SERVER_IP=$current_ip|FLASK_SERVER_IP=$new_ip|g" "$flask_env_file"
    # Enable the Nginx site configuration
    sudo ln -sf /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled
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
else
    echo "Invalid choice. Please run the script again and select either 1 or 2."
    exit 1
fi