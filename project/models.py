from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from project import ALLOWED_EXTENSIONS, ALLOWED_IMG_EXTENSIONS, login_manager, mysql

class Permission:
        PUBLIC = 1
        USER = 2
        ARCHIVIST = 4
        REVIEWER = 8        
        ADMINISTRATOR = 16

#return User(user["userID"], permission["role"], permission["permissions"], user["preferred_title"], user["name"], user["email"])

class User(UserMixin):
    def __init__(self, userID, permissions, preferred_title, name, email):
        self.id = str(userID)
        self.userID = userID
        self.role = permissions
        self.permissions = permissions["permissions"]
        self.preferred_title = preferred_title or ""
        self.name = name
        self.email = email

    def can(self, permission):
        return (self.permissions & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)
    
      
class Role:
    def __init__(self, name, permissions=Permission.PUBLIC):
        self.name = name
        self.permissions = permissions

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def has_permission(self, perm):
        return (self.permissions & perm) == perm
    
    
    @staticmethod
    def all_roles():
        return {
            "Public": {
                "permissions": Permission.PUBLIC,
                "tasks": "Can view public items"
            },
            "User": {
                "permissions": Permission.PUBLIC | Permission.USER,
                "tasks": "Can view public items and request access to restricted items"
            },
            "Archivist": {
                "permissions": Permission.PUBLIC | Permission.USER | Permission.ARCHIVIST,
                "tasks": "Can view and edit archive items"
            },
            "Reviewer": {
                "permissions": Permission.PUBLIC | Permission.USER | Permission.ARCHIVIST | Permission.REVIEWER,
                "tasks": "Can view, edit, review, approve access requests and change access levels"
            },
            "Administrator": {
                "permissions": Permission.PUBLIC | Permission.USER | Permission.ARCHIVIST | Permission.REVIEWER | Permission.ADMINISTRATOR,
                "tasks": "Can manage all aspects of the system"
            }
        }  
    
    @staticmethod
    def update_user_role(user_id, new_role_name):
        roles = Role.all_roles()
        if new_role_name not in roles:
            raise ValueError("Invalid role value")
        
        new_permissions = roles[new_role_name]["permissions"]
                
        execute(
            """
            UPDATE Users
            SET permissions = %s
            WHERE userID = %s
            """,
            (new_permissions, user_id)
        )
        
    @staticmethod
    def insert_roles():
        
        roles = Role.all_roles()

        for role_name, role_data in roles.items():
            role = fetch_role_by_name(role_name)

            if role is None:
                role_id = next_id("Roles", "roleID", "R")

                execute(
                    """
                    INSERT INTO Roles
                        (roleID, name, permissions, tasks)
                    VALUES
                        (%s, %s, %s, %s)
                    """,
                    (
                        role_id,
                        role_name,
                        role_data["permissions"],
                        role_data["tasks"]
                    )
                )
            else:
                execute(
                    """
                    UPDATE Roles
                    SET permissions = %s,
                        tasks = %s
                    WHERE name = %s
                    """,
                    (
                        role_data["permissions"],
                        role_data["tasks"],
                        role_name
                    )
                )
        
        
# Role definitions
# Public: Can view public items (permission 1)
# User: Can view public items and request access to restricted items (permissions 1 + 2 = 3)
# Archivist: Can view and edit all items can not approve access requests or change access levels (permissions 1 + 2 + 4 = 7)
# Reviewer: Can view and review items (permissions 1 + 2 + 8 = 11)
# Administrator: Can manage all aspects of the system (permissions 1 + 2 + 4 + 8 + 16 = 31)
def fetch_role_by_name(role_name):
    result = row(
        """
        SELECT *
        FROM Roles
        WHERE name = %s
        """,
        (role_name,)
    )

    if result:
        return result

    return None

def fetch_role_by_permission(permissions):
    result = row(
        """
        SELECT *
        FROM Roles
        WHERE permissions = %s
        """,
        (permissions,)
    )
    
    if result:
        return result

    result["name"] = "Public"
    result["permissions"] = 1
    
    return result

def fetch_all_roles():
    return rows(
        """
        SELECT *
        FROM Roles
        """
    )


