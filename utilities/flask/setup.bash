python3 --version
python3 -m venv main_env
source main_env/bin/activate
touch main.py
flask --app main.py run --debug
#windows python -m flask --app main.py run --debug
