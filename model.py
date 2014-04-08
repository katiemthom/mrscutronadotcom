########### IMPORT ###########
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, desc
from sqlalchemy import Column, Integer, String, Date, Text, Float, Boolean, DateTime, BigInteger
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from flask.ext.login import UserMixin
from math import ceil
import data_loader

import os 
import config 
import bcrypt 
import datetime
########### END IMPORT ###########

########### SESSION ###########
engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit=False,autoflush=False))
########### END SESSION ###########

########### CLASS DEFINITIONS ###########
Base = declarative_base()
Base.query = session.query_property 

class User(Base, UserMixin): 
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key = True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    period = Column(Integer, nullable=False)
    salt = Column(String(64), nullable=False)
    is_banned = Column(Boolean, nullable=False, default=False)
    profile_picture = Column(String(200), nullable=True, default='http://katiemthom.com/cat_ph.jpeg')
    school_id = Column(Integer, nullable=False) 
    is_admin_user = Column(Boolean, nullable=False, default=False)

    def get_id(self):
    	return self.user_id

    def setpw(self, pw):
        self.salt = bcrypt.gensalt()
        pw = pw.encode("utf-8")
        self.password = bcrypt.hashpw(pw, self.salt)
        session.commit()

    def authenticate(self, password):
        password = password.encode('utf-8')
        return bcrypt.hashpw(password, self.salt.encode('utf-8')) == self.password

    def is_admin(self):
    	return False 

class Post(Base):
	__tablename__ = 'posts'
	post_pk = Column(BigInteger, primary_key = True)
	post_id = Column(BigInteger, nullable=False)
	timestamp = Column(DateTime, nullable=False)
	content = Column(Text, nullable=False)
	user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
	is_featured = Column(Boolean, default=False, nullable=False)
	version_id = Column(Integer, nullable=False, default=1)
	is_deleted = Column(Boolean, default=False)
	user = relationship("User", backref="posts")
	comment_count = Column(Integer, nullable=False, default=0)
	title = Column(String(250), nullable=False)

class Comment(Base): 
	__tablename__ = 'comments'
	comment_pk = Column(BigInteger, primary_key = True)
	comment_id = Column(BigInteger, nullable=False)
	timestamp = Column(DateTime, nullable=False)
	user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
	post_pk = Column(BigInteger, ForeignKey('posts.post_pk'), nullable=False)
	content = Column(String(500), nullable=False)
	version_id = Column(Integer, nullable=False, default=1)
	is_deleted = Column(Boolean, default=False)
	user = relationship("User", backref="comments")
	post = relationship("Post", backref="comments")

class Assignment(Base): 
	__tablename__ = 'assignments'
	assignment_pk = Column(BigInteger, primary_key = True)
	assigned_on = Column(DateTime, nullable = False)
	due_on = Column(DateTime, nullable = False)
	link = Column(String(120), nullable = True)
	description = Column(Text, nullable = True)
	max_points = Column(Integer, nullable = False, default=4)
	category = Column(String, nullable = False)
	group = Column(Integer, nullable = False, default=0)
	version_id = Column(Integer, nullable = False, default=1)
	assignment_id = Column(BigInteger, nullable = False)
	is_deleted = Column(Boolean, nullable = False, default = False)
	title = Column(String(120), nullable = False)
	weight = Column(Float, nullable = False, default = 1)

class Grade(Base):
	__tablename__ = 'grades'
	grade_pk = Column(BigInteger, primary_key = True)
	assignment_pk = Column(BigInteger, ForeignKey('assignments.assignment_pk'), nullable = False)
	value = Column(Float, nullable = False)
	user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable = False)
	note = Column(Text, nullable = True)
	version_id = Column(Integer, nullable = False, default = 1)
	is_deleted = Column(Boolean, nullable = False, default = False)
	user = relationship("User", backref='grades')
	assignment = relationship("Assignment", backref='grades')

class Notes(Base): 
	__tablename__ = 'notes'
	id = Column(Integer, primary_key = True)
	link = Column(String(120), nullable = True)
	created_on = Column(Date)
	description = Column(String(200), nullable = True)

class PhoneNumber(Base):
	__tablename__ = 'phone_numbers'
	id = Column(Integer, primary_key = True)
	user_id = Column(BigInteger, nullable = False)
	phone_number = Column(String, nullable = False)
	salt = Column(String(64), nullable=False)

	def setphone_number(self, phone_number):
		self.salt = bcrypt.gensalt()
		phone_number = phone_number.encode("utf-8")
		self.phone_number = bcrypt.hashpw(phone_number, self.salt)
		session.commit()
		return 