def rows(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        cur.close()


def row(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchone()
    finally:
        cur.close()


def execute(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        mysql.connection.commit()
    finally:
        cur.close()


def next_id(table_name: str, id_column: str, prefix: str, width: int = 3) -> str:
    current = row(
        f"SELECT MAX(CAST(SUBSTRING({id_column}, %s) AS UNSIGNED)) AS max_num FROM {table_name}",
        (len(prefix) + 1,),
    )
    max_num = current["max_num"] or 0
    return f"{prefix}{max_num + 1:0{width}d}"


def fetch_collections():
    return rows(
        """
        SELECT collectionID AS collection_id,
               collectionName AS name,
               description
        FROM Collection
        ORDER BY collectionName
        """
    )


def fetch_item(item_id: str):
    return row(
        """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               ci.format,
               DATE_FORMAT(ci.dateAdded, '%%d %%M %%Y') AS date_added,
               ci.dateRecorded AS date_recorded,
               REPLACE(ci.imagePath, 'img/', '') AS image_filename,
               c.collectionName AS collection_name,
               c.description AS collection_description,
               cm.ownership,
               cm.accessLevel AS access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.culturalNotes AS cultural_notes,
               cm.accessConditions AS access_conditions,
               cm.communityApprovalStatus AS community_approval
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.itemID = %s
        """,
        (item_id,),
    )

def fetch_user_requests(user_id):
    return rows(
        """
        SELECT 
            ar.requestID,
            ar.itemID,
            ar.requestDate,
            ar.requestStatus,
            ar.purpose,
            ci.title,
            ci.format,
            ci.status

        FROM accessrequest ar
        JOIN collectionitem ci ON ar.itemID = ci.itemID
        WHERE
            userID = %s
        ORDER BY requestDate
        """,
        (user_id,),
    )
    
def fetch_user_request(user_id, item_id):
    return row(
        """
        SELECT 
            ar.requestID,
            ar.itemID,
            ar.requestDate,
            ar.requestStatus,
            ar.purpose,
            ci.title,
            ci.format,
            ci.status

        FROM accessrequest ar
        JOIN collectionitem ci ON ar.itemID = ci.itemID
        WHERE
            ar.userID = %s
            AND ar.itemID = %s
        ORDER BY requestDate
        """,
        (user_id,item_id,),
    )



def create_user(preferred_title, name, email, password):
    password_hash = generate_password_hash(password)
    user_id = next_id("Users", "userID", "U")
    execute(
        """
        INSERT INTO Users
        (userID, permissions, preferred_title, name, email, passwordHash)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, "1", preferred_title, name, email, password_hash),
    )
    return user_id


def get_user_by_email(email):
    return row(
        """
        SELECT userID, permissions, preferred_title, name, email, passwordHash
        FROM Users
        WHERE email = %s
        """,
        (email,),
    )


def get_user_by_id(userID):
    return row(
        """
        SELECT userID, permissions, preferred_title, name, email, passwordHash
        FROM Users
        WHERE userID = %s
        """,
        (userID,),
    )


def get_user_reviewer(userID):
    return row(
        """
        SELECT reviewerID,
               authorisationStatus,
               role
        FROM Reviewer
        WHERE userID = %s
        """,
        (userID,),
    )


def verify_user_password(email, password):
    user = get_user_by_email(email)

    if user is None:
        return None

    if check_password_hash(user["passwordHash"], password):
        return user

    return None


# class User(UserMixin):
#     def __init__(self, userID, role, preferred_title, name, email):

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return None
    
    permission = fetch_role_by_permission(user["permissions"])
               #user["preferred_title"]
    return  User(user["userID"], permission, user["preferred_title"], user["name"], user["email"])
# lass User(UserMixin):
#     def __init__(self, userID, permissions, preferred_title, name, email):

def load_users():
    users = rows(
        """
        SELECT 
            u.userID, 
            r.name AS role, 
            u.preferred_title, 
            u.name, 
            u.email
        FROM Users u
        JOIN Roles r ON u.permissions = r.permissions
        
        """
    )
    return users

def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions