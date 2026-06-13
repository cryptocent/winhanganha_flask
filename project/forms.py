from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField 
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
    