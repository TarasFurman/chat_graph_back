# chat_graph_back

1. Clone project:

git clone https://github.com/TarasFurman/chat_graph_back.git

2. Create venv:

python3 -m venv venv

source venv/bin/activate

cd chat_graph_back

pip install -r requirements.txt

3. Create .env file with next keys (or use existing one in project):
DJANGO_SETTINGS_MODULE<br/>
DJANGO_CONFIGURATION<br/>
DEBUG<br/>
DB_NAME<br/>
DB_USER<br/>
DB_PASSWORD<br/>
DB_HOST<br/>
DB_PORT<br/>
SECRET_KEY<br/>

4. Create postgresql database and user with names and password from .env file

5. Start django-project:

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
