from datetime import date

from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user

from project import app
from project.forms import LoginForm, MetadataForm, RegistrationForm, AccessRequestForm
from project.models import (
    User,
    create_user,
    execute,
    fetch_collections,
    fetch_item,
    get_user_reviewer,
    next_id,
    row,
    rows,
    verify_user_password,
    fetch_user_requests,
    fetch_user_request,
    role,
    permission
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


@app.route("/")
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
        WHERE cm.accessLevel = 'Public'
          AND cm.communityApprovalStatus = 'Approved'
        ORDER BY ci.itemID
        LIMIT 3
        """
    )
    return render_template(
        "index.html",
        collections=fetch_collections(),
        featured_items=featured_items,
    )


@app.route("/items")
def items():
    search = request.args.get("search", "").strip()
    collection = request.args.get("collection", "").strip()
    access_level = request.args.get("access_level", "").strip()
    item_type = request.args.get("item_type", "").strip()
    review_status = request.args.get("review_status", "").strip()

    sql = """
        SELECT ci.itemID AS item_id,
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
        WHERE 1 = 1
    """
    params = []

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


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item_detail(item_id: str = "I001"):
    form = AccessRequestForm(request.form)
    item = fetch_item(item_id)
    if item is None:
        abort(404)

    requirements = rows(
        """
        SELECT metadataID AS requirement_id,
               culturalNotes AS requirement_text
        FROM CulturalMetadata
        WHERE itemID = %s
        """,
        (item_id,),
    )

    request_row = None

    if current_user.is_authenticated:
        request_row = fetch_user_request(current_user.id,item_id)

    if request.method == "POST" and form.validate():
        if session.get("userID") is None:
            flash("You must be logged in to request access.", "warning")
            return redirect(url_for("login"))
        
        request_id = next_id("accessrequest", "requestID", "Q")
        purpose = form.purpose.data.strip()
        details = form.details.data.strip()
        full_purpose = purpose if not details else f"{purpose}: {details}"

        execute(
            """
            INSERT INTO accessrequest
            (requestID, itemID, userID, requestDate, requestStatus, purpose)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                request_id,
                item_id,
                session.get("userID"),
                date.today().isoformat(),
                "Pending",
                full_purpose,
            ),
        ) 
        
        flash("Your request has been received. You will be notified of the request outcome", "success")
        return redirect(url_for("item_detail", item_id=item_id))
    
    return render_template("item_detail.html", item=item, requirements=requirements, form=form, access_request=request_row)

@app.route("/item-assessment")
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
               cm.recommendedAccessLevel AS recommended_access_level,
               cm.culturalSensitivity AS cultural_sensitivity,
               cm.communityApprovalStatus AS review_status,
               cm.culturalNotes AS cultural_notes,
               cm.accessConditions AS access_conditions,
               ci.description AS public_description,
               u.name AS assigned_reviewers
        FROM AssessmentRecord ar
        JOIN CollectionItem ci ON ci.itemID = ar.itemID
        JOIN Collection c ON c.collectionID = ci.collectionID
        JOIN CulturalMetadata cm ON cm.itemID = ci.itemID
        JOIN Reviewer r ON r.reviewerID = ar.reviewerID
        JOIN Users u ON u.userID = r.userID
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
               u.name AS reviewer_name,
               DATE_FORMAT(ac.commentDate, '%%d %%M %%Y') AS note_date,
               ac.commentText AS note_text
        FROM AssessmentComment ac
        JOIN Reviewer r ON r.reviewerID = ac.reviewerID
        JOIN Users u ON u.userID = r.userID
        WHERE ac.assessmentID = %s
        ORDER BY ac.commentDate, ac.commentID
        """,
        (assessment_row["assessment_id"],),
    )
    return render_template("item_assessment.html", assessment=assessment_row, notes=notes)


@app.route("/item-assessment", methods=["POST"])
def update_assessment_metadata():
    form = MetadataForm(request.form)
    if form.validate():
        flash("Assessment metadata saved.", "success")
    else:
        flash("Assessment metadata could not be saved.", "danger")
    return redirect(url_for("assessment"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        create_user(form.name.data, form.email.data, form.password.data)
        flash("Thanks for registering. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data
        user_row = verify_user_password(email, password)

        if user_row:
            user = User(user_row["userID"], user_row["name"], user_row["email"])
            login_user(user)

            session["userID"] = user_row["userID"]
            session["name"] = user_row["name"]
            session["email"] = user_row["email"]

            reviewer_info = get_user_reviewer(user_row["userID"])
            if reviewer_info:
                session["authorisationStatus"] = reviewer_info["authorisationStatus"]
                session["role"] = reviewer_info["role"]
                session["reviewerID"] = reviewer_info["reviewerID"]

            flash("Logged in successfully", "success")
            return redirect(url_for("account"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    request_rows = fetch_user_requests(current_user.id)
    return render_template("account.html", requests=request_rows)
