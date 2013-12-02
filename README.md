mrscutronadotcom
================

mrscutronadotcom is a web app I'm building for my friend Laura, who teaches Algebra II at a public charter high school in San Francisco.  It is also my Hackbright Academy final project. 

Users
=====

Laura will be the admin user on the site.  Her students will be the users. Users can upload profile pictures. 

Landing page, signed in as admin: 
![Signed in as admin.](/static/ss/1.png)

Landing page, signed in as student: 
![Signed in as user.](/static/ss/2.png)

Blogs
=====

Laura wants to assign blog posts to students, so students will have their own math blogs.  They will be able to comment on each others' blogs, as well as edit their own comments and posts. 

Featured and recent blogs: 
![](/static/ss/3.png)

Search blogs by student (I searched for "K"): 
![](/static/ss/4.png)

Pagination: 
![](/static/ss/5.png)

Comments: 
![](/static/ss/6.png)

Add a post with live preview and auto-save: 
![](/static/ss/7.png)

User view of blog post: 
![](/static/ss/8.png)

Grades
======

Students will be able to view and interact with a visualization of their grade for the class. 

Grades view: 
![](/static/ss/9.png)

"What if?": 
![](/static/ss/10.png)
![](/static/ss/11.png)


Notes 
=====

Students can view and download lecture notes.

Will show previews of notes (as opposed to my resume) when Amazon S3 is implemented. 

Search by date: 

![](/static/ss/12.png)

Recent notes: 

![](/static/ss/13.png)
![](/static/ss/14.png)


Build Instructions
==================

To run the postgres server: download and run [postgres.app](http://postgresapp.com/) (for mac). 

Follow the instructions to set up postgres app.  

In the project directory, create a virtualenv and install the requirements via pip: 

$ pip install -r requirements.txt

Start the virtual env: 

$ . env/bin/activate

Create the db: 

$ python -i model.py
$ create_db()

Run the app: 

$ python app.py

Point your browser to: localhost:5000.
