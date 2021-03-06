from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators, IntegerField, RadioField
from wtforms import SelectField
from flask_wtf import Form
from flask_wtf.file import FileField

class LoginForm(Form): 
	email = TextField('Email', [validators.Required(), validators.Email()])
	password = PasswordField('Password', [validators.Required()])

class ContactForm(Form):
	page = TextField('Page', [validators.Required()])
	bug = TextAreaField('Bug', [validators.Required()])

class CommentForm(Form):
	comment = TextAreaField('Comment', [validators.Required()])

class AddPostForm(Form):
	post_content = TextField('Content', [validators.Required()])
	post_title = TextField('Content', [validators.Required()])

class EditPostForm(Form):
	new_content = TextField('Content', [validators.Required()])

class SearchForm(Form):
	search_term = TextField('Term', [validators.Required()])

class SignupForm(Form):
	first_name = TextField('First', [validators.Required()])
	last_name = TextField('Last', [validators.Required()])
	password = TextField('Password', [validators.Required()])
	email = TextField('Email', [validators.Required()])
	pw_validation = TextField('Validate', [validators.Required()])
	school_id = TextField('SchoolId', [validators.Length(min=4,max=4)])
	period = SelectField('Class Period', choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
	profile_pic = RadioField('ProfileImage', choices=[('/static/profile_pics/cat1.png','<img class="media-object" src="/static/profile_pics/cat1.png">'),('/static/profile_pics/cat2.png','<img class="media-object" src="/static/profile_pics/cat2.png">'),('/static/profile_pics/cat3.png','<img class="media-object" src="/static/profile_pics/cat3.png">')])
	# profile_pic = TextField('Profile Picture')


class AddAssignmentForm(Form):
	assigned_on = TextField("Assigned On", [validators.Required()])
	due_on = TextField("Due On", [validators.Required()])
	title = TextField("Assignment Title", [validators.Required()])
	category = SelectField('Category', choices=[('CWH','CWH'),('MK','MK'),('AK','AK')])
	link = TextField('Assignment Link')
	description = TextField('Assignment Description')
	group = SelectField('Group', choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4')])
	weight = SelectField('Assignment Weight', choices=[('0','0'),('0.5','0.5'),('1','1'),('1.5','1.5'),('2','2'),('2.5','2.5'),('3','3'),('3.5','3.5'),('4','4'),('4.5','4.5'),('5','5')])

class UploadGradesForm(Form):
	csv_file = TextField("CSV", [validators.Required()])

class UploadNotesForm(Form):
	notes_file = TextField("PDF", [validators.Required()])
	created_on = TextField("Created On", [validators.Required()])
	description = TextField("Description", [validators.Required()])

class AddPhoneForm(Form):
	phone_number = TextField("Phone", [validators.Length(min=10, max=10)])

class SendTextForm(Form):
	text_content = TextAreaField("Text Content", [validators.Required()])	

class ChangePasswordForm(Form):
	old_password = TextField("Old Password", [validators.Required()])
	new_password = TextField("New Password", [validators.Required()])
	new_password_v = TextField("New Password Validator", [validators.Required()])


	
