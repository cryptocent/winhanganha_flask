from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField 
from wtforms.validators import Length, DataRequired, Email, EqualTo



class RegistrationForm(Form):
    name = StringField("Name", [Length(min=4, max=25)])
    email = StringField("Email Address", [Length(min=6, max=100)])
    password = PasswordField(
        "New Password",
        [
            DataRequired(),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I accept the TOS", [DataRequired()])


class MetadataForm(Form):
    access_decision = StringField("Recommended access level", [DataRequired()])
    cultural_notes = StringField("Cultural notes")
    access_conditions = StringField("Access conditions")
    public_description = StringField("Approved public description")


class LoginForm(Form):
    email = StringField("Email Address", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])

class AccessRequestForm(Form):
    name = StringField("Full Name", [DataRequired()])
    email = StringField("Email Address", [DataRequired(), Email()])
    purpose = SelectField(
        'Purpose of request', 
        [DataRequired()],
        choices=[
            ('', ''), 
            ('Research', 'Research'), 
            ('Teaching or learning', 'Teaching or learning'), 
            ('Community or family history', 'Community or family history'), 
            ('Library consultation', 'Library consultation'), 
            ('Other', 'Other')
        ]        
    )
    details = TextAreaField('Purpose of request',)
    submit = SubmitField("Submit Request")
    