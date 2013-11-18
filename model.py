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
    profile_picture = Column(String(64), nullable=True, default='http://katiemthom.com/cat_ph.jpeg')
    school_id = Column(Integer, nullable=False)

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
	max_points = Column(Integer, nullable = False, default=5)
	category = Column(String, nullable = False)
	group = Column(Integer, nullable = False, default=0)
	version_id = Column(Integer, nullable = False, default=1)
	assignment_id = Column(BigInteger, nullable = False)
	is_deleted = Column(Boolean, nullable = False, default = False)
	title = Column(String(120), nullable = False)

class Grade(Base):
	__tablename__ = 'grades'
	grade_pk = Column(BigInteger, primary_key = True)
	assignment_pk = Column(BigInteger, ForeignKey('assignments.assignment_pk'), nullable = False)
	value = Column(Float, nullable = False)
	user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable = False)
	note = Column(Text, nullable = True)
	weight = Column(Float, nullable = False, default = 1)
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

def create_user(first_name,last_name,email,password,period,school_id,salt="salt"):
	new_user = User(first_name=first_name,last_name=last_name,email=email,password=password,period=period,school_id=school_id,salt=salt)
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
	return session.query(User).get(school_id)
########### END USER FUNCTIONS ###########

########### FUNCTIONS WITH NOTES ###########
def get_notes(): 
	return session.query(Notes).limit(3).all()
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
		new_post = Post(timestamp=datetime.datetime.now(),user_id=author_id,content=content,post_id=last.post_pk+1, title=title)
	else:
		new_post = Post(timestamp=datetime.datetime.now(),user_id=author_id,content=content,post_id=1, title=title)
	session.add(new_post)
	session.commit()
	return new_post

def edit_post(user_id,post_id,content,title,is_featured,version_id,comment_count):
	new_post = Post(timestamp=datetime.datetime.now(),user_id=user_id,post_id=post_id,content=content,is_featured=is_featured,version_id=version_id,title=title,comment_count=comment_count)
	session.add(new_post)
	session.commit()
	return new_post

def get_last_post(user_id):
	last_post = session.query(Post).filter_by(user_id=user_id).order_by(desc(Post.timestamp)).first()
	return last_post
########### END FUNCTIONS WITH POSTS ###########

########### FUNCTIONS WITH GRADES ###########
def get_grades_by_user_id(user_id):
	return session.query(Grade).filter_by(user_id=user_id).all()

def add_grade(assignment_pk, value, user_id):
	new_grade = Grade(assignment_pk = assignment_pk, value = value, user_id = user_id)
	return new_grade
########### END FUNCTIONS WITH GRADES ###########

########### FUNCTIONS WITH ASSIGNMENTS ###########
def add_assignment(assigned_on,due_on,link,description,max_points,category,group,title):
	#set assignment id see add comment below
	last = session.query(Assignment).order_by(desc(Assignment.assignment_pk)).first()
	if last: 
		assignment_id = last.assignment_pk + 1
	else: 
		assignment_id = 1
	new_assignment = Assignment(assigned_on=assigned_on,due_on=due_on,link=link,description=description,max_points=max_points,category=category,group=group,title=title,assignment_id=assignment_id)
	session.add(new_assignment)
	session.commit()
	return new_assignment
########### END FUNCTIONS WITH ASSIGNMENTS ###########

########### FUNCTIONS WITH COMMENTS ###########
def add_comment(author_id,post_pk,content):
	last = session.query(Comment).order_by(desc(Comment.comment_pk)).first()
	if last: 
		new_comment = Comment(timestamp=datetime.datetime.now(),user_id=author_id,post_pk=post_pk,content=content,comment_id=last.comment_pk+1)
	else: 
		new_comment = Comment(timestamp=datetime.datetime.now(),user_id=author_id,post_pk=post_pk,content=content,comment_id=1)
	post = session.query(Post).filter_by(post_pk=post_pk).one()
	post.comment_count += 1
	session.add(new_comment)
	session.commit()
	return new_comment

def edit_comment(user_id,post_pk,comment_pk,content):
	old_comment = get_comment_by_pk(comment_pk)
	old_comment.is_deleted = True 
	new_comment = Comment(timestamp=datetime.datetime.now(),user_id=user_id,post_pk=post_pk,content=content, comment_id=old_comment.comment_id, version_id=old_comment.version_id+1)
	session.add(new_comment)
	session.commit()
	return new_comment

def get_comments_by_post_pk(post_pk):
	return session.query(Comment).filter_by(post_pk=post_pk).filter_by(is_deleted=False).all()

def get_comment_by_pk(comment_pk):
	return session.query(Comment).filter_by(comment_pk=comment_pk).first()	
########### END FUNCTIONS WITH COMMENTS ###########

########### END FUNCTIONS ###########

def main(): 
	pass

def create_db():
	Base.metadata.create_all(engine)
	print 'db created!'

if __name__ == "__main__":
	main()
