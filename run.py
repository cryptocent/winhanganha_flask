import os
from werkzeug.security import generate_password_hash

from project import app
from project.models import mysql, User

# Patching users in the initial db script who have now passwords.
def patch_blank_passwords():
    print("🔄 Checking for blank user passwords.")
    pwd_hash = generate_password_hash("password")

    try:
        cursor = mysql.connection.cursor()
    except AttributeError:
        cursor = mysql.get_db().cursor()

    try:
        query = """
            UPDATE users 
            SET passwordHash = %s 
            WHERE passwordHash IS NULL OR passwordHash = '';
        """
        cursor.execute(query, (pwd_hash,))

        try:
            mysql.connection.commit()
        except AttributeError:
            mysql.get_db().commit()
            
    finally:
        cursor.close()

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

 
    # HOTFIX: patch users without passwords as these break the code.
    with app.app_context():
        try:
            patch_blank_passwords()
        except Exception as e:
            print(f"❌ Database update failed: {e}")
            print("Launching the app now.")
   
    app.run(host=host, port=port, debug=debug, load_dotenv=True)
