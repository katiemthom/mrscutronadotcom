########## Import ##########
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from model import User, session
from flask.ext.mail import Message, Mail 
from flaskext.markdown import Markdown
from werkzeug import secure_filename

import model
import os 
import config
import forms 
########## end Import ##########

########## Flask Setup ##########
app = Flask(__name__)
app.config.from_object(config)
Markdown(app)
########## end Flask Setup ##########

########## File Upload Setup ##########
UPLOAD_FOLDER = '/static/profile_pics'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
########## end File Upload Setup ##########

########## Mail Setup ##########
mail = Mail()
app.config['MAIL_SERVER'] = 'mail.mrscutrona.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bugs@mrscutrona.com'
app.config['MAIL_PASSWORD'] = config.epw
mail.init_app(app)
########## end Mail Setup ##########

########## Pagination Setup ##########
PER_PAGE = 5
def url_for_other_page(page):
	args = dict(request.view_args.items() + request.args.to_dict().items())
	args['page'] = page
	return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
########## end Pagination Setup ##########

########## Date Formatter ########## 
def format_date(dt):
	# return dt.strftime('%B %d, %Y %I:%M %p')
	return dt.strftime('%Y-%m-%d %H:%M UTC')
app.jinja_env.globals['format_date'] = format_date
########## End Date Formatter ########## 

########## Login Manager to make login easier ##########
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
	return model.get_user_by_id(user_id)
########## end Login Manager to make login easier ##########

########## signin and signup views ##########
@app.route('/uploadpic', methods=['GET', 'POST'])
def upload_img():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print filename
			return render_template('upload_pic.html')
	else: 
		return render_template('upload_pic.html')


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
	return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))
########## end main views ##########

########## other views ##########
@app.route('/notes')
def show_notes():
	notes = model.get_notes()
	return render_template('notes.html', notes = notes, user = current_user)

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
		flash('All fields are required.','warning')
		return render_template('reportbug.html',  user=current_user)
	else:
		page = form.page.data
		bug = form.bug.data
		msg = Message('bug report', sender='bugs@mrscutrona.com', recipients=['katiemthom@gmail.com'])
		msg.body = "Page: %s Body: %s" % (page,bug)
		mail.send(msg)
		flash('Message sent!','success')
		return render_template('reportbug.html', user=current_user)

@app.route('/mygrades')
@login_required
def show_grades():
	grades = model.get_grades_by_user_id(current_user.id)
	return render_template('mygrades.html',grades=grades,user=current_user)
########## end other views ##########

########## blog views ##########
@app.route('/blogs')
def show_blogs():
	featured_posts = model.get_featured_posts()
	recent_posts = model.get_recent_posts()
	return render_template('blogs.html', user=current_user, featured_posts=featured_posts, recent_posts=recent_posts)

@app.route('/blog/<int:author_id>', defaults={'page':1})
@app.route('/blog/<int:author_id>/<int:page>')
def show_blog(author_id, page):
	count = model.count_all_posts(author_id)
	posts = model.get_posts_for_page(author_id, page, PER_PAGE, count)
	pagination = model.Pagination(page, PER_PAGE, count)
	return render_template('blog.html', posts=posts, user=current_user, pagination=pagination)

@app.route('/search')
def search():
	return render_template('search.html', user=current_user)

@app.route('/search', methods=['POST'])
def process_search():
	form = forms.SearchForm(request.form)
	if form.validate() == False: 
		flash("You didn't search for anything silly.")
		return render_template('search.html', user=current_user)
	else:
		posts = []
		ids_no_posts = []
		search_terms = form.search_term.data.split()
		for search_term in search_terms:
			user_ids = model.search_user(search_term)
			if user_ids == []:
				flash("Oh no!  That person doesn't exist.")
				return render_template('search.html', user=current_user)
			for user_id in user_ids:
				post = model.get_last_post(user_id)
				if post:
					posts.append(post)
				else: 
					ids_no_posts.append(user_id)
		users_no_posts = []
		for user_id in ids_no_posts:
			user = model.get_user_by_id(user_id)
			users_no_posts.append(user)
		posts = list(set(posts))
		users_no_posts = list(set(users_no_posts))
		return render_template('searchresults.html', user=current_user, posts=posts, no_posts=users_no_posts)
########## end blog views ##########

########## post views ##########
@app.route('/post/<int:post_pk>')
def show_post(post_pk):
	post = model.get_post_by_pk(post_pk)
	comments = model.get_comments_by_post_pk(post_pk)
	return render_template('post.html', post=post, user=current_user, comments=comments)

