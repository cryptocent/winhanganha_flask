import os
from datetime import date
from pathlib import Path

import pymysql
from dotenv import load_dotenv
#from flask_login import LoginManager
from flask_bootstrap import Bootstrap4
from flask import Flask, abort, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


app = Flask(__name__)




def get_db():
    if "db" not in g:
        g.db = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def rows(sql, params=None):
    with get_db().cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchall()


def row(sql, params=None):
    with get_db().cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()


def execute(sql, params=None):
    with get_db().cursor() as cur:
        cur.execute(sql, params or ())
    get_db().commit()


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
               ci.itemID AS item_code,
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
               cm.handlingNotes AS cultural_notes,
               cm.handlingNotes AS access_conditions,
               cm.communityApprovalStatus AS community_approval,
               cm.communityApprovalStatus AS review_status
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE ci.itemID = %s
        """,
        (item_id,),
    )


def next_id(table_name: str, id_column: str, prefix: str, width: int = 3) -> str:
    current = row(
        f"SELECT MAX(CAST(SUBSTRING({id_column}, %s) AS UNSIGNED)) AS max_num FROM {table_name}",
        (len(prefix) + 1,),
    )
    max_num = current["max_num"] or 0
    return f"{prefix}{max_num + 1:0{width}d}"


@app.route("/")
@app.route("/index.html")
def home():
    featured_items = rows(
        """
        SELECT ci.itemID AS item_id,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               REPLACE(ci.imagePath, 'img/', '') AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.communityApprovalStatus AS review_status
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        WHERE cm.accessLevel = 'Public' AND cm.communityApprovalStatus = 'Approved' 
        ORDER BY ci.itemID
        LIMIT 3
        """
    )
    return render_template("index.html", collections=fetch_collections(), featured_items=featured_items)


@app.route("/items")
@app.route("/items.html")
def items():
    search = request.args.get("search", "").strip()
    collection = request.args.get("collection", "").strip()
    access_level = request.args.get("access_level", "").strip()
    item_type = request.args.get("item_type", "").strip()
    review_status = request.args.get("review_status", "").strip()

    sql = """
        SELECT ci.itemID AS item_id,
               ci.itemID AS item_code,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               REPLACE(ci.imagePath, 'img/', '') AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.communityApprovalStatus AS review_status,
               cm.culturalSensitivity AS cultural_sensitivity
        FROM CollectionItem ci
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
    """
    params = []

    if search:
        sql += " AND (ci.title LIKE %s OR ci.description LIKE %s OR ci.languageGroup LIKE %s OR ci.place LIKE %s OR c.collectionName LIKE %s)"
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

    item_rows = rows(sql, params)
    item_types = rows("SELECT DISTINCT itemType AS item_type FROM CollectionItem ORDER BY itemType")
    access_levels = rows("SELECT DISTINCT accessLevel AS access_level FROM CulturalMetadata ORDER BY accessLevel")
    review_statuses = rows("SELECT DISTINCT communityApprovalStatus AS review_status FROM CulturalMetadata ORDER BY communityApprovalStatus")

    return render_template(
        "items.html",
        items=item_rows,
        collections=fetch_collections(),
        item_types=item_types,
        access_levels=access_levels,
        review_statuses=review_statuses,
        filters={
            "search": search,
            "collection": collection,
            "access_level": access_level,
            "item_type": item_type,
            "review_status": review_status,
        },
    )


@app.route("/item/<item_id>")
@app.route("/item-details.html")
def item_detail(item_id: str = "I001"):
    item = fetch_item(item_id)
    if item is None:
        abort(404)
    requirements = rows(
        """
        SELECT metadataID AS requirement_id,
               handlingNotes AS requirement_text
        FROM CulturalMetadata
        WHERE itemID = %s
        """,
        (item_id,),
    )
    return render_template("item_detail.html", item=item, requirements=requirements)


@app.route("/request-access/<item_id>", methods=["POST"])
def request_access(item_id: str):
    if fetch_item(item_id) is None:
        abort(404)

    request_id = next_id("AccessRequest", "requestID", "Q")
    purpose = request.form.get("request_purpose", "").strip()
    details = request.form.get("request_details", "").strip()
    full_purpose = purpose if not details else f"{purpose}: {details}"

    execute(
        """
        INSERT INTO AccessRequest
        (requestID, itemID, requesterName, requesterEmail, requestDate, requestStatus, purpose)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            request_id,
            item_id,
            request.form.get("requester_name", "").strip(),
            request.form.get("requester_email", "").strip(),
            date.today().isoformat(),
            "Pending",
            full_purpose,
        ),
    )
    return redirect(url_for("item_detail", item_id=item_id, requested="1"))


#needs to be expanded to show all assessment items and details, currently only shows one item for testing purposes
@app.route("/item-assessment")
@app.route("/item-assessment.html")
def assessment():
    assessment_row = row(
        """
        SELECT ar.assessmentID AS assessment_id,
               ar.assessmentDate AS opened_date,
               DATE_ADD(ar.assessmentDate, INTERVAL 9 DAY) AS target_decision_date,
               ar.assessmentOutcome AS final_decision,
               ar.notes AS decision_reason,
               ar.notes AS pending_action,
               ci.itemID AS item_id,
               ci.itemID AS item_code,
               ci.title,
               ci.description,
               ci.itemType AS item_type,
               ci.place,
               ci.languageGroup AS language_group,
               ci.status,
               ci.dateRecorded AS date_recorded,
               REPLACE(ci.imagePath, 'img/', '') AS image_filename,
               c.collectionName AS collection_name,
               cm.accessLevel AS access_level,
               cm.accessLevel AS recommended_access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.communityApprovalStatus AS approval_status,
               cm.communityApprovalStatus AS review_status,
               cm.handlingNotes AS cultural_notes,
               cm.handlingNotes AS access_conditions,
               ci.description AS public_description,
               r.name AS assigned_reviewers
        FROM AssessmentRecord ar
        JOIN CollectionItem ci ON ci.itemID = ar.itemID
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        JOIN Reviewer r ON r.reviewerID = ar.reviewerID
        WHERE ar.itemID = 'I004'
        ORDER BY ar.assessmentID
        LIMIT 1
        """
    )
    if assessment_row is None:
        abort(404)

    notes = rows(
        """
        SELECT ac.commentID AS note_id,
               r.name AS reviewer_name,
               DATE_FORMAT(ac.commentDate, '%%d %%M %%Y') AS note_date,
               ac.commentText AS note_text
        FROM AssessmentComment ac
        JOIN Reviewer r ON r.reviewerID = ac.reviewerID
        WHERE ac.assessmentID = %s
        ORDER BY ac.commentDate, ac.commentID
        """,
        (assessment_row["assessment_id"],),
    )
    return render_template("item_assessment.html", assessment=assessment_row, notes=notes)


if __name__ == "__main__":
    host = os.environ.get('FLASK_HOST')
    port = int(os.environ.get('FLASK_PORT'))
    debug_val = os.getenv("FLASK_DEBUG")
    is_debug = debug_val.lower() == "true" if debug_val else False
    app.run(host=host, port=port, debug=is_debug)