from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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
app.config['MAIL_SERVER'] = 'mail.mrscutrona.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bugs@mrscutrona.com'
app.config['MAIL_PASSWORD'] = config.epw
mail.init_app(app)
PER_PAGE = 5
def url_for_other_page(page):
	args = dict(request.view_args.items() + request.args.to_dict().items())
	args['page'] = page
	return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
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
	featured_posts = model.get_featured_posts()
	print featured_posts[0].user.profile_picture
	recent_posts = model.get_recent_posts()
	return render_template('blogs.html', user=current_user, featured_posts=featured_posts, recent_posts=recent_posts)

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
		msg = Message('bug report', sender='bugs@mrscutrona.com', recipients=['katiemthom@gmail.com'])
		msg.body = """
		Page: %s
		%s
		""" % (page,bug)
		mail.send(msg)
		return redirect('/reportbug')

@app.route('/blog/<int:author_id>', defaults={'page':1})
@app.route('/blog/<int:author_id>/<int:page>')
def show_blog(author_id, page):
	count = model.count_all_posts(author_id)
	posts = model.get_posts_for_page(author_id, page, PER_PAGE, count)
	pagination = model.Pagination(page, PER_PAGE, count)
	return render_template('blog.html', posts=posts, user=current_user, pagination=pagination)

@app.route('/post/<int:post_id>')
def show_post(post_id):
	post = model.get_post_by_id(post_id)
	comments = model.get_comments_by_post_id(post_id)
	return render_template('post.html', post=post, user=current_user, comments=comments)
########## end login-not-required views ##########

########## login-required views ##########
@app.route('/myblog/', defaults={'page':1})
@app.route('/myblog/page/<int:page>')
@login_required
def show_posts(page):
	count = model.count_all_posts(current_user.user_id)
	posts = model.get_posts_for_page(current_user.user_id, page, PER_PAGE, count)
	pagination = model.Pagination(page, PER_PAGE, count)
	return render_template('myblog.html', pagination=pagination,posts = posts, user = current_user)

@app.route('/mygrades')
@login_required
def show_grades():
	grades = model.get_grades_by_user_id(current_user.id)
	return render_template('mygrades.html',grades=grades,user=current_user)

@app.route('/post/<int:post_pk>', methods=['POST'])
@login_required
def comment(post_pk):
	new_comment = model.add_comment(request.form.get('user_id'),request.form.get('post_pk'),request.form.get('comment'))
	return jsonify({
		'comment_author': new_comment.user.first_name,
		'comment_content': new_comment.content,
		'comment_timestamp': new_comment.timestamp})

@app.route('/addpost')
@login_required
def show_add_post():
	return render_template('addpost.html', user=current_user)

@app.route('/addpost', methods=['POST'])
@login_required
def add_post():
	form = forms.AddPostForm(request.form)
	if form.validate() == False: 
		flash('All fields are required.')
		return render_template('addpost.html')
	else:
		content = form.post_content.data
		title = form.post_title.data
		new_post = model.add_post(current_user.user_id, content, title)
	return redirect('/myblog')

########## end login-required views ##########

if __name__ == "__main__":
    app.run(debug = True)
