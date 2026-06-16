from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, FileField, DateField, HiddenField 
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
    file_record = FileField("Item File", [DataRequired()])
    item_img = FileField("Collection Item Image")
    date_recorded = DateField("Date Recorded", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Submit Item")
    
    language_group = SelectField(
        "Language Group/Nation",
        validators=[DataRequired()],
        choices=[
            ("", "Select a language group"),

            ("Aboriginal English", "Aboriginal English"),
            ("Adnyamathanha", "Adnyamathanha"),
            ("Alyawarr", "Alyawarr"),
            ("Anindilyakwa", "Anindilyakwa"),
            ("Anmatyerr", "Anmatyerr"),
            ("Arabana", "Arabana"),
            ("Arrernte", "Arrernte"),
            ("Awabakal", "Awabakal"),
            ("Banyjima", "Banyjima"),
            ("Bardi", "Bardi"),
            ("Barngarla", "Barngarla"),
            ("Bidawal", "Bidawal"),
            ("Bininj Kunwok", "Bininj Kunwok"),
            ("Birpai / Biripi", "Birpai / Biripi"),
            ("Boonwurrung / Bunurong", "Boonwurrung / Bunurong"),
            ("Bundjalung", "Bundjalung"),
            ("Bunuba", "Bunuba"),
            ("Butchulla", "Butchulla"),
            ("Darkinjung", "Darkinjung"),
            ("Dharawal / Tharawal", "Dharawal / Tharawal"),
            ("Dharug / Darug", "Dharug / Darug"),
            ("Dhudhuroa", "Dhudhuroa"),
            ("Dhuwaya", "Dhuwaya"),
            ("Dja Dja Wurrung", "Dja Dja Wurrung"),
            ("Djab Wurrung", "Djab Wurrung"),
            ("Djabugay", "Djabugay"),
            ("Djambarrpuyngu", "Djambarrpuyngu"),
            ("Dunghutti / Thungutti", "Dunghutti / Thungutti"),
            ("Eora", "Eora"),
            ("Erub Mer", "Erub Mer"),
            ("Gadigal", "Gadigal"),
            ("Gamilaraay / Kamilaroi", "Gamilaraay / Kamilaroi"),
            ("Gomeroi", "Gomeroi"),
            ("Gooniyandi", "Gooniyandi"),
            ("Gooreng Gooreng", "Gooreng Gooreng"),
            ("Gumbaynggirr", "Gumbaynggirr"),
            ("Gumatj", "Gumatj"),
            ("Gunaikurnai / Kurnai", "Gunaikurnai / Kurnai"),
            ("Gunditjmara", "Gunditjmara"),
            ("Gundungurra", "Gundungurra"),
            ("Gurang Gurang", "Gurang Gurang"),
            ("Gurindji", "Gurindji"),
            ("Guugu Yimithirr", "Guugu Yimithirr"),
            ("Iwaidja", "Iwaidja"),
            ("Jawi", "Jawi"),
            ("Jawoyn", "Jawoyn"),
            ("Kabi Kabi / Gubbi Gubbi", "Kabi Kabi / Gubbi Gubbi"),
            ("Kaiwaligau Ya / Kowrareg", "Kaiwaligau Ya / Kowrareg"),
            ("Kala Lagaw Ya", "Kala Lagaw Ya"),
            ("Kalau Lagau Ya", "Kalau Lagau Ya"),
            ("Kalaw Kawaw Ya", "Kalaw Kawaw Ya"),
            ("Kalaw Lagaw Ya", "Kalaw Lagaw Ya"),
            ("Kalkadoon", "Kalkadoon"),
            ("Karajarri", "Karajarri"),
            ("Kartujarra", "Kartujarra"),
            ("Kaurna", "Kaurna"),
            ("Kaytetye", "Kaytetye"),
            ("Kija", "Kija"),
            ("Kokatha", "Kokatha"),
            ("Kuku Yalanji", "Kuku Yalanji"),
            ("Kulkalgau Ya", "Kulkalgau Ya"),
            ("Kunwinjku", "Kunwinjku"),
            ("Kuuku Ya'u", "Kuuku Ya'u"),
            ("Luritja", "Luritja"),
            ("Manyjilyjarra", "Manyjilyjarra"),
            ("Martu Wangka", "Martu Wangka"),
            ("Maung", "Maung"),
            ("Meriam Mer", "Meriam Mer"),
            ("Meriam Mir", "Meriam Mir"),
            ("Miriwoong", "Miriwoong"),
            ("Mirning", "Mirning"),
            ("Murrinh-Patha", "Murrinh-Patha"),
            ("Narangga", "Narangga"),
            ("Ngambri", "Ngambri"),
            ("Ngarluma", "Ngarluma"),
            ("Ngarrindjeri", "Ngarrindjeri"),
            ("Ngarigo", "Ngarigo"),
            ("Ngiyampaa", "Ngiyampaa"),
            ("Ngunnawal", "Ngunnawal"),
            ("Noongar / Nyungar", "Noongar / Nyungar"),
            ("Nukunu", "Nukunu"),
            ("Nunggubuyu", "Nunggubuyu"),
            ("Nyiyaparli", "Nyiyaparli"),
            ("Nyulnyul", "Nyulnyul"),
            ("Paakantyi / Barkindji", "Paakantyi / Barkindji"),
            ("palawa kani", "palawa kani"),
            ("Pitjantjatjara", "Pitjantjatjara"),
            ("Ritharrngu", "Ritharrngu"),
            ("Taungurung", "Taungurung"),
            ("Tiwi", "Tiwi"),
            ("Turrbal", "Turrbal"),
            ("Umpila", "Umpila"),
            ("Wadawurrung / Wathaurong", "Wadawurrung / Wathaurong"),
            ("Wailwan / Wayilwan", "Wailwan / Wayilwan"),
            ("Wakka Wakka", "Wakka Wakka"),
            ("Walmajarri", "Walmajarri"),
            ("Wardaman", "Wardaman"),
            ("Warlpiri", "Warlpiri"),
            ("Warumungu", "Warumungu"),
            ("Wemba Wemba", "Wemba Wemba"),
            ("Wergaia / Wotjobaluk", "Wergaia / Wotjobaluk"),
            ("Western Desert Language", "Western Desert Language"),
            ("Wik Mungkan", "Wik Mungkan"),
            ("Wiradjuri", "Wiradjuri"),
            ("Wirangu", "Wirangu"),
            ("Woi Wurrung / Wurundjeri", "Woi Wurrung / Wurundjeri"),
            ("Wongaibon", "Wongaibon"),
            ("Worimi", "Worimi"),
            ("Yaegl", "Yaegl"),
            ("Yaitmathang", "Yaitmathang"),
            ("Yamatji", "Yamatji"),
            ("Yankunytjatjara", "Yankunytjatjara"),
            ("Yawuru", "Yawuru"),
            ("Yidinji", "Yidinji"),
            ("Yindjibarndi", "Yindjibarndi"),
            ("Yinhawangka", "Yinhawangka"),
            ("Yolngu Matha", "Yolngu Matha"),
            ("Yorta Yorta", "Yorta Yorta"),
            ("Yugambeh", "Yugambeh"),
            ("Yuggera / Jagera", "Yuggera / Jagera"),
            ("Yuin", "Yuin"),
            ("Yumplatok / Torres Strait Creole", "Yumplatok / Torres Strait Creole"),

            # General options
            ("Multiple language groups", "Multiple language groups"),
            ("Unknown", "Unknown"),
            ("Not yet assessed", "Not yet assessed"),
            ("Other / Not listed", "Other / Not listed"),
        ]
)
    
    
    
 
class CancelUserRequest(Form):
    cancel = SubmitField("Cancel Request")
    

class MetadataForm(Form):
    form_name = HiddenField(default="metadata_form")
    title = StringField("Item title")
    description = TextAreaField("Item description")
    access_level = SelectField(
        "Access level",
        choices=[
            ("", ""),
            ("Public", "Public"),
            ("Restricted", "Restricted"),
            ("Private", "Private"),
        ],
    )
    cultural_sensitivity = SelectField(
        "Cultural sensitivity",
        choices=[
            ("", ""),
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low"),
            ("Not yet assessed", "Not yet assessed"),
        ],
    )
    approval_status = SelectField(
        "Approval status",
        choices=[
            ("", ""),
            ("Under Assessment", "Under Assessment"),
            ("Restricted", "Restricted"),
            ("Private", "Private"),
            ("Approved", "Approved"),
            ("Remove", "Remove from Archive"),
        ],
    )
    ownership = SelectField(
        "Ownership",
        choices=[
            ("", ""),
            ("Community owned", "Community owned"),
            ("Family owned", "Family owned"),
            ("Individual owned", "Individual owned"),
            ("Organisation owned", "Organisation owned"),
            ("Library held", "Library held"),
            ("Unknown", "Unknown"),
            ("Not yet assessed", "Not yet assessed"),
        ],
    )
    cultural_notes = TextAreaField("Cultural notes")
    access_conditions = TextAreaField("Access conditions")
    item_handling = TextAreaField("Item handling details")
    submit = SubmitField("Save item data")
    place = StringField("Place")
    language_group = SelectField(
        "Language Group/Nation",
        validators=[DataRequired()],
        choices=[
            ("", "Select a language group"),

            ("Aboriginal English", "Aboriginal English"),
            ("Adnyamathanha", "Adnyamathanha"),
            ("Alyawarr", "Alyawarr"),
            ("Anindilyakwa", "Anindilyakwa"),
            ("Anmatyerr", "Anmatyerr"),
            ("Arabana", "Arabana"),
            ("Arrernte", "Arrernte"),
            ("Awabakal", "Awabakal"),
            ("Banyjima", "Banyjima"),
            ("Bardi", "Bardi"),
            ("Barngarla", "Barngarla"),
            ("Bidawal", "Bidawal"),
            ("Bininj Kunwok", "Bininj Kunwok"),
            ("Birpai / Biripi", "Birpai / Biripi"),
            ("Boonwurrung / Bunurong", "Boonwurrung / Bunurong"),
            ("Bundjalung", "Bundjalung"),
            ("Bunuba", "Bunuba"),
            ("Butchulla", "Butchulla"),
            ("Darkinjung", "Darkinjung"),
            ("Dharawal / Tharawal", "Dharawal / Tharawal"),
            ("Dharug / Darug", "Dharug / Darug"),
            ("Dhudhuroa", "Dhudhuroa"),
            ("Dhuwaya", "Dhuwaya"),
            ("Dja Dja Wurrung", "Dja Dja Wurrung"),
            ("Djab Wurrung", "Djab Wurrung"),
            ("Djabugay", "Djabugay"),
            ("Djambarrpuyngu", "Djambarrpuyngu"),
            ("Dunghutti / Thungutti", "Dunghutti / Thungutti"),
            ("Eora", "Eora"),
            ("Erub Mer", "Erub Mer"),
            ("Gadigal", "Gadigal"),
            ("Gamilaraay / Kamilaroi", "Gamilaraay / Kamilaroi"),
            ("Gomeroi", "Gomeroi"),
            ("Gooniyandi", "Gooniyandi"),
            ("Gooreng Gooreng", "Gooreng Gooreng"),
            ("Gumbaynggirr", "Gumbaynggirr"),
            ("Gumatj", "Gumatj"),
            ("Gunaikurnai / Kurnai", "Gunaikurnai / Kurnai"),
            ("Gunditjmara", "Gunditjmara"),
            ("Gundungurra", "Gundungurra"),
            ("Gurang Gurang", "Gurang Gurang"),
            ("Gurindji", "Gurindji"),
            ("Guugu Yimithirr", "Guugu Yimithirr"),
            ("Iwaidja", "Iwaidja"),
            ("Jawi", "Jawi"),
            ("Jawoyn", "Jawoyn"),
            ("Kabi Kabi / Gubbi Gubbi", "Kabi Kabi / Gubbi Gubbi"),
            ("Kaiwaligau Ya / Kowrareg", "Kaiwaligau Ya / Kowrareg"),
            ("Kala Lagaw Ya", "Kala Lagaw Ya"),
            ("Kalau Lagau Ya", "Kalau Lagau Ya"),
            ("Kalaw Kawaw Ya", "Kalaw Kawaw Ya"),
            ("Kalaw Lagaw Ya", "Kalaw Lagaw Ya"),
            ("Kalkadoon", "Kalkadoon"),
            ("Karajarri", "Karajarri"),
            ("Kartujarra", "Kartujarra"),
            ("Kaurna", "Kaurna"),
            ("Kaytetye", "Kaytetye"),
            ("Kija", "Kija"),
            ("Kokatha", "Kokatha"),
            ("Kuku Yalanji", "Kuku Yalanji"),
            ("Kulkalgau Ya", "Kulkalgau Ya"),
            ("Kunwinjku", "Kunwinjku"),
            ("Kuuku Ya'u", "Kuuku Ya'u"),
            ("Luritja", "Luritja"),
            ("Manyjilyjarra", "Manyjilyjarra"),
            ("Martu Wangka", "Martu Wangka"),
            ("Maung", "Maung"),
            ("Meriam Mer", "Meriam Mer"),
            ("Meriam Mir", "Meriam Mir"),
            ("Miriwoong", "Miriwoong"),
            ("Mirning", "Mirning"),
            ("Murrinh-Patha", "Murrinh-Patha"),
            ("Narangga", "Narangga"),
            ("Ngambri", "Ngambri"),
            ("Ngarluma", "Ngarluma"),
            ("Ngarrindjeri", "Ngarrindjeri"),
            ("Ngarigo", "Ngarigo"),
            ("Ngiyampaa", "Ngiyampaa"),
            ("Ngunnawal", "Ngunnawal"),
            ("Noongar / Nyungar", "Noongar / Nyungar"),
            ("Nukunu", "Nukunu"),
            ("Nunggubuyu", "Nunggubuyu"),
            ("Nyiyaparli", "Nyiyaparli"),
            ("Nyulnyul", "Nyulnyul"),
            ("Paakantyi / Barkindji", "Paakantyi / Barkindji"),
            ("palawa kani", "palawa kani"),
            ("Pitjantjatjara", "Pitjantjatjara"),
            ("Ritharrngu", "Ritharrngu"),
            ("Taungurung", "Taungurung"),
            ("Tiwi", "Tiwi"),
            ("Turrbal", "Turrbal"),
            ("Umpila", "Umpila"),
            ("Wadawurrung / Wathaurong", "Wadawurrung / Wathaurong"),
            ("Wailwan / Wayilwan", "Wailwan / Wayilwan"),
            ("Wakka Wakka", "Wakka Wakka"),
            ("Walmajarri", "Walmajarri"),
            ("Wardaman", "Wardaman"),
            ("Warlpiri", "Warlpiri"),
            ("Warumungu", "Warumungu"),
            ("Wemba Wemba", "Wemba Wemba"),
            ("Wergaia / Wotjobaluk", "Wergaia / Wotjobaluk"),
            ("Western Desert Language", "Western Desert Language"),
            ("Wik Mungkan", "Wik Mungkan"),
            ("Wiradjuri", "Wiradjuri"),
            ("Wirangu", "Wirangu"),
            ("Woi Wurrung / Wurundjeri", "Woi Wurrung / Wurundjeri"),
            ("Wongaibon", "Wongaibon"),
            ("Worimi", "Worimi"),
            ("Yaegl", "Yaegl"),
            ("Yaitmathang", "Yaitmathang"),
            ("Yamatji", "Yamatji"),
            ("Yankunytjatjara", "Yankunytjatjara"),
            ("Yawuru", "Yawuru"),
            ("Yidinji", "Yidinji"),
            ("Yindjibarndi", "Yindjibarndi"),
            ("Yinhawangka", "Yinhawangka"),
            ("Yolngu Matha", "Yolngu Matha"),
            ("Yorta Yorta", "Yorta Yorta"),
            ("Yugambeh", "Yugambeh"),
            ("Yuggera / Jagera", "Yuggera / Jagera"),
            ("Yuin", "Yuin"),
            ("Yumplatok / Torres Strait Creole", "Yumplatok / Torres Strait Creole"),

            # General options
            ("Multiple language groups", "Multiple language groups"),
            ("Unknown", "Unknown"),
            ("Not yet assessed", "Not yet assessed"),
            ("Other / Not listed", "Other / Not listed"),
        ]
    )
    
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
     
class CommentForm(Form):
    form_name = HiddenField(default="comment_form")

    comment_text = TextAreaField(
        "Add discussion note",
        validators=[DataRequired()]
    )

    submit = SubmitField("Add note")