from calendar import c
from datetime import date
from tkinter import CURRENT
from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import file
from wtforms import form
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename
import MySQLdb
from project import ALLOWED_EXTENSIONS, ALLOWED_IMG_EXTENSIONS, app
from project.decorators import permission_required, is_administrator
from project.forms import LoginForm, MetadataForm, RegistrationForm, AccessRequestForm, AddItemForm, CancelUserRequest, AssessmentForm, AccessRequestDecisionForm, ContactForm
from project.models import (
    Permission,
    Role,
    User,
    add_new_item,
    allowed_file,
    cancel_user_request,
    create_user,
    execute,
    fetch_access_level_filters,
    fetch_all_roles,
    fetch_collections,
    fetch_filtered_items,
    fetch_item,
    fetch_assessment,
    fetch_item_status,
    fetch_item_type_filters,
    fetch_review_status_filters,
    fetch_role_by_permission,
    fetch_user_request,
    fetch_user_request_by_ID,
    fetch_user_requests,
    get_assessment_rows,
    get_featured_items,
    get_item_metadata,
    get_user_reviewer,
    load_users,
    next_id,
    row,
    rows,
    secure_filename,
    submit_access_request,
    update_user_permissions,
    verify_user_password,
    execute_assessment_updates,
    get_pending_access_requests,
    get_access_request_by_id,
    execute_access_request,
    update_metadata,
    insert_assessment_comment,
    fetch_assessment_comments,
    update_item,
    delete_item,
    get_language_groups,
    get_language_group_id_by_name
)

@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

@app.errorhandler(MySQLdb.Error)
def internal_error(e):
    return render_template("500.html"), 500

@app.route("/")
def home():
    featured_items = get_featured_items()
    return render_template(
        "index.html",
        collections=fetch_collections(),
        featured_items=featured_items,
    )


@app.route("/items")
def items():
    filters = {
        "search": request.args.get("search", "").strip(),
        "collection": request.args.get("collection", "").strip(),
        "access_level": request.args.get("access_level", "").strip(),
        "item_type": request.args.get("item_type", "").strip(),
        "review_status": request.args.get("review_status", "").strip(),
    }

    item_rows = fetch_filtered_items(filters)

    return render_template(
        "items.html",
        items=item_rows,
        collections=fetch_collections(),
        item_types=fetch_item_type_filters(),
        access_levels=fetch_access_level_filters(),
        review_statuses=fetch_review_status_filters(),
        filters=filters,
    )


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item_detail(item_id):
    form = AccessRequestForm(request.form)
    item = fetch_item(item_id)
    if item is None:
        abort(404)

    if item["status"] == "Under Assessment":
        if not current_user.is_authenticated:
            flash("You must be logged in to view this item.", "warning")
            return redirect(url_for("login"))

        if not current_user.can(Permission.ARCHIVIST):
            abort(403)

    requirements = get_item_metadata(item_id)

    request_row = None

    if current_user.is_authenticated:
        request_row = fetch_user_request(current_user.id,item_id)

    if request.method == "POST" and form.validate():
        request_array = {}
        if session.get("userID") is None:
            flash("You must be logged in to request access.", "warning")
            return redirect(url_for("login"))
        
        request_array["request_id"] = next_id("accessrequest", "requestID", "Q")
        purpose = form.purpose.data.strip()
        details = form.details.data.strip()
        request_array["full_purpose"] = purpose if not details else f"{purpose}: {details}"
        request_array["item_id"] = item_id
        request_array["user_id"] = current_user.userID

        success = submit_access_request(request_array)
        
        flash("Your request has been received. You will be notified of the request outcome", "success")
        return redirect(url_for("item_detail", item_id=item_id))
    
    return render_template("item_detail.html", item=item, requirements=requirements, form=form, access_request=request_row)


@app.route("/item-assessments", methods=["GET", "POST"])
@login_required
@permission_required(Permission.ARCHIVIST)
def assessments():
    assessment_rows = get_assessment_rows()
    access_request_rows = get_pending_access_requests()  
    return render_template("item_assessment_list.html", assessments=assessment_rows, access_requests = access_request_rows)

