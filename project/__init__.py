import os
from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL



BASE_DIR = Path(__file__).resolve().parent.parent

#sets upload folder makes it if it does not exist
upload_folder = BASE_DIR / "project" / "static" / "uploads"
os.makedirs(upload_folder, exist_ok=True)

#allowed extensions for archive upload types
ALLOWED_EXTENSIONS = {
    "txt", "pdf", "png", "jpg", "jpeg", "gif",
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "csv", "zip", "rar", "7z", "tar", "gz",
    "mp3", "mp4", "avi", "mkv"
}
#allowed extensions for archive image upload
ALLOWED_IMG_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif"
}

#app config 
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = upload_folder
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["ALLOWED_IMG_EXTENSIONS"] = ALLOWED_IMG_EXTENSIONS

###############################################################################################################
###############################################################################################################
## update parameters to suit environment
app.config["SECRET_KEY"] = "SuperSecretKeyForSessionManagement13579"
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3306 #3306 is default MySQL port
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "winhanganha_archive"

app.config["FLASK_RUN_HOST"] = "127.0.0.1"
app.config["FLASK_RUN_PORT"] = 5000 #5000 is default for flask app (http://localhost:5000)
## must be false on submission
app.config["FLASK_DEBUG"] = False

## end of parameter updates
###############################################################################################################
###############################################################################################################


app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CHARSET"] = "utf8mb4"

#database connection
mysql = MySQL(app)

#flask-login session management
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
login_manager.init_app(app)

#bootstrap css and js injection
bootstrap = Bootstrap5(app)

from project import models
from project.models import (
    User,
    AnonymousUser,
    get_user_by_id,
    fetch_role_by_permission
)

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return None

    permission = fetch_role_by_permission(user["roleID"])

    return User(
        user["userID"],
        user["roleID"],
        permission,
        user["preferred_title"],
        user["name"],
        user["email"]
    )

#inserts roles each time app is loaded (if roles are actually changed in the source this ensures the roles are updated in the DB)
with app.app_context():
    models.Role.insert_roles()

from project import views

#allows usage of permisson throughout app
@app.context_processor
def inject_permissions():
    from project.models import Permission
    return dict(Permission=Permission)

#file type output reader friendly
def file_type(path):
    if not path:
        return "none"

    ext = os.path.splitext(path)[1].lower().replace(".", "")

    image_types = {"png", "jpg", "jpeg", "gif", "webp"}
    pdf_types = {"pdf"}
    video_types = {"mp4", "webm", "ogg", "avi", "mkv"}
    audio_types = {"mp3", "wav", "ogg", "m4a"}
    document_types = {"doc", "docx", "txt", "rtf"}
    spreadsheet_types = {"xls", "xlsx", "csv"}
    presentation_types = {"ppt", "pptx"}
    archive_types = {"zip", "rar", "7z", "tar", "gz"}

    if ext in image_types:
        return "image"
    if ext in pdf_types:
        return "pdf"
    if ext in video_types:
        return "video"
    if ext in audio_types:
        return "audio"
    if ext in document_types:
        return "document"
    if ext in spreadsheet_types:
        return "spreadsheet"
    if ext in presentation_types:
        return "presentation"
    if ext in archive_types:
        return "archive"

    return "file"
#loads file types to the jinja templates
app.jinja_env.globals.update(file_type=file_type)