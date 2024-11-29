python3 --version
python3 -m venv .venv
source .venv/bin/activate
touch main.py
flask --app main.py run --debug
#windows python -m flask --app main.py run --debug