@app.route("/item-assessment/<item_id>", methods=["GET", "POST"])
@login_required
@permission_required(Permission.ARCHIVIST)
def assessment_item(item_id):
    form = AssessmentForm(request.form)
    final_decision = None 
    if request.method == "POST":
        final_decision = request.form.get("final_decision")
        #print(f"POST received for Item ID: {item_id}, Decision Outcome: {final_decision}")
        if "submit_metadata" in request.form:
            metadata = get_item_metadata(item_id)
            metadata_id = metadata[0]['requirement_id']
            update_metadata(metadata_id, request.form.get("access_level"), request.form.get("cultural_sensitivity"),    
                            request.form.get("community_approval"), request.form.get("access_conditions"),
                            request.form.get("cultural_notes"))
            flash("Metadata Updated", "success")   
        elif final_decision:
            if not current_user.can(Permission.REVIEWER):
                flash("You do not have permission to submit a final decision.", "danger")
                return redirect(url_for("assessment_item", item_id=item_id))
            user_id = current_user.userID   
            execute_assessment_updates(item_id, user_id, final_decision)
            flash("Assessment completed successfully", "success")
            return redirect(url_for("assessments"))   
        elif "submit_notes" in request.form:  
            assessment_row = fetch_assessment(item_id) 
            note = request.form.get("discussion_note")
            date_added = date.today().strftime("%Y-%m-%d %H:%M:%S")  
            comment_id = next_id("assessmentcomment", "commentID", "AC")
            user_id = current_user.userID         
            insert_assessment_comment(comment_id, assessment_row['assessment_id'], user_id, date_added, note)   
            flash("Note added", "success")        
        else:
            flash("No decision was selected.", "danger")

    assessment_row = fetch_assessment(item_id) 
    assessments_comments = fetch_assessment_comments(assessment_row['assessment_id'])
    language_groups = get_language_groups()
    return render_template("item_assessment.html", assessment=assessment_row, notes = assessments_comments,
        languages = language_groups, form=form, item_id=item_id, final_decision=final_decision)


