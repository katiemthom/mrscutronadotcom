from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators, FileField, SelectField

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
	validate_password = TextField('Validate', [validators.Required()])
	school_id = TextField('SchoolId', [validators.Required()])
	period = SelectField('Class Period', choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
	profile_picture = FileField('Image File')

class AddAssignmentForm(Form):
	assigned_on = TextField("Assigned On", [validators.Required()])
	due_on = TextField("Due On", [validators.Required()])
	assignment_title = TextField("Assignment Title", [validators.Required()])
	category = SelectField('Category', choices=[('CWH','CWH'),('MK','MK'),('AK','AK')])
	assignment_link = TextField('Assignment Link')
	assignment_description = TextField('Assignment Description')
	max_points = TextField('Max Points', [validators.Required()])
	group = SelectField('Group', choices=[('0','0'),('1','1'),('2','2'),('3','3'),('4','4')])
	
