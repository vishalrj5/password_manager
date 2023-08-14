configure db on .env ( rename the .env.example to .env )

create virtual environment
python -m venv venv

Install requirements on requirements.txt
pip install -r requirements.txt

run migrations
python manage.py makemigrations
python manage.py migrate

run server
python manage.py runserver