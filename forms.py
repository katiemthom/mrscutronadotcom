from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators, IntegerField
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
	profile_picture = FileField('Image File')

class AddAssignmentForm(Form):
	assigned_on = TextField("Assigned On", [validators.Required()])
	due_on = TextField("Due On", [validators.Required()])
	title = TextField("Assignment Title", [validators.Required()])
	category = SelectField('Category', choices=[('CWH','CWH'),('MK','MK'),('AK','AK')])
	link = TextField('Assignment Link')
	description = TextField('Assignment Description')
	group = SelectField('Group', choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4')])

class UploadGradesForm(Form):
	csv_file = FileField("CSV", [validators.Required()])

class UploadNotesForm(Form):
	notes_file = FileField("PDF", [validators.Required()])
	created_on = TextField("Created On", [validators.Required()])
	description = TextField("Description", [validators.Required()])

class AddPhoneForm(Form):
	phone_number = TextField("Phone", [validators.Length(min=10, max=10)])


	
