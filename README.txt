# First Nations Winhanganha Archive Flask Project

## Project Structure



run.py
project/
  __init__.py        Flask app, Bootstrap, MySQL and Flask Env setup
  views.py           Routes and page handlers
  models.py          Database and other functions
  decorators.py      Custom decorators and permission checks
  forms.py           WTForms classes
  templates/         Jinja templates
  static/            CSS and images
database.sql


## Setup

### 1. Create and activate a virtual environment

#### Windows
python -m venv venv
venv/scripts/activate


#### Linux
python3 -m venv venv
source venv/bin/activate


### 2. Install dependencies


python3 -m pip install -r requirements.txt


### 3. Update the __init__.py file with your environment parameters.

########################################################################################################################
########################################################################################################################
## update parameters to suit environment
app.config["SECRET_KEY"] = "SuperSecretKeyForSessionManagement13579"
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "winhanganha_archive"

app.config["FLASK_RUN_HOST"] = "127.0.0.1"
app.config["FLASK_RUN_PORT"] = 1337
## must be false on submission
app.config["FLASK_DEBUG"] = False 

## end of parameter updates
########################################################################################################################
########################################################################################################################

### 4. Create the database

Import the database file into MySQL:

database.sql


### 5. Run the app (from the app root)

#### Windows
python ./run.py

#### Linux
python3 ./run.py


## Notes


* Ensure MySQL is running before starting the Flask application.
