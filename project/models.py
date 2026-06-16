from flask_login import UserMixin, AnonymousUserMixin
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

class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False
      
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
        return cur.rowcount
    except:
        mysql.connection.rollback()
        raise
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


def fetch_item(item_id):
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
               ci.imagePath AS image_filename,
               ci.recordPath as recordPath,
               c.collectionName AS collection_name,
               c.description AS collection_description,
               cm.ownership,
               cm.accessLevel AS access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.culturalNotes AS cultural_notes,
               cm.accessConditions AS access_conditions,
               cm.communityApprovalStatus AS community_approval,
               cm.itemHandling AS item_handling
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.itemID = %s AND ci.status != 'Remove'
        """,
        (item_id,),
    )

def fetch_item_status(item_id):
    return row(
        """
        SELECT 
            status             
        FROM CollectionItem     
        WHERE itemID = %s
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
            AND requestStatus != 'Cancel' AND ci.status != 'Remove'
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
            AND requestStatus != 'Cancel' AND ci.status != 'Remove'
        """,
        (user_id,item_id,),
    )

def fetch_user_request_by_ID(user_id, request_id):
    return row(
        """
        SELECT 
            ar.requestID
        FROM accessrequest ar
        WHERE
            ar.userID = %s
            AND ar.requestID = %s
        """,
        (user_id,request_id,),
    )

def cancel_user_request(request_id):
    execute(
        """
        UPDATE accessrequest SET requestStatus = 'Cancel' WHERE requestID = %s
        """, (request_id,),
    )
    return True


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


# def get_user_reviewer(userID):
#     return row(
#         """
#         SELECT reviewerID,
#                authorisationStatus,
#                role
#         FROM Reviewer
#         WHERE userID = %s
#         """,
#         (userID,),
#     )


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

def load_users(userID = ''):
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
        WHERE userID != %s
        """,
        (userID,),
    )
    return users

def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def update_user_permissions(user_id,role):
    update_permission = execute(
        """
        UPDATE Users
        SET permissions = %s
        WHERE userID = %s
        """,
        (role, user_id),
     )

    return update_permission == 1
 

def add_new_item(array):
    
    array["item_id"] = next_id("CollectionItem", "itemID", "I")
    array["meta_id"] = next_id("culturalmetadata", "metadataID", "M")
    
    item_insert = execute(
            """
            INSERT INTO CollectionItem
            (
                itemID,
                collectionID,
                title,
                description,
                itemType,
                place,
                languageGroup,
                status,
                format,
                imagePath,
                recordPath,
                dateAdded,
                dateRecorded
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                array["item_id"],
                array["collection_id"],
                array["title"],
                array["description"],
                array["item_type"],
                array["place"],
                array["language_group"],
                "Under Assessment",
                array["record_format"],
                array["img_path"],
                array["record_path"],
                array["date_added"],
                array["date_recorded"],
            ),
        )

    meta_insert = execute(
            """
            INSERT INTO culturalmetadata
            (
                metadataID,
                itemID,
                accessLevel,
                culturalSensitivity,
                communityApprovalStatus
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                array["meta_id"],
                array["item_id"],
                "Under Assessment",
                "Not yet assessed",
                "Under Assessment"
             ),
         )

    return item_insert == 1 and meta_insert == 1

def get_assessment_rows():

     assessment_rows = rows(
        """
        SELECT 
               ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               ci.dateRecorded AS date_recorded,
               ci.imagePath AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.recommendedAccessLevel AS recommended_access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.communityApprovalStatus AS review_status,
               cm.culturalNotes AS cultural_notes,
               cm.accessConditions AS access_conditions,
               cm.itemHandling AS item_handling
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.status = 'Under Assessment'
        ORDER BY ci.itemID
        """
    )
    
     return assessment_rows

def get_featured_items():
    featured_items = rows(
        """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.imagePath AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.communityApprovalStatus AS review_status
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE cm.accessLevel = 'Public'
          AND cm.communityApprovalStatus = 'Approved'
        ORDER BY ci.itemID
        LIMIT 3
        """
    )
    return featured_items

def get_item_metadata(item_id):
    requirements = rows(
        """
        SELECT *
        FROM CulturalMetadata
        WHERE itemID = %s
        """,
        (item_id,),
    )

    return requirements


def submit_access_request(request_array):
    
    request_array["request_id"] = next_id("accessrequest", "requestID", "Q")
    
    request_insert = execute(
            """
            INSERT INTO accessrequest
            (requestID, itemID, userID, requestDate, requestStatus, purpose)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                request_array["request_id"],
                request_array["item_id"],
                request_array["current_user"],
                request_array["request_date"],
                "Pending",
                request_array["full_purpose"],
            ),
        ) 
    return request_insert == 1


def fetch_filtered_items(filters):
    sql = """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               ci.imagePath AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.communityApprovalStatus AS review_status,
               cm.culturalSensitivity AS cultural_sensitivity
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.status != 'Under Assessment' AND ci.status != 'Remove'
    """

    params = []

    search = filters.get("search")
    collection = filters.get("collection")
    access_level = filters.get("access_level")
    item_type = filters.get("item_type")
    review_status = filters.get("review_status")

    if search:
        sql += """
            AND (
                ci.title LIKE %s
                OR ci.description LIKE %s
                OR ci.languageGroup LIKE %s
                OR ci.place LIKE %s
                OR c.collectionName LIKE %s
            )
        """
        term = f"%{search}%"
        params.extend([term, term, term, term, term])

    if collection:
        sql += " AND c.collectionName = %s"
        params.append(collection)

    if access_level:
        sql += " AND cm.accessLevel = %s"
        params.append(access_level)

    if item_type:
        sql += " AND ci.itemType = %s"
        params.append(item_type)

    if review_status:
        sql += " AND cm.communityApprovalStatus = %s"
        params.append(review_status)

    sql += " ORDER BY ci.itemID"

    return rows(sql, params)


def fetch_item_type_filters():
    return rows(
        """
        SELECT DISTINCT itemType AS item_type
        FROM CollectionItem
        WHERE itemType IS NOT NULL
          AND itemType != ''
        ORDER BY itemType
        """
    )


def fetch_access_level_filters():
    return rows(
        """
        SELECT DISTINCT accessLevel AS access_level
        FROM CulturalMetadata
        WHERE accessLevel IS NOT NULL
          AND accessLevel != ''
        ORDER BY accessLevel
        """
    )


def fetch_review_status_filters():
    return rows(
        """
        SELECT DISTINCT communityApprovalStatus AS review_status
        FROM culturalmetadata
        WHERE communityApprovalStatus IS NOT NULL
          AND communityApprovalStatus != ''
        ORDER BY communityApprovalStatus
        """
    )
    
def update_meta_data(form, item_id):
    
    if form.access_level.data == "Under Assessment":
        communityApproval = "Under Assessment"
    else:
        communityApproval = "Approved"
        
    execute(
        """
        UPDATE culturalmetadata
        SET accessLevel = %s,
            culturalSensitivity = %s,
            ownership = %s,
            culturalNotes = %s,
            accessConditions = %s,
            itemHandling = %s,
            communityApprovalStatus = %s
        WHERE 
            itemID = %s
        """,
        (
            form.access_level.data,
            form.cultural_sensitivity.data,
            form.ownership.data,
            form.cultural_notes.data,
            form.access_conditions.data,
            form.item_handling.data,
            communityApproval,
            item_id,
        ),
    )
    
    execute(
        """
        UPDATE collectionitem
        SET 
            status = %s,
            title = %s,
            description = %s,
            place = %s,
            languageGroup = %s
        WHERE 
            itemID = %s
        """,
        (
            form.approval_status.data,
            form.title.data,
            form.description.data,
            form.place.data,
            form.language_group.data,
            item_id
        ),        
    )
    
def fetch_item_comments(item_id):
    
    comments = rows(
    """
    SELECT
        ac.commentID,
        ac.commentText,
        ac.commentDate,
        CASE
            WHEN u.preferred_title IS NULL THEN ''
            WHEN u.preferred_title = '' THEN ''
            WHEN LOWER(u.preferred_title) = 'none' THEN ''
            ELSE u.preferred_title
        END AS preferred_title,
        u.name,
        r.name AS 'role_name'
    FROM
        assessmentcomment ac
        JOIN users u ON u.userID = ac.userID
        JOIN roles r ON u.permissions = r.permissions
    WHERE 
        ac.itemID = %s
    ORDER BY
        ac.commentID DESC, ac.commentDate
    
    """,(item_id,),
    )
    
    return comments


def add_item_comment(item_id,comment_text,user,date_added):
    comment_id = next_id("assessmentcomment", "commentID", "AC")
    
    comment_insert = execute(
        """
        INSERT INTO 
            assessmentcomment
            (commentID, itemID, userID, commentText, commentDate)
            VALUES
            (%s,%s,%s,%s,%s)        
        """,(
            comment_id,
            item_id,
            user,
            comment_text,
            date_added            
        ),
    )
    
    return comment_insert == 1