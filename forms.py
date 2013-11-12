from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators

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
