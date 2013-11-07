from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from model import User, session
from flask.ext.mail import Message, Mail 

import model
import os 
import config
import forms 

########## Flask Setup ##########
mail = Mail()
app = Flask(__name__)
app.config.from_object(config)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'katiemthom@gmail.com'
app.config['MAIL_PASSWORD'] = config.epw
mail.init_app(app)
########## end Flask Setup ##########

########## Login Manager to make login easier ##########
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'show_blogs'

@login_manager.user_loader
def load_user(user_id):
	return model.get_user_by_id(user_id)
########## end Login Manager to make login easier ##########

########## main views ##########
@app.route('/')
def index():
	return render_template('index.html', user = current_user)

@app.route('/', methods=['POST'])
def process_login(): 
	form = forms.LoginForm(request.form)
	if not form.validate():
		flash('Incorrect username or password')
		return render_template('index.html')
	email = form.email.data
	password = form.password.data 
	user = session.query(User).filter_by(email=email).first()
	if not user or not user.authenticate(password):
		flash('Incorrect username or password')
		return render_template('index.html')
	login_user(user)
	return redirect(url_for('show_notes'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
########## end main views ##########

########## login-not-required views ##########
@app.route('/notes')
def show_notes():
	notes = model.get_notes()
	return render_template('notes.html', notes = notes, user = current_user)

@app.route('/blogs')
def show_blogs():
	posts = model.get_posts()

	return render_template('blogs.html', user=current_user, posts=posts)

@app.route('/classes')
def show_classes():
	return render_template('classes.html', user=current_user)

@app.route('/reportbug')
def report_bug():
	return render_template('reportbug.html', user=current_user)

@app.route('/reportbug', methods=['POST'])
def send_bug():
	form = forms.ContactForm(request.form)
	if form.validate() == False: 
		flash('All fields are required.')
		return render_template('reportbug.html')
	else:
		page = form.page.data
		bug = form.bug.data
		msg = Message('bug report', sender='katiemthom@gmail.com', recipients=['katiemthom@gmail.com'])
		msg.body = """
		Page: %s
		%s
		""" % (page,bug)
		mail.send(msg)
		return redirect('/reportbug')

@app.route('/blog/<int:author_id>')
def show_blog(author_id):
	posts = model.get_posts_by_user_id(author_id)
	author = model.get_user_by_id(author_id)
	return render_template('blog.html', posts=posts, user=current_user, author=author)
########## end login-not-required views ##########

########## login-required views ##########
@app.route('/myblog')
@login_required
def show_posts():
	posts = model.get_posts_by_user_id(current_user.id)
	return render_template('myblog.html', posts = posts, user = current_user)

@app.route('/mygrades')
@login_required
def show_grades():
	grades = model.get_grades_by_user_id(current_user.id)
	return render_template('mygrades.html',grades=grades,user=current_user)
########## end login-required views ##########

if __name__ == "__main__":
    app.run(debug = True)
