First Nations Winhanganha Archive Flask Project

Project structure
-----------------
.env
run.py
project/
  __init__.py        Flask app, Bootstrap, MySQL and Flask-Login setup
  views.py           Routes and page handlers
  models.py          Database helper functions, user model and login loader
  decorators.py         
  forms.py           WTForms classes
  templates/         Jinja templates
  static/            CSS and images
winhanganha_archive.sql

Setup
-----
1. Create and activate a virtual environment. 
       python3 -m venv venv
       venv/scripts/activate <-- Windows
       venv/bin/activate <-- Linux

2. Install dependencies:
       python3 -m pip install -r requirements.txt

3. Create a .env file beside run.py:
       SECRET_KEY=replace_with_a_long_random_secret
       MYSQL_HOST=localhost
       MYSQL_PORT=3306
       MYSQL_USER=root
       MYSQL_PASSWORD=your_mysql_password
       MYSQL_DATABASE=winhanganha_archive
       FLASK_HOST=127.0.0.1
       FLASK_PORT=5000
       FLASK_DEBUG=true

4. Create the database:
       mysql: import the database winhanganha_archive.sql

5. Run the app:
       python3 run.py

Notes
-----

