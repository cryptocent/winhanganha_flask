import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mysqldb import MySQL


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
upload_folder = BASE_DIR / "uploads"
os.makedirs(upload_folder, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'csv', 'zip', 'rar', '7z', 'tar', 'gz', 'mp3', 'mp4', 'avi', 'mkv'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = upload_folder
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DATABASE")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CHARSET"] = "utf8mb4"



mysql = MySQL(app)
bootstrap = Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


from project import models
from project import views


with app.app_context():
    models.Role.insert_roles()
    
@app.context_processor
def inject_permissions():
    from project.models import Permission
    return dict(Permission=Permission)    