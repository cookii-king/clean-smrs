python3 --version
python3 -m venv main_env
source main_env/bin/activate
pip3 install flask
pip3 install flask_sqlalchemy
pip3 install flask_marshmallow
pip3 install marshmallow-sqlalchemy
touch main.py
flask --app main.py run --debug
