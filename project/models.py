from functools import wraps
from datetime import date
from flask import session, redirect, url_for, flash, g, abort
from werkzeug.local import LocalProxy
from werkzeug.security import check_password_hash, generate_password_hash
from project import mysql


#set up permission values
class Permission:
        PUBLIC = 1
        USER = 2
        ARCHIVIST = 4
        REVIEWER = 8        
        ADMINISTRATOR = 16

#user class
class User:
    def __init__(self, userID, roleID, permissions, preferred_title, name, email):
        self.id = str(userID)
        self.userID = userID
        self.roleID = roleID
        self.role = permissions
        self.permissions = permissions.get("permissions", Permission.PUBLIC)
        self.preferred_title = preferred_title or ""
        self.name = name
        self.email = email

    @property
    def is_authenticated(self):
        return True

    def can(self, permission):
        return (self.permissions & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)

#anonymous user class
class AnonymousUser:
    is_authenticated = False
    id = None
    userID = None
    preferred_title = ""
    name = ""
    email = ""
    role = {"name": "Public", "permissions": 1, "tasks": "Can view public items"}
    permissions = 1

    def can(self, permission):
        return False

    def is_administrator(self):
        return False


def _get_current_user():
    return getattr(g, "current_user", AnonymousUser())

#allows use of current_user for user
current_user = LocalProxy(_get_current_user)



def login_user(user):
    session["user_id"] = user.userID
    session["userID"] = user.userID
    g.current_user = user


def logout_user():
    session.clear()
    g.current_user = AnonymousUser()

# wrapper for access control 
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view

#role permissions class    
# Role definitions
# Public: Can view public items (permission 1)
# User: Can view public items and request access to restricted items (permissions 1 + 2 = 3)
# Archivist: Can view and edit all items can not approve access requests or change access levels (permissions 1 + 2 + 4 = 7)
# Reviewer: Can view and review items (permissions 1 + 2 + 8 = 11)
# Administrator: Can manage all aspects of the system (permissions 1 + 2 + 4 + 8 + 16 = 31)  
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
        
        
# fetches role by role name
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

#fetched role by permission value
def fetch_role_by_permission(roleID):
    result = row(
        """
        SELECT *
        FROM Roles
        WHERE roleID = %s
        """,
        (roleID,)
    )
    
    if result:
        return result
    
    return row(
        """
        SELECT *
        FROM Roles
        WHERE name = 'Public'
        """
    )

#fetches all roles
def fetch_all_roles():
    return rows(
        """
        SELECT *
        FROM Roles
        """
    )

#mysql helper function to retreive rows
def rows(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        cur.close()

#mysql helper function to retreive single row
def row(sql, params=None):
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchone()
    finally:
        cur.close()

#mysql helper function to execute query (insert, update, delete)
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

#gets the next id from table for use in adding records to table
def next_id(table_name: str, id_column: str, prefix: str, width: int = 3) -> str:
    current = row(
        f"SELECT MAX(CAST(SUBSTRING({id_column}, %s) AS UNSIGNED)) AS max_num FROM {table_name}",
        (len(prefix) + 1,),
    )
    max_num = current["max_num"] or 0
    return f"{prefix}{max_num + 1:0{width}d}"

#gets all collections from collection table
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

#gets item details by item id
def fetch_item(item_id: str):
    return row(
        """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               lg.languagename AS language_group,
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
               cm.communityApprovalStatus AS community_approval
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        JOIN languagegroup lg on ci.languagegroupid = lg.languagegroupid
        WHERE ci.itemID = %s
        """,
        (item_id,),
    )

#gets assessment record for item id
def fetch_assessment(item_id: str):
    return row(
        """
        SELECT 
               a.assessmentID as assessment_id, 
               ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               lg.languagename AS language_group,
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
               a.notes AS approval_notes,
               a.assessmentOutcome AS final_approval
        FROM assessmentrecord a
        JOIN CollectionItem ci on ci.itemID = a.itemID
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        LEFT JOIN languagegroup lg on ci.languagegroupid = lg.languagegroupid
        WHERE ci.itemID = %s
        """,
        (item_id,),
    )

#gets current item status
def fetch_item_status(item_id: str):
    return row(
        """
        SELECT 
            status             
        FROM CollectionItem     
        WHERE itemID = %s
        """,
        (item_id,),
    )

#gets all user access requests for a user 
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
            AND requestStatus != 'Cancel'
        ORDER BY requestDate
        """,
        (user_id,),
    )

#gets single access request for user and item id     
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
            AND requestStatus != 'Cancel'
        """,
        (user_id,item_id,),
    )

