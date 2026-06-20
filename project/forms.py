from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, FileField 
from wtforms.validators import Length, DataRequired, Email, EqualTo



class RegistrationForm(Form):
    preferred_title = SelectField(
        "Preferred Title",
        choices=[
            ("", "Select a title"),
            ("Uncle", "Uncle"),
            ("Aunty", "Aunty"),
            ("Dr.", "Dr"),
            ("Mr", "Mr"),
            ("Mrs", "Mrs"),
            ("Ms", "Ms"),
            ("-", "Prefer not to say"),
        ]
    )
    name = StringField("Full Name", [Length(min=4, max=25)])
    email = StringField("Email Address", [Length(min=6, max=100)])
    password = PasswordField(
        "New Password",
        [
            DataRequired(),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")


class MetadataForm(Form):
    access_decision = StringField("Recommended access level", [DataRequired()])
    cultural_notes = StringField("Cultural notes")
    access_conditions = StringField("Access conditions")
    public_description = StringField("Approved public description")


class LoginForm(Form):
    email = StringField("Email Address", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])

class AccessRequestForm(Form):
    purpose = SelectField(
        "Purpose of request",
        [DataRequired()],
        choices=[
            ("", "Select a purpose"),
            ("Lore","Lore"),
            ("Research", "Research"),
            ("Teaching or learning", "Teaching or learning"),
            ("Community or family history", "Community or family history"),
            ("Library consultation", "Library consultation"),
            ("Other", "Other"),
        ]
    )

    details = TextAreaField("Request details", [DataRequired()])
    submit = SubmitField("Submit Request")

        # title = request.form.get("title")
        # description = request.form.get("description")
        # item_type = request.form.get("item_type")
        # place = request.form.get("place")
        # language_group = request.form.get("language_group")
        # collection_id = request.form.get("collection_id")
        # file_record = request.files.get("file_record")
        # collection_img = request.files.get("collection_img")

class ContactForm(FlaskForm):
    name = StringField("Full Name", [DataRequired(), Length(min=2, max=100)])
    email = StringField("Email Address", [DataRequired(), Email()])
    subject = StringField("Subject", [DataRequired(), Length(min=2, max=150)])
    message = TextAreaField("Message", [DataRequired(), Length(min=10)])
    submit = SubmitField("Send Message")
    
class AddItemForm(Form):
    collection_id = SelectField(
        "Parent Collection",
        [DataRequired()],
        choices=[]
    )
    title = StringField("Title", [DataRequired()])
    description = TextAreaField("Description", [DataRequired()])
    item_type = SelectField(
        "Item Type",
        validators=[DataRequired()],
        choices=[
            ("", "Select an item type"),
            ("Audio", "Audio"),
            ("Video", "Video"),
            ("Image", "Image"),
            ("Document", "Document"),
            ("Language Record", "Language Record"),
            ("Place Record", "Place Record"),
            ("Oral History", "Oral History"),
            ("Transcript", "Transcript"),
            ("Cultural Note", "Cultural Note"),
            ("Community Record", "Community Record"),
            ("Collection Record", "Collection Record"),
            ("Other", "Other"),
        ]
    )
    record_format = SelectField(
    "Format",
    validators=[DataRequired()],
    choices=[
        ("", "Select a format"),
        ("Audio recording", "Audio recording"),
        ("Video recording", "Video recording"),
        ("Digitised image", "Digitised image"),
        ("Digitised document", "Digitised document"),
        ("Digitised text record", "Digitised text record"),
        ("PDF document", "PDF document"),
        ("Word document", "Word document"),
        ("Spreadsheet", "Spreadsheet"),
        ("Presentation", "Presentation"),
        ("Audio transcript", "Audio transcript"),
        ("Video transcript", "Video transcript"),
        ("Audio transcript and cultural note", "Audio transcript and cultural note"),
        ("Photograph", "Photograph"),
        ("Map", "Map"),
        ("Place name record", "Place name record"),
        ("Language word list", "Language word list"),
        ("Community meeting notes", "Community meeting notes"),
        ("Consultation record", "Consultation record"),
        ("Cultural access note", "Cultural access note"),
        ("Archive metadata record", "Archive metadata record"),
        ("Other format", "Other format"),
    ]
)
    place = StringField("Place")
    language_group = TextAreaField("Language Group/Nation")
    file_record = FileField("Item File", [DataRequired()])
    item_img = FileField("Collection Item Image")
    submit = SubmitField("Submit Item")
 
class CancelUserRequest(Form):
    cancel = SubmitField("Cancel Request")
    

# class AdminPermissionForm(Form):
#     permission = SelectField(
#         "Role",
#         choices=[],
#         coerce=int,
#         validators=[DataRequired()]
#     )

class AssessmentForm(Form):
    final_decision = SelectField(
        "Decision Required",
        [DataRequired()],
        choices=[
            ("", "Select a decision"),
            ("Decision pending","Decision pending"),
            ("Release publicly", "Release publicly"),
            ("Release with restricted access", "Release with restricted access"),
            ("Keep private", "Keep private"),
            ("Library consultation", "Library consultation"),
            ("Return for further consultation", "Return for further consultation"),
        ]
    )
    decision_reason = StringField("Decision Reason")


class AccessRequestDecisionForm(Form):
    final_decision = SelectField(
        "Access Request Decision",
        [DataRequired()],
        choices=[
            ("", "Select a decision"),
            ("Pending","Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
            ("Cancel", "Cancel"),
        ]
    )

    