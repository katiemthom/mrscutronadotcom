########## Import ##########
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from model import User, session as sesh
from flask.ext.mail import Message, Mail 
from flaskext.markdown import Markdown
from werkzeug import secure_filename
from boto.s3.connection import S3Connection
from boto.s3.key import Key
# from twilio.rest import TwilioRestClient

import os.path as op
import model
import os 
import config
import forms 
import datetime
import csvparser
import json
import csv
import time
########## end Import ##########

########## Flask Setup ##########
app = Flask(__name__)
app.config.from_object(config)
Markdown(app)
s3 = S3Connection(os.environ['aws_access_key_id'], os.environ['aws_secret_access_key'])
# s3 = S3Connection(config.aws_access_key_id, config.aws_secret_access_key)

########## end Flask Setup ##########

########## Twilio Setup ##########
# account_sid = "AC3901c5cf385356b4ab1bf0684c5751c8"
# auth_token  = "7f1b4dd329c1aa6bfa87b0aa4a669a94"
# client = TwilioRestClient(account_sid, auth_token)

# try:
#     client = twilio.rest.TwilioRestClient(account_sid, auth_token)
#     from twilio.rest import TwilioRestClient
 
#     message = client.sms.messages.create(
#         body="Hello World",
#         to="+14159352345",
#         from_="+14158141829"
#     )
# except twilio.TwilioRestException as e:
#     print e


# message = client.sms.messages.create(body="Jenny please?! I love you <3",
#     to="+18572058821",    # Replace with your phone number
#     from_="+18572541932") # Replace with your Twilio number
# print message.sid
########## end Twilio Setup ##########

