from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators, FileField

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

class SignupForm(Form):
	first_name = TextField('First', [validators.Required()])
	last_name = TextField('Last', [validators.Required()])
	password = TextField('Password', [validators.Required()])
	school_id = TextField('SchoolId', [validators.Required()])
	period = SelectField('Class Period', choices=[('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
	profile_picture = FileField('Image File')