@app.route('/post/<int:post_pk>', methods=['POST'])
def comment(post_pk):
	new_comment = model.add_comment(request.form.get('user_id'),request.form.get('post_pk'),request.form.get('comment'))
	comment_timestamp = format_date(new_comment.timestamp)
	return jsonify({
		'comment_author': new_comment.user.first_name,
		'comment_content': new_comment.content,
		'comment_pk': new_comment.comment_pk,
		'comment_timestamp': comment_timestamp})

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
		return render_template('addpost.html', user=current_user)
	else:
		content = form.post_content.data
		title = form.post_title.data
		new_post = model.add_post(current_user.user_id, content, title)
	return redirect(url_for("show_blog",author_id=current_user.user_id))

@app.route('/editpost/<int:post_pk>')
@login_required
def edit_post(post_pk): 
	post = model.get_post_by_pk(post_pk)
	return render_template('editpost.html',user=current_user, post=post)

@app.route('/editpost/<int:post_pk>', methods=['POST'])
@login_required
def process_edit(post_pk):
	form = forms.EditPostForm(request.form)
	if form.validate() == False: 
		flash('All fields are required.')
		return render_template('url_for(edit_post)', post_pk = post_pk)
	else:
		content = form.new_content.data
		old_post = model.get_post_by_pk(post_pk)
		old_post.is_deleted = True
		model.edit_post(current_user.user_id,old_post.post_id,content,old_post.title,old_post.is_featured,old_post.version_id+1,old_post.comment_count)
	return redirect(url_for("show_blog",author_id=current_user.user_id))

@app.route('/deletepost/<int:post_pk>')
@login_required
def delete_post(post_pk): 
	post = model.get_post_by_pk(post_pk)
	post.is_deleted = True 
	model.session.commit()
	return redirect(url_for("show_blog",author_id=current_user.user_id))
########## end post views ##########

########## comment views ##########
@app.route('/edit_comment/<int:comment_pk>', methods=['GET'])
def edit_comment(comment_pk):
	comment = model.get_comment_by_pk(comment_pk)
	return jsonify({
		'comment_content': comment.content})

@app.route('/edit_comment/<int:comment_pk>', methods=['POST'])
def show_new_comment(comment_pk):
	old_comment = model.get_comment_by_pk(comment_pk)
	new_comment = model.edit_comment(current_user.user_id, old_comment.post.post_pk, comment_pk, request.form.get('edited_comment'))
	new_comment_timestamp = format_date(new_comment.timestamp)
	return jsonify({
		'comment_author': new_comment.user.first_name,
		'comment_content': new_comment.content,
		'comment_timestamp': new_comment_timestamp})

@app.route('/deletecomment/<int:comment_pk>')
@login_required
def delete_comment(comment_pk): 
	comment = model.get_comment_by_pk(comment_pk)
	comment.is_deleted = True 
	comment.post.comment_count -= 1 
	model.session.commit()
	return redirect(url_for("show_post",post_pk=comment.post_pk))
########## end comment views ##########

########## test views ##########
@app.route('/testdatabase', methods=['POST'])
def check_db():
	try:
		session.info()
		return jsonify({'up': True}) 
	except sqlalchemy.exc.OperationalError:
		return jsonify({'up': False})
	else:
		return jsonify({'up': False})  
	

@app.route('/test')
def show_mark():
	return render_template('test.html')

@app.route('/addpostajax', methods=['POST'])
def test_ajax():
	content = request.form.get('hello')
	title = request.form.get('title')
	return render_template('testajax.html', content=content, title=title)

@app.route('/signup')
def sign_up():
	return render_template('signup.html', user=current_user)

@app.route('/signup', methods=['POST'])
def process_sign_up():
	form = forms.SignupForm(request.form)
	first_name = form.first_name.data
	last_name = form.last_name.data
	email = form.email.data
	password = form.password.data
	validate_password = form.validate_password.data
	profile_picture = form.profile_picture.data
	period = form.period.data
	school_id = form.school_id.data
	if password != validate_password:
		flash('Passwords do not match.')
		return render_template('signup.html', user=current_user, first=first_name
			, last=last_name,email=email)
	else:
		new_user = model.create_user(first_name,last_name,email,password,int(period),int(school_id))
		login_user(new_user)
		return render_template('index.html',user=current_user)

@app.route('/d3test')
def show_d3():
	return render_template('d3test.html')

########## end test views ##########

if __name__ == "__main__":
    app.run(debug = True)