########## File Upload Setup ##########
UPLOAD_FOLDER = '/Users/katiemthom/Desktop/projects/mrscutronadotcom/static/grades'
UPLOAD_FOLDER_PICS = '/Users/katiemthom/Desktop/projects/mrscutronadotcom/static/profile_pics'
UPLOAD_FOLDER_NOTES = '/Users/katiemthom/Desktop/projects/mrscutronadotcom/static/notes'
ALLOWED_EXTENSIONS = set(['txt','csv'])
ALLOWED_EXTENSIONS_NOTES = set(['txt','pdf'])
ALLOWED_EXTENSIONS_PICS = set(['png','jpg','jpeg','gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PICS'] = UPLOAD_FOLDER_PICS
app.config['UPLOAD_FOLDER_NOTES'] = UPLOAD_FOLDER_NOTES

def allowed_file(filename):
	print "checking allowed"
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def allowed_file_notes(filename):
	print "checking allowed"
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS_NOTES

def allowed_img_file(filename):
	return '.' in filename and \
		filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS_PICS
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
@app.route('/uploadgrades', methods=['GET', 'POST'])
def upload_img():
	try: 
		if current_user.is_admin_user: 
			if request.method == 'POST':
				form = forms.UploadGradesForm()
				if not form.validate():
					flash('You forgot to choose a file or you choose a file with an extension that is not allowed.','warning')
					return render_template('uploadgrades.html', user=current_user)
				# GET URL
				n = form.csv_file.data
				print n
				b = s3.get_bucket('mrscutronagrades')
				print b
				print "b"
				k = b.get_key(n)
				contents = k.get_contents_as_string()
				csvparser.load_grade_csv(contents)
				# file = request.files['csv_file']
				# if file and allowed_file(file.filename):
				# 	# filename = secure_filename(file.filename)
				# 	print "hello1"
				# 	bucket = s3.create_bucket('mrscutronagrades'+str(time.time()))
				# 	k = Key(bucket)
				# 	k.key = 'grades file'
				# 	print "hello"
				# 	k.set_contents_from_filename('/Users/katiemthom/Downloads/a.csv')
				# 	contents = k.get_contents_as_string()
				# 	print contents
					# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					# csvparser.load_grade_csv(filename)
				flash('Grades uploaded!','success')
				return render_template('uploadgrades.html', user=current_user)
			else: 
				return render_template('uploadgrades.html', user=current_user)
		else:
			flash('You don\'t have permission to access that page.', 'warning')
			return render_template('index.html', user=current_user)
	except:
		flash('You don\'t have permission to access that page.', 'warning')
		return render_template('index.html', user=current_user)

@app.route('/', methods=['POST'])
def process_login(): 
	form = forms.LoginForm(request.form)
	if not form.validate():
		flash('Incorrect username or password')
		return render_template('index.html')
	email = form.email.data
	password = form.password.data 
	user = sesh.query(User).filter_by(email=email).first()
	if not user or not user.authenticate(password):
		flash('Incorrect username or password')
		return render_template('index.html',  user = current_user)
	login_user(user)
	return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/')
def index():
	return render_template('index.html', user = current_user)
########## end signin and signup views ##########

########## user views ##########
########## end user views ##########

########## assignment views ##########
@app.route('/assignmentlist')
def list_assignments():
	assignments = model.get_assignments()
	return render_template('assignmentlist.html', assignments=assignments, user=current_user)

@app.route('/addassignment', methods=['GET','POST'])
def add_assignment():
	if request.method == 'POST':
		form = forms.AddAssignmentForm(request.form)
		if form.validate() == False: 
			flash('All fields are required.','warning')
			return render_template('addassignment.html',  user=current_user)
		else:
			assigned_on = form.assigned_on.data
			assigned_on_split = assigned_on.split('-')
			assigned_on = datetime.datetime(int(assigned_on_split[2]),int(assigned_on_split[1]),int(assigned_on_split[0]))
			due_on = form.due_on.data
			due_on_split = due_on.split('-')
			due_on = datetime.datetime(int(due_on_split[2]),int(due_on_split[1]),int(due_on_split[0]))
			link = form.link.data
			description = form.description.data
			category = form.category.data
			group = form.group.data
			title = form.title.data
			new_assignment = model.add_assignment(assigned_on,due_on,link,description,category,group,title)
			return redirect('assignmentlist')
	else:
		return render_template('addassignment.html', user=current_user)

@app.route('/deleteassignment/<int:assignment_pk>', methods=['GET'])
def delete_assignment(assignment_pk):
	model.delete_assignment(assignment_pk)
	assignments = model.get_assignments()
	return render_template('assignmentlist.html', user = current_user, assignments=assignments)
########## end assignment views ##########

########## notes views ##########
@app.route('/notes', defaults={'page':1})
@app.route('/notes/<int:page>')
def show_notes(page):
	count = model.count_all_notes()
	print count
	notes = model.get_notes_for_page(page, 3, count)
	print notes
	pagination = model.Pagination(page, 3, count)
	print pagination
	return render_template('notes.html', notes = notes, user = current_user, pagination=pagination)

@app.route('/find_notes', methods=['POST'])
def find_notes():
	print request.form
	notes_from = request.form.get('search_for')
	notes_from_split = notes_from.split('-')
	notes_from = datetime.datetime(int(notes_from_split[2]),int(notes_from_split[1]),int(notes_from_split[0]))
	print notes_from
	try:
		print "in try"
		notes = model.get_notes_by_date(notes_from)
		return jsonify({'created_on': format_date(notes.created_on), 'description': notes.description, 'link': notes.link})
	except:
		return jsonify({'message': 'No notes were found for that date.'})

@app.route('/uploadnotes', methods=['GET', 'POST'])
def upload_notes():
	if request.method == "POST":
		# try: 
		# 	print "in try"
		# 	if current_user.is_admin_user: 
		# 		print "is admin"
		# 		if request.method == 'POST':
		# 			print "if post"
		form = forms.UploadNotesForm()
		if not form.validate():
			flash('All fields are required.  Notes can only be pdf files.','warning')
			return render_template('uploadnotes.html', user=current_user)
					# file = request.files['notes_file']
					# if file and allowed_file_notes(file.filename):
					# print "if file"
					# print file.filename
					# filename = secure_filename(file.filename)
					# print filename
					# print app.config['UPLOAD_FOLDER_NOTES']
					# file.save(os.path.join(app.config['UPLOAD_FOLDER_NOTES'], filename))
		description = form.description.data
		created_on = form.created_on.data
		created_on_split = created_on.split('-')
		created_on = datetime.datetime(int(created_on_split[2]),int(created_on_split[1]),int(created_on_split[0]))
		filename = form.notes_file.data
		link =  "https://www.dropbox.com/sh/q2e8gjmi9bm5gr7/ebpSLR6lcC/" + filename
		new_notes = model.add_notes(link=link,created_on=created_on,description=description)
		flash('Notes uploaded!','success')
		return render_template('uploadnotes.html', user=current_user)
				# else: 
				# 	return render_template('uploadnotes.html', user=current_user)
			# else:
			# 	flash('You don\'t have permission to access that page.', 'warning')
			# 	return render_template('index.html', user=current_user)
		# except:
		# 	flash('You don\'t have permission to access that page.', 'warning')
		# 	return render_template('index.html', user=current_user)
	else:
		return render_template('uploadnotes.html', user=current_user)


########## end notes views ##########

########## report bug views ##########
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
########## end report bug views ##########

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
	if session.get('current_post'):
		post = session['current_post']
		title = session['current_title']
	else:
		post = ""
		title = ""
	return render_template('addpost.html', user=current_user, post=post, title = title)

@app.route('/addpost', methods=['POST'])
@login_required
def add_post():
	form = forms.AddPostForm(request.form)
	if form.validate() == False: 
		post = session['current_post']
		title = session['current_title']
		flash('All fields are required.')
		return render_template('addpost.html', user=current_user, post=post, title = title)
	else:
		content = form.post_content.data
		title = form.post_title.data
		new_post = model.add_post(current_user.user_id, content, title)
		session['current_post'] = ""
		session['current_title'] = ""
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
	sesh.commit()
	return redirect(url_for("show_blog",author_id=current_user.user_id))

@app.route('/addpostajax', methods=['POST'])
def test_ajax():
	content = request.form.get('hello')
	title = request.form.get('title')
	session['current_post'] = request.form['hello']
	session['current_title'] = request.form['title']
	return render_template('filtermarkdown.html', content=content, title=title)
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
	sesh.commit()
	return redirect(url_for("show_post",post_pk=comment.post_pk))
########## end comment views ##########

########## grade views ##########
@app.route('/grades')
def show_grades():
	return render_template('grades.html', user = current_user)

@app.route('/gradeinfo')
def calc_grade():
	grades = model.calc_grade(current_user.user_id)
	total_grade = round(grades[0] + grades[1] + grades[2])
	if total_grade > 100: 
		letter_grade = "A+"
	elif total_grade >= 96: 
		letter_grade = "A"
	elif total_grade >= 88: 
		letter_grade = "A-"
	elif total_grade >= 79: 
		letter_grade = "B+"
	elif total_grade >= 71: 
		letter_grade = "B"
	elif total_grade >= 63: 
		letter_grade = "B-"
	elif total_grade >= 54: 
		letter_grade = "C+"
	elif total_grade >= 46: 
		letter_grade = "C"
	elif total_grade >= 38: 
		letter_grade = "C-"
	else: 
		letter_grade = "NC"
	cwh_grade = round(grades[0])
	mk_grade = round(grades[2])
	ak_grade = round(grades[1])
	allgrades = model.get_grades_by_user_id(current_user.user_id)
	grades_list = []
	for grade in allgrades: 
	 	grades_list.append({"category": grade.assignment.category, "atitle": grade.assignment.title, "score": grade.value, "date": format_date(grade.assignment.due_on), "pk": grade.grade_pk})
	grades_json = json.dumps(grades_list)
	return jsonify({'grades_dict': grades_json, 'letter_grade': letter_grade,'mk_grade': mk_grade, 'ak_grade': ak_grade, 'cwh_grade': cwh_grade})
########## end grade views ##########

########## test views ##########
@app.route('/test')
def show_mark():
	return render_template('test2.html', user=current_user)
########## end test views ##########	

########## signup views ##########
@app.route('/signup')
def sign_up():
	form = forms.SignupForm()
	return render_template('signup.html', user=current_user, form =form)

@app.route('/signup', methods=['POST'])
def process_sign_up():
	form = forms.SignupForm()
	if not form.validate(): 
		print form.errors
		first_name = form.first_name.data
		last_name = form.last_name.data
		email = form.email.data
		school_id = form.school_id.data
		flash('All fields are required.  School ID must be a 4-digit number.','warning')
		return render_template('signup.html', user=current_user, first=first_name
				, last=last_name,email=email, school_id=school_id)
	else:
		print form.errors
		first_name = form.first_name.data
		last_name = form.last_name.data
		email = form.email.data
		if email[-10:] != "es-cat.org":
			flash('You must use your CAT email.','warning')
			return render_template('signup.html', user=current_user, first=first_name, last=last_name, school_id=school_id)
		password = form.password.data
		validate_password = form.pw_validation.data
		period = form.period.data
		school_id = form.school_id.data
		profile_pic = form.profile_pic.data
		print profile_pic
		if password != validate_password:
			flash('Passwords do not match.')
			return render_template('signup.html', user=current_user, first=first_name
				, last=last_name,email=email, school_id=school_id)
		new_user = model.create_user(first_name,last_name,email,password,int(period),int(school_id),profile_pic)
		login_user(new_user)
		return render_template('index.html',user=new_user)

@app.route('/datamodels')
def show_models():
	return render_template('datamodels.html', user=current_user)
########## end signup views ##########

########## student views ##########
@app.route('/students')
def show_students():
	return render_template('students.html', user = current_user)

@app.route('/getstudents/<int:period>')
def get_students(period):
	students = model.get_users_by_period(period)
	students_list = []
	for student in students:
		if student.is_banned == False: 
			is_banned = "Active"
		else:
			is_banned = "Banned"
		students_list.append({"user_id": student.user_id, "first_name": student.first_name, "last_name": student.last_name, "period": student.period, "is_banned": is_banned})
	students_json = json.dumps(students_list)
	return jsonify({'students_list': students_list})

@app.route('/togglestatus/<int:user_id>/<status>', methods=['POST'])
def toggle_status(user_id, status):
	model.toggle_status_by_user_id(user_id, status) 
	return jsonify({'msg': 'success!'})
########## end student views ##########

########## text views ##########
@app.route('/sendtext', methods=['GET','POST'])
def send_text():
	if request.method == "GET": 
		return render_template('sendtext.html', user=current_user)
	else: 
		form = forms.SendTextForm()
		text_body = form.text_content.data
		phone_numbers = model.get_phone_numbers()
		# where do I unencrypt? 
		if not form.validate(): 
			flash('All fields are required.', 'warning')
			return render_template('sendtext.html', user=current_user)
		else:
			try: 
				message = client.sms.messages.create(
			        body=text_body,
			        to="+15188591825",
			        from_="+18572541932"
			    )
				flash('Success!', 'success')
				return render_template('sendtext.html', user=current_user)
			except twilio.TwilioRestException as e:
				print e
				flash(e, 'warning')
				return render_template('sendtext.html', user=current_user)

@app.route('/textnotifications', methods = ['GET', 'POST'])
def add_number():
	if request.method == "GET":
		return render_template('textnotifications.html', user=current_user)
	else: 
		form = forms.AddPhoneForm()
		if not form.validate(): 
			flash('Make sure you enter a ten digit number.', 'warning')
			return render_template('textnotifications.html', user=current_user)
		else:
			try: 
				model.add_phone_number(current_user.user_id, form.phone_number.data)
				flash('Phone number added!', 'success')
				return render_template('textnotifications.html', user=current_user)
			except: 
				flash('Make sure you enter a ten digit number.', 'warning')
				return render_template('textnotifications.html', user=current_user)
########## end text views ##########			 

if __name__ == "__main__":
    app.run(debug = True)
