from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, validators

class LoginForm(Form): 
	email = TextField('Email', [validators.Required(), validators.Email()])
	password = PasswordField('Password', [validators.Required()])

class ContactForm(Form):
	page = TextField('Page', [validators.Required()])
	bug = TextAreaField('Bug', [validators.Required()])