#gets user access request by request ID 
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

#cancels a user access request
def cancel_user_request(request_id):
    execute(
        """
        UPDATE accessrequest SET requestStatus = 'Cancel' WHERE requestID = %s
        """, (request_id,),
    )
    return True

#creates new user
def create_user(preferred_title, name, email, password):
    password_hash = generate_password_hash(password)
    user_id = next_id("Users", "userID", "U")
    execute(
        """
        INSERT INTO Users
        (userID, roleID, preferred_title, name, email, passwordHash)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, "R002", preferred_title, name, email, password_hash),
    )
    return user_id

#gets user details by email address
def get_user_by_email(email):
    return row(
        """
        SELECT userID, roleID, preferred_title, name, email, passwordHash
        FROM Users
        WHERE email = %s
        """,
        (email,),
    )

#gets user by user id
def get_user_by_id(userID):
    return row(
        """
        SELECT userID, roleID, preferred_title, name, email, passwordHash
        FROM Users
        WHERE userID = %s
        """,
        (userID,),
    )

#not used
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
    
#not used
def get_elder_reviewer_id():
    return row(
        """
        SELECT reviewerID,
               authorisationStatus,
               role
        FROM Reviewer
        WHERE role = %s
        """,
        ("Elder reviewer",),
    )

#checks password has been entered correctly
def verify_user_password(email, password):
    user = get_user_by_email(email)

    if user is None:
        return None

    if check_password_hash(user["passwordHash"], password):
        return user

    return None

#loads user by user id (login) 
def load_user(user_id):
    user = get_user_by_id(user_id)
 
    if user is None:
        return None
    
    permission = fetch_role_by_permission(user["roleID"])

    return  User(user["userID"], user["roleID"], permission, user["preferred_title"], user["name"], user["email"])

#admin loads users except the current user
def load_users(userID):
    users = rows(
        """
        SELECT 
            u.userID, 
            r.name AS role, 
            u.preferred_title, 
            u.name, 
            u.email
        FROM Users u
        JOIN Roles r ON u.roleID = r.roleID
        WHERE userID != %s
        ORDER BY u.name
        """,
        (userID,),
    )
    return users

#checks the file extension is in the allowed extensions 
def allowed_file(filename, allowed_extensions):
    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in allowed_extensions

#admin updates user permissions
def update_user_permissions(role,user_id):
    update_permission = execute(
        """
        UPDATE Users
        SET roleID = %s
        WHERE userID = %s
        """,
        (role, user_id),
     )

    return update_permission == 1
 
#insert new item
def add_new_item(array):
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
                languageGroupId,
                status,
                format,
                imagePath,
                recordPath,
                dateAdded
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            ),
        )

     meta_insert = execute(
            """
            INSERT INTO culturalmetadata
            (
                metadataID,
                itemID,
                accessLevel
            )
            VALUES (%s, %s, %s)
            """,
            (
                array["meta_id"],
                array["item_id"],
                "Under Assessment",
             ),
         )


     assessment_record_insert = execute(
            """
            INSERT INTO assessmentrecord
            (
                assessmentID,
                itemID,
                userID,
                assessmentDate,
                assessmentOutcome,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                array["assessment_id"],
                array["item_id"],
                array["userID"],
		        array["date_added"],
                "Under Review",
                "Initial submission"
             ),
         )   

     return item_insert == 1 and meta_insert == 1 and assessment_record_insert == 1

#gets items that require assessment
def get_assessment_rows():

     assessment_rows = rows(
        """
        SELECT 
               ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               lg.languagename AS language_group,
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
               ci.description AS public_description

        from assessmentrecord  a             
        JOIN CollectionItem ci on ci.itemid = a.itemID
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        join languagegroup lg on ci.languagegroupid = lg.languagegroupid
		WHERE ci.status = 'Under Assessment'
        ORDER BY ci.itemID
        """
    )
    
     return assessment_rows

