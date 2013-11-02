from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text

Base = declarative_base()
ENGINE = None
Session = None 

########### CLASS DEFINITIONS ###########

class User(Base): 
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	email = Column(String(64))
	password = Column(String(64))
	period = Column(Integer)

class Post(Base): 
	__tablename__ = 'posts'
	id = Column(Integer, primary_key = True)
	timestamp = Column(DateTime)
	content = Column(Text)
	author_id = Column(Integer)

class Comment(Base): 
	__tablename__ = 'comments'
	id = Column(Integer, primary_key = True)
	timestamp = Column(DateTime)
	author_id = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))
	content = Column(String(500))
	user = relationship("User", backref="comments")
	post = relationship("Post", backref="comments")

class Assignment(Base): 
	__tablename__ = 'assignments'
	id = Column(Integer, primary_key = True)
	assigned_date = Column(DateTime)
	due_date = Column(DateTime)
	link = Column(String(120), nullable = True)
	description = Column(Text)
	max_points = Column(Integer)
	category = Column(String)

class Grade(Base):
	__tablename__ = 'grades'
	id = Column(Integer, primary_key = True)
	assignment_id = Column(Integer, ForeignKey('assignments.id'))
	value = Column(Integer)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", backref='grades')
	assignment = relationship("Assignment", backref='grades')

class Notes(Base): 
	__tablename__ = 'notes'
	id = Column(Integer, primary_key = True)
	link = Column(String(120), nullable = True)
	date = Column(DateTime)

########### FUNCTIONS ###########

def connect_to_db(): 
	global ENGINE
	global Session 
	ENGINE = create_engine("postgres://ekgeujzpmsqkme:7LQzlA8jPu7eq4tJAPaGM7Fvlc@ec2-54-235-78-155.compute-1.amazonaws.com:5432/d280dpo6dangu0", echo=True)
	Session = sessionmaker(bind=ENGINE)
	return Session()

def main(): 
	pass

if __name__ == "__main__":
	main()