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