#admin gets access requests
def get_pending_access_requests():

    access_request_rows = rows (
        """
        with accessrequests as (
            select
                requestID,
                itemID,
                userID,
                requestDate,
                requestStatus,
                purpose
            from accessrequest
        ), requestor as ( 
            select 
                userID,
                name,
                email
            from users 
        ), item as ( 
            select 
                itemID,
                collectionID,
                title,
                itemtype,
                imagePath,
                place,
                languagegroupid,
                status
            from collectionitem
        ), collection as ( 
            select 
                collectionID,
                collectionName
            from collection
        ), culturalmetadata as ( 
            select 
                metadataID,
                itemID,
                accessLevel,
                culturalSensitivity
            from culturalmetadata
        )
        select
            a.requestID as access_request_id,
            a.itemID as item_id,
            a.userID as user_id,
            a.requestDate as request_date,
            a.requestStatus as request_status,
            a.purpose as purpose,
            r.name as requestor_name,
            r.email as requestor_email,
            i.title as title,
            i.status as status,
            i.itemtype as item_type,
            i.imagepath as image_filename,
            i.collectionID as collection_id,
            c.collectionname as collection_name,
            m.metadataID as metadata_id,
            m.accessLevel as access_level,
            m.culturalSensitivity as cultural_sensitivity
        from accessrequests a 
        join item i on a.itemID = i.itemID
        join collection c on c.collectionID = i.collectionID 
        join culturalmetadata m on m.itemID = i.itemID
        join requestor r on r.userID = a.userID
        where a.requestStatus = 'Pending'
        """
    )
    return access_request_rows

#gets access requests by the id 
def get_access_request_by_id(requestID):

    return row (
        """
        with accessrequest as ( 
            select 
                requestID,
                itemID,
                userID,
                requestDate,
                requestStatus,
                purpose
            from accessrequest
        ), requestor as ( 
            select 
                userID,
                name,
                email
            from users 
        ), item as ( 
            select 
                itemID,
                collectionID,
                title,
                itemtype,
                imagePath,
                place,
                languagegroupid,
                status
            from collectionitem
        ), collection as ( 
            select 
                collectionID,
                collectionName
            from collection
        ), culturalmetadata as ( 
            select 
                metadataID,
                itemID,
                accessLevel,
                culturalSensitivity
            from culturalmetadata
        ), langgroup as ( 
            select 
                languagegroupid,
                languagename
            from languagegroup
        )
        select
            a.requestID as access_request_id,
            a.itemID as item_id,
            a.userID as user_id,
            a.requestDate as request_date,
            a.requestStatus as request_status,
            a.purpose as purpose,
            r.name as requestor_name,
            r.email as requestor_email,
            i.title as title,
            i.status as status,
            i.itemtype as item_type,
            i.imagepath as image_filename,
            i.place as place,
            lg.languagename as language_group,
            i.collectionID as collection_id,
            c.collectionname as collection_name,
            m.metadataID as metadata_id,
            m.accessLevel as access_level,
            m.culturalSensitivity as cultural_sensitivity
        from accessrequest a 
        join requestor r on a.userid = r.userid
        join item i on a.itemID = i.itemID
        join collection c on c.collectionID = i.collectionID 
        join culturalmetadata m on m.itemID = i.itemID
        join langgroup lg on i.languagegroupid = lg.languagegroupid
        where a.requestID = %s
        """,
        (requestID,),
    )

#gets featured items for the home page (public items approved)
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
          AND cm.communityApprovalStatus = 'Public'
          AND ci.status != 'Under Assessment'
        ORDER BY ci.itemID
        LIMIT 3
        """
    )
    return featured_items

#gets an items metadata
def get_item_metadata(item_id):
    requirements = rows(
        """
        SELECT metadataID AS requirement_id,
               culturalNotes AS requirement_text
        FROM CulturalMetadata
        WHERE itemID = %s
        """,
        (item_id,),
    )

    return requirements

#user item access request
def submit_access_request(request_array):
    today = date.today()
    execute(
            """
            INSERT INTO accessrequest
            (requestID, itemID, userID, requestDate, requestStatus, purpose)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ( 
                request_array["request_id"],
                request_array["item_id"],
                request_array["user_id"],
                date.today(),
                "Pending",
                request_array["full_purpose"],
            ),
        ) 
#filtered items by filter
def fetch_filtered_items(filters):
    sql = """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               lg.languagename AS language_group,
               ci.status,
               ci.imagePath AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.communityApprovalStatus AS review_status,
               cm.culturalSensitivity AS cultural_sensitivity
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        LEFT JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        LEFT JOIN languagegroup lg on ci.languagegroupid = lg.languagegroupid
        WHERE ci.status != 'Under Assessment'
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
        FROM CulturalMetadata
        WHERE communityApprovalStatus IS NOT NULL
          AND communityApprovalStatus != ''
        ORDER BY communityApprovalStatus
        """
    )

def get_reviewer_id_hack():
    return rows(
        """
        SELECT reviewerID
        FROM USERS 
        where role in ('Elder reviewer','Community representative','Collection manager')
        order by FIELD(role,'Elder reviewer','Collection manager','Community representative')
        LIMIT 1;
        """
    )

