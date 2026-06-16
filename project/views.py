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
from project import ALLOWED_EXTENSIONS, ALLOWED_IMG_EXTENSIONS, app
from project.decorators import permission_required, is_administrator
from project.forms import LoginForm, MetadataForm, RegistrationForm, AccessRequestForm, AddItemForm, CancelUserRequest, CommentForm
from project.models import (
    Permission,
    User,
    add_new_item,
    add_item_comment,
    allowed_file,
    cancel_user_request,
    create_user,
    fetch_access_level_filters,
    fetch_all_roles,
    fetch_collections,
    fetch_item_comments,
    fetch_filtered_items,
    fetch_item,
    fetch_item_type_filters,
    update_meta_data,
    fetch_review_status_filters,
    fetch_role_by_permission,
    fetch_user_request,
    fetch_user_request_by_ID,
    fetch_user_requests,
    get_assessment_rows,
    get_featured_items,
    load_users,
    secure_filename,
    submit_access_request,
    update_user_permissions,
    verify_user_password,
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

        if not current_user.can(Permission.REVIEWER):
            abort(403)

    request_row = None

    if current_user.is_authenticated:
        request_row = fetch_user_request(current_user.id,item_id)

    if request.method == "POST" and form.validate():
        request_array = {}
        if session.get("userID") is None:
            flash("You must be logged in to request access.", "warning")
            return redirect(url_for("login"))
        
       
        purpose = form.purpose.data.strip()
        details = form.details.data.strip()
        request_array["full_purpose"] = purpose if not details else f"{purpose}: {details}"
        request_array["current_user"] = current_user.userID
        request_array["request_date"] = date.today().isoformat()
        request_array["item_id"] = item_id

        success = submit_access_request(request_array)
        
        if success:
            flash("Your request has been received. You will be notified of the request outcome", "success")
            return redirect(url_for("item_detail", item_id=item_id))
        else:
            flash("Your request failed, please try again", "warning")
            return redirect(url_for("item_detail", item_id=item_id))
    
    return render_template("item_detail.html", item=item, form=form, access_request=request_row)


@app.route("/item-assessments")
@login_required
@permission_required(Permission.REVIEWER)
def assessments():
    assessment_rows = get_assessment_rows()
       
    return render_template("item_assessment_list.html", assessments=assessment_rows)





@app.route("/item-assessment/<item_id>", methods=["GET", "POST"])
@login_required
@permission_required(Permission.REVIEWER)
def assessment_item(item_id):
    assessment_row = fetch_item(item_id)

    if assessment_row is None:
        abort(404)

    if request.method == "POST":
        form_name = request.form.get("form_name")

        if form_name == "metadata_form":
            assessment_form = MetadataForm(request.form)

            if assessment_form.validate():
                update_meta_data(assessment_form, item_id)
                if request.form.get("status") == "Remove":
                    flash("Item Removed from Archive.", "success")
                    return redirect(url_for("items"))
                flash("Item Data Updated.", "success")
                return redirect(url_for("assessment_item", item_id=item_id))

        elif form_name == "comment_form":
            comment_text = request.form.get("comment_text", "").strip()

            if comment_text:
                add_item_comment(
                    item_id=item_id,                    
                    comment_text=comment_text,
                    user=current_user.userID,
                    date_added = date.today().strftime("%Y-%m-%d")
                )
            flash("Comment added.", "success")
            return redirect(url_for("assessment_item", item_id=item_id))

    assessment_form = MetadataForm(data={
        "title": assessment_row["title"],
        "description": assessment_row["description"],
        "access_level": assessment_row["access_level"],
        "cultural_sensitivity": assessment_row["cultural_sensitivity"],
        "approval_status": assessment_row["status"],
        "cultural_notes": assessment_row["cultural_notes"],
        "access_conditions": assessment_row["access_conditions"],
        "ownership": assessment_row["ownership"],
        "item_handling": assessment_row["item_handling"],
        "language_group": assessment_row["language_group"],
        "place": assessment_row["place"],
        "record_format": assessment_row["format"],
        "item_type": assessment_row["item_type"],
    })

    comments = fetch_item_comments(item_id)
    comment_form = CommentForm()
    return render_template(
        "item_assessment.html",
        assessment=assessment_row,
        notes=comments,
        form=assessment_form,
        comment_form=comment_form
    )



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
            permission = fetch_role_by_permission(user_row["permissions"])
            user = User(user_row["userID"], permission, user_row["preferred_title"], user_row["name"], user_row["email"])
            login_user(user)

            session["userID"] = user_row["userID"]
            session["role"] = permission
            session["preferred_title"] = user_row["preferred_title"]
            session["name"] = user_row["name"]
            session["email"] = user_row["email"]

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
        update_user_permissions(user_id,new_role["permissions"])
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
        dataArray["language_group"] = request.form.get("language_group")
        dataArray["collection_id"] = request.form.get("collection_id")
        dataArray["date_recorded"] = form.date_recorded.data.strftime("%Y-%m-%d")

        file_record = request.files.get("file_record")
        collection_img = request.files.get("item_img")

        dataArray["date_added"] = date.today().strftime("%Y-%m-%d")

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

    return render_template("item_add.html", collections=collections, form=form)