class Pagination(object):

	def __init__(self, page, per_page, total_count):
		self.page = page
		self.per_page = per_page
		self.total_count = total_count

	@property
	def pages(self):
		return int(ceil(self.total_count / float(self.per_page)))

	@property
	def has_prev(self): 
		return self.page > 1

	@property
	def has_next(self):
		return self.page < self.pages

	def iter_pages(self, left_edge=2, left_current=2,right_current=5,right_edge=2):
		last = 0
		for num in xrange(1, self.pages + 1):
			if num <= left_edge or \
				(num > self.page - left_current - 1 and \
				num < self.page + right_current) or \
				num > self.pages - right_edge:
				if last + 1 != num: 
					yield None
				yield num
				last = num 
########### END CLASS DEFINITIONS ###########

########### FUNCTIONS ###########

########### USER FUNCTIONS ###########
def get_user_by_id(user_id):
	return session.query(User).get(user_id)

def create_user(first_name,last_name,email,password,period,school_id,profile_picture=None,salt="salt"):
	new_user = User(first_name=first_name,last_name=last_name,email=email,password=password,period=period,school_id=school_id,profile_picture=profile_picture,salt=salt)
	new_user.setpw(password)
	session.add(new_user)
	session.commit()
	return new_user

def search_user(search_term):
	results = engine.execute("select user_id from users where user_index_col @@ to_tsquery('"+search_term+":*');")
	user_ids = []
	for result in results:
		user_ids.append(result[0])
	return user_ids

def get_user_by_school_id(school_id):
	return session.query(User).filter_by(school_id=school_id).one()

def get_users_by_period(period):
	return session.query(User).filter_by(period=period).all()

def toggle_status_by_user_id(user_id, status): 
	user = get_user_by_id(user_id)
	if status == "Banned": 
		user.is_banned = True
	else: 
		user.is_banned = False
	session.commit()
	return 
########### END USER FUNCTIONS ###########

########### FUNCTIONS WITH NOTES ###########
def get_notes(): 
	return session.query(Notes).limit(3).all()

def get_notes_by_date(dt):
	return session.query(Notes).filter_by(created_on=dt).one()

def count_all_notes():
	return len(session.query(Notes).all())

def get_notes_for_page(page, per_page, count):
	end = page * per_page
	begin = end - per_page
	notes = session.query(Notes).order_by(desc(Notes.created_on)).all()
	return notes[begin:end]

def add_notes(link, created_on, description):
	new_notes = Notes(link = link, created_on = created_on, description = description)
	session.add(new_notes)
	session.commit()
	return new_notes
########### END FUNCTIONS WITH NOTES ###########

########### FUNCTIONS WITH POSTS ###########
def get_featured_posts():
	return session.query(Post).filter_by(is_deleted=False).order_by(desc(Post.comment_count)).limit(3).all()

def get_recent_posts():
	return session.query(Post).filter_by(is_deleted=False).order_by(desc(Post.timestamp)).limit(6).all()

def get_post_by_pk(post_pk): 
	return session.query(Post).filter_by(post_pk=post_pk).one()

def get_posts_for_page(user_id, page, per_page, count):
	end = page * per_page
	begin = end - per_page
	posts = session.query(Post).filter_by(user_id=user_id).filter_by(is_deleted=False).order_by(desc(Post.timestamp)).all()
	return posts[begin:end]

def count_all_posts(user_id):
	return len(session.query(Post).filter_by(user_id=user_id).filter_by(is_deleted=False).all())

def add_post(author_id,content,title):
	last = session.query(Post).order_by(desc(Post.post_pk)).first()
	if last:
		new_post = Post(timestamp=datetime.datetime.utcnow(),user_id=author_id,content=content,post_id=last.post_pk+1, title=title)
	else:
		new_post = Post(timestamp=datetime.datetime.utcnow(),user_id=author_id,content=content,post_id=1, title=title)
	session.add(new_post)
	session.commit()
	return new_post

def edit_post(user_id,post_id,content,title,is_featured,version_id,comment_count):
	new_post = Post(timestamp=datetime.datetime.utcnow(),user_id=user_id,post_id=post_id,content=content,is_featured=is_featured,version_id=version_id,title=title,comment_count=comment_count)
	session.add(new_post)
	session.commit()
	return new_post

def get_last_post(user_id):
	last_post = session.query(Post).filter_by(user_id=user_id).order_by(desc(Post.timestamp)).first()
	return last_post
########### END FUNCTIONS WITH POSTS ###########

########### FUNCTIONS WITH GRADES ###########
def get_grades_by_user_id(user_id):
	assignments = session.query(Assignment).filter_by(is_deleted=False).order_by(desc(Assignment.due_on)).all()
	grades = []
	for assignment in assignments: 
		grade = session.query(Grade).filter_by(user_id=user_id).filter_by(assignment_pk=assignment.assignment_pk).first()
		if grade != None:
			grades.append(grade)
	return grades


def add_grade(assignment_pk, value, user_id):
	new_grade = Grade(assignment_pk = assignment_pk, value = value, user_id = user_id)
	session.add(new_grade)
	session.commit()
	return new_grade

def calc_grade(user_id):
	grades = get_grades_by_user_id(user_id)
	cwh_max = 0
	cwh_val = 0
	ak_max = 0
	ak_val = 0
	mk_max = 0
	mk_val = 0
	for grade in grades:
		try:
			category = grade.assignment.category
		except:
			category = None
		if category != None:
			if category == "CWH":
				cwh_max += grade.assignment.max_points
				cwh_val += grade.value
			if category == "MK":
				mk_max += grade.assignment.max_points
				mk_val += grade.value
			if category == "AK":
				ak_max += grade.assignment.max_points
				ak_val += grade.value
	if cwh_max == 0:
		cwh_final = .15 * 100
	else: 
		cwh_final = (cwh_val/cwh_max) * .15 * 100
	if ak_max == 0:
		ak_final = .45 * 100
	else: 
		ak_final = (ak_val/ak_max) * .45 * 100
	if mk_max == 0:
		mk_final = .4 * 100
	else: 
		mk_final = (mk_val/mk_max) * .4 * 100
	return (cwh_final, ak_final, mk_final)

########### END FUNCTIONS WITH GRADES ###########

########### FUNCTIONS WITH ASSIGNMENTS ###########
def add_assignment(assigned_on,due_on,link,description,category,group,title,weight):
	#set assignment id see add comment below
	last = session.query(Assignment).order_by(desc(Assignment.assignment_pk)).first()
	if last: 
		assignment_id = last.assignment_pk + 1
	else: 
		assignment_id = 1
	max_points = 4 * float(weight)
	new_assignment = Assignment(assigned_on=assigned_on,due_on=due_on,link=link,description=description,category=category,group=group,title=title,assignment_id=assignment_id,weight=weight,max_points=max_points)
	session.add(new_assignment)
	session.commit()
	return new_assignment

def get_assignment_by_title(title):
	return session.query(Assignment).filter_by(title=title).one()

def get_assignments():
	return session.query(Assignment).filter_by(is_deleted=False).all()

def delete_assignment(assignment_pk):
	assignment = session.query(Assignment).filter_by(assignment_pk=assignment_pk).one()
	assignment.is_deleted = True
	session.commit()
	return 

########### END FUNCTIONS WITH ASSIGNMENTS ###########

########### FUNCTIONS WITH COMMENTS ###########
def add_comment(author_id,post_pk,content):
	last = session.query(Comment).order_by(desc(Comment.comment_pk)).first()
	if last: 
		new_comment = Comment(timestamp=datetime.datetime.utcnow(),user_id=author_id,post_pk=post_pk,content=content,comment_id=last.comment_pk+1)
	else: 
		new_comment = Comment(timestamp=datetime.datetime.utcnow(),user_id=author_id,post_pk=post_pk,content=content,comment_id=1)
	post = session.query(Post).filter_by(post_pk=post_pk).one()
	post.comment_count += 1
	session.add(new_comment)
	session.commit()
	return new_comment

def edit_comment(user_id,post_pk,comment_pk,content):
	old_comment = get_comment_by_pk(comment_pk)
	old_comment.is_deleted = True 
	new_comment = Comment(timestamp=datetime.datetime.utcnow(),user_id=user_id,post_pk=post_pk,content=content, comment_id=old_comment.comment_id, version_id=old_comment.version_id+1)
	session.add(new_comment)
	session.commit()
	return new_comment

def get_comments_by_post_pk(post_pk):
	return session.query(Comment).filter_by(post_pk=post_pk).filter_by(is_deleted=False).all()

def get_comment_by_pk(comment_pk):
	return session.query(Comment).filter_by(comment_pk=comment_pk).first()	
########### END FUNCTIONS WITH COMMENTS ###########

########### FUNCTIONS WITH PHONENUMBERS ###########
def add_phone_number(user_id, phone_number):
	print user_id, phone_number
	new_phone_number = PhoneNumber(user_id=long(user_id),phone_number=int(phone_number),salt="salt")
	print new_phone_number
	new_phone_number.setphone_number(phone_number)
	session.add(new_phone_number)
	session.commit()
	return new_phone_number

def get_phone_numbers(): 
	return session.query(PhoneNumber).all()

########### END FUNCTIONS WITH PHONENUBMERS ###########

########### END FUNCTIONS ###########

def main(): 
	pass

def create_db():
	Base.metadata.create_all(engine)
	print 'db created!'

if __name__ == "__main__":
	main()
