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

engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit=False,autoflush=False))

Base = declarative_base()
Base.query = session.query_property 

########### CLASS DEFINITIONS ###########

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
	title = Column(String(64), nullable=False)

class Comment(Base): 
	__tablename__ = 'comments'
	comment_pk = Column(BigInteger, primary_key = True)
	comment_id = Column(BigInteger, nullable=False)
	timestamp = Column(DateTime, nullable=False)
	user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
	post_pk = Column(BigInteger, ForeignKey('posts.post_pk'), nullable=False)
	content = Column(String(500), nullable=False)
	version_id = Column(Integer, nullable=False)
	is_deleted = Column(Boolean, default=False)
	user = relationship("User", backref="comments")
	post = relationship("Post", backref="comments")

class Assignment(Base): 
	__tablename__ = 'assignments'
	id = Column(Integer, primary_key = True)
	assigned_date = Column(Date)
	due_date = Column(Date)
	link = Column(String(120), nullable = True)
	description = Column(Text)
	max_points = Column(Integer)
	category = Column(String)

class Grade(Base):
	__tablename__ = 'grades'
	id = Column(Integer, primary_key = True)
	assignment_id = Column(Integer, ForeignKey('assignments.id'))
	value = Column(Float)
	user_id = Column(Integer, ForeignKey('users.user_id'))
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

########### FUNCTIONS ###########

def create_db():
	Base.metadata.create_all(engine)
	print 'db created!'

	data_loader.load_users()
	# data_loader.load_notes()
	data_loader.load_posts()
	print 'db created!'

def get_user_by_id(user_id):
	return session.query(User).get(user_id)

########### FUNCTIONS WITH NOTES ###########

def get_notes(): 
	return session.query(Notes).limit(3).all()

########### FUNCTIONS WITH POSTS ###########

# def get_posts_by_user_id(user_id,page):
# 	return session.query(Post).filter_by(author_id=user_id).order_by(desc(Post.timestamp)).paginate(page,5,False).items

def get_featured_posts():
	return session.query(Post).order_by(desc(Post.comment_count)).limit(3).all()

def get_recent_posts():
	return session.query(Post).order_by(desc(Post.timestamp)).limit(5).all()

def get_posts_by_user_id(user_id):
	return session.query(Post).filter_by(user_id=user_id).order_by(desc(Post.timestamp)).all()

def get_posts():
	return session.query(Post).order_by(desc(Post.timestamp)).limit(5).all()

def get_post_by_id(post_id): 
	return session.query(Post).filter_by(post_id=post_id).one()

def get_posts_for_page(user_id, page, per_page, count):
	# page * per_page = end slice
	# end slice - per_page = beginning slice
	end = page * per_page
	begin = end - per_page
	posts = session.query(Post).filter_by(user_id=user_id).order_by(desc(Post.timestamp)).all()
	return posts[begin:end]


def count_all_posts(user_id):
	return len(session.query(Post).filter_by(user_id=user_id).all())

def add_post(author_id,content):
	new_post = Post(timestamp=datetime.datetime.now(),author_id=author_id,content=content)
	session.add(new_post)
	session.commit()
	return new_post

########### FUNCTIONS WITH GRADES ###########

def get_grades_by_user_id(user_id):
	return session.query(Grade).filter_by(user_id=user_id).all()

########### FUNCTIONS WITH COMMENTS ###########

def add_comment(author_id,post_id,content):
	new_comment = Comment(timestamp=datetime.datetime.now(),author_id=author_id,post_id=post_id,content=content)
	session.add(new_comment)
	session.commit()
	return new_comment

def get_comments_by_post_id(post_pk):
	return session.query(Comment).filter_by(post_pk=post_pk).all()

########### FUNCTIONS ###########

def main(): 
	pass

if __name__ == "__main__":
	main()