@app.route("/access_request/<access_request_id>", methods=["GET", "POST"])
@login_required
@permission_required(Permission.REVIEWER)
def access_request(access_request_id):
    form = AccessRequestDecisionForm(request.form)
    if request.method == "POST":
        final_decision = request.form.get("final_decision")
        execute_access_request(access_request_id, final_decision)
        return redirect(url_for("assessments"))
    access_request_row = get_access_request_by_id(access_request_id)
    return render_template("access_request.html", access_request=access_request_row, 
        form=form, access_request_id=access_request_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        create_user(form.preferred_title.data, form.name.data, form.email.data, form.password.data)
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
            permission = fetch_role_by_permission(user_row["roleID"])
            user = User(user_row["userID"], permission['roleID'], permission, user_row["preferred_title"], user_row["name"], user_row["email"])
            login_user(user)

            session["userID"] = user_row["userID"]
            session["role"] = permission["permissions"]
            session["preferred_title"] = user_row["preferred_title"]
            session["name"] = user_row["name"]
            session["email"] = user_row["email"]

            # reviewer_info = get_user_reviewer(user_row["userID"])
            # if reviewer_info:
            #     session["authorisationStatus"] = reviewer_info["authorisationStatus"]
            #     session["role"] = reviewer_info["role"]
            #     session["reviewerID"] = reviewer_info["reviewerID"]

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
    return redirect(url_for("login"))



@app.route("/account", methods=["GET", "POST"])
@login_required
def account():

    if request.method == "POST":
        complete = False
        request_id = request.form.get("requestID")
        user_request = fetch_user_request_by_ID(current_user.userID,request_id)

        if user_request is None:
            return None

        complete = cancel_user_request(user_request["requestID"])
        if complete == True:
            flash("Request cancelled successfully.", "success")
            return redirect(url_for("account"))
        flash("Request cancel failed.", "danger")
        return redirect(url_for("account"))

    cancel_request_form = CancelUserRequest(request.form)
    request_rows = fetch_user_requests(current_user.id)
    return render_template("account.html", requests=request_rows, form=cancel_request_form)



@app.route("/dashboard", methods=["GET", "POST"])
@login_required
@is_administrator
def dashboard():
   
    if request.method == "POST":
        user_id = request.form.get("userID")
        role_id =  request.form.get("role")
        new_role = fetch_role_by_permission(role_id)
        update_user_permissions(new_role["roleID"], user_id)
        flash("User role updated successfully.", "success")
        return redirect(url_for("dashboard"))
    
    
    request_users = load_users(current_user.userID)
    all_roles = fetch_all_roles()
    return render_template("admin.html", users=request_users, roles=all_roles)



@app.route("/add-item", methods=["GET", "POST"])
@login_required
@permission_required(Permission.ARCHIVIST)
def add_item():
    form = AddItemForm(request.form)

    collections = fetch_collections()

    form.collection_id.choices = [("", "Select Collection")]
    form.collection_id.choices += [
        (collection["collection_id"], collection["name"])
        for collection in collections
    ]

    if request.method == "POST":
        dataArray = {}
        dataArray["title"] = request.form.get("title")
        dataArray["description"] = request.form.get("description")
        dataArray["item_type"] = request.form.get("item_type")
        dataArray["record_format"] = request.form.get("record_format")
        dataArray["place"] = request.form.get("place")
        language_name = request.form.get("language_group")
        language_group = get_language_group_id_by_name(language_name)   
        dataArray["language_group"] = language_group['languageGroupID']
        dataArray["collection_id"] = request.form.get("collection_id")

        file_record = request.files.get("file_record")
        collection_img = request.files.get("item_img")
        dataArray["userID"] = current_user.userID
        dataArray["date_added"] = date.today().strftime("%Y-%m-%d")
        dataArray["item_id"] = next_id("CollectionItem", "itemID", "I")
        dataArray["meta_id"] = next_id("culturalmetadata", "metadataID", "M")
        dataArray["assessment_id"] = next_id("assessmentrecord", "assessmentID", "A")
        dataArray["img_path"] = "img/placeholder.png"
        dataArray["record_path"] = None

        if collection_img and collection_img.filename:
            if allowed_file(collection_img.filename, ALLOWED_IMG_EXTENSIONS):
                original_img_name = secure_filename(collection_img.filename)
                img_ext = original_img_name.rsplit(".", 1)[1].lower()
                img_filename = f"{uuid4().hex}.{img_ext}"

                collection_img.save(app.config["UPLOAD_FOLDER"] / img_filename)

                dataArray["img_path"] = f"uploads/{img_filename}"
     
        if file_record and file_record.filename:
            if allowed_file(file_record.filename, ALLOWED_EXTENSIONS):
                original_file_name = secure_filename(file_record.filename)
                file_ext = original_file_name.rsplit(".", 1)[1].lower()
                filename = f"{uuid4().hex}.{file_ext}"
                file_record.save(app.config["UPLOAD_FOLDER"] / filename)
                dataArray["record_path"] = f"uploads/{filename}"
            else:
                flash("Invalid record file type.", "danger")
                return redirect(url_for("add_item"))
        else:
            flash("You must upload a record file.", "danger")
            return redirect(url_for("add_item"))

        success = add_new_item(dataArray)

        if success:
            flash("Item added successfully.", "success")
            return redirect(url_for("add_item"))

        flash("Item could not be added.", "danger")
        return redirect(url_for("add_item"))
    language_groups = get_language_groups()
    return render_template("item_add.html", collections=collections, languages=language_groups, form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash("Thanks for your message, we'll be in touch soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

@app.route("/item/<item_id>/update", methods=["POST"])
@login_required
@permission_required(Permission.ARCHIVIST)
def update_item_details(item_id):
    language_name = request.form.get("language_group")
    language_group = get_language_group_id_by_name(language_name) 
    update_item(
        item_id,
        request.form.get("title"),
        request.form.get("description"),
        request.form.get("item_type"),
        request.form.get("place"),
        language_group['languageGroupID'],
        request.form.get("item_format"),
        request.form.get("date_recorded"),
        )
    flash("Item details updated successfully.", "success")
    return redirect(url_for("assessment_item", item_id=item_id))

@app.route("/item/<item_id>/delete", methods=["POST"])
@login_required
@is_administrator
def delete_item_route(item_id):
    delete_item(item_id)
    flash("Item deleted successfully.", "success")
    return redirect(url_for("assessments"))