# NOTE executed within a combined commit
def execute_assessment_updates(item_id, user_id, final_decision, final_reason):
    cur = mysql.connection.cursor()
    try:
        mapped_status = get_mapped_status(final_decision)
        if mapped_status is None:
            raise ValueError(f"Mapping failed! '{final_decision}' is not a valid LHS status option.")
        assessment_query = "update assessmentrecord set assessmentoutcome = %s, userID = %s, notes = %s where itemid = %s" 
        cur.execute(assessment_query, (final_decision, user_id, final_reason, item_id))
        item_query = "update collectionitem set status = %s WHERE itemid = %s" 
        cur.execute(item_query, (mapped_status, item_id))        
        mysql.connection.commit()
        item_query2 = "update culturalmetadata set communityApprovalStatus = %s, accessLevel = %s WHERE itemid = %s" 
        cur.execute(item_query2, (mapped_status,mapped_status, item_id))        
        mysql.connection.commit()    
                  
        
            
        return cur.rowcount
    except:
        mysql.connection.rollback()
        raise
    finally:
        cur.close()

def get_mapped_status(status_string):

    status_mapping = {
        'Decision pending': 'Under Assessment',
        'Release publicly': 'Public',
        'Keep private': 'Private',
        'Release with restricted access': 'Restricted',
        'Library consultation': 'Restricted',
        'Return for further consultation' : 'Under Assessment'
    }

    return status_mapping.get(status_string, None)
           
#allow deny access request
def execute_access_request(access_request_id, final_decision):
    execute(
        """
        update accessrequest
        set requeststatus = %s
        WHERE requestid = %s
        """,
        (final_decision, access_request_id)
    )

#updates metadata
def update_metadata(metadata_id, access_level, cultural_sensitivity, community_approval_status, access_conditions, cultural_notes):
    execute(
        """
        update culturalmetadata
        set accessLevel = %s,
            culturalSensitivity = %s,
            communityApprovalStatus = %s,
            accessConditions = %s,
            culturalNotes = %s
        WHERE metadataID = %s
        """,
        (access_level, cultural_sensitivity, community_approval_status, access_conditions, cultural_notes, metadata_id)        
    )

#inserts comment for item assessment
def insert_assessment_comment(comment_id, assessment_id, user_id, date_time, comment):
    execute(
        """
        INSERT INTO assessmentcomment
            (commentID,
            assessmentID,
            userID,
            commentText,
            commentDate)
            VALUES
            (%s, %s, %s, %s, %s);
        """,
        (comment_id, assessment_id, user_id, comment, date_time )        
    )

#gets assessment comments for assessment item
def fetch_assessment_comments(assessment_id):
    return rows(
        """
        with comments as (
            select 
                assessmentID as assessment_id,
                userID,
                commentText as comment_text,
                commentDate as comment_date
            from assessmentcomment
        ), commentators as (
            select 
                userID,
                name,
                preferred_title
            from users 
        )  
        select 
            assessment_id,
            name as user_name,
            preferred_title,
            comment_text,
            comment_date
        from comments c
        join commentators co on c.userID = co.userID 
        where assessment_id = %s
        """,
        (assessment_id,),        
    )

#updates item details  
def update_item(item_id, title, description, item_type, place, language_group, item_format, date_recorded):
    execute(
        """
    UPDATE collectionitem
    SET title =%s,
        description = %s,
        itemType = %s,
        place = %s,
        languageGroupId = %s,
        format = %s,
        dateRecorded = %s
    WHERE itemID = %s
    """,
    (title, description, item_type, place, language_group, item_format, date_recorded, item_id),
    )
    
#deletes item from database    
def delete_item(item_id):
    execute(
        """
    DELETE FROM collectionitem
    WHERE itemID = %s
    """,
    (item_id,),
    )

#gets language groups       
def get_language_groups():
    return rows(
       """
       select 
       languageGroupID, 
       languageName 
       
       from languagegroup 
       
       order by languagename asc
       """ 
    )

#gets language group by name
def get_language_group_id_by_name(name):
    return row(
       """
       select 
       languageGroupID
       from languagegroup 
       
       where languageName = %s
        """,
        (name,),   
    )

def add_collections(name,description):
    collection_id = next_id("collection","collectionID", "C")
    add_collection = execute(
        """
        INSERT INTO collection
        (collectionID,collectionName,description)
        VALUES
        (%s,%s,%s)   
        """,(collection_id,name,description),
    )
    
    return add_collection == 1

#custom decorators    
def permission_required(permission):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_administrator(func):
    return permission_required(Permission.ADMINISTRATOR)(func)