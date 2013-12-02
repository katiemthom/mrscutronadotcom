mrscutronadotcom
================

mrscutronadotcom is a web app I'm building for my friend Laura, who teaches Algebra II at a public charter high school in San Francisco.  It is also my Hackbright Academy final project. 

Users
=====

Laura will be the admin user on the site.  Her students will be the users. 

Landing page, signed in as admin: 
![Signed in as admin.](/static/ss/1.png)

Blogs
=====

Students will have their own math blogs.  They will be able to comment on each others' blogs. 

Grades
======

Students will be able to view and interact with a visualization of their grade for the class. 

Notes 
=====

Students will be able to view and download lecture notes. 

Class Stats
===========

Students will be able to view how their class stacks up against the rest through interactive data visualizations. 

...and hopefully more!

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
