mrscutronadotcom
================

Mrscutronadotcom is a web application I am building for a fantastic friend and Algebra II teacher, Laura Cutrona. This project was inspired by my time in the classroom as a math teacher at Ocala Middle School and Metropolitan Arts and Tech High School.  With this application, Mrs. Cutrona will be able to assign blog posts as homework or in-class assignments as well as send mass texts to students ("don't forget--quiz tomorrow!"), and students will be able to view interactive grade visualizations as well as download class notes.  There are more features to come!  This is a work in progress, and will be put into production January 2014. 

Mrscutronadotcome is written with Python, Flask, Javascript, AJAX, D3, and the Twilio API.

#Grades

##Grades view: 
![](/static/ss/9.png)

##"What if?": 
![](/static/ss/10.png)
![](/static/ss/11.png)

##gradeschart.js

Uses AJAX to retrieve student grade data and D3 to visualize the data.  Data is graphed in layers and scaled according to the amount of data.  Implements interactive "What If?" feature where students can select from a variety of outcomes for future assignments and see how their grade is affected. 

##csvparser.py

Parses grade files exported from Laura's gradebook and enters individual grades into the database. 

#Blogs

Blogging functionality includes searching by user, editing and deleting comments and posts, add post live preview and autosave. 

##post.js, addpost.js

Uses AJAX to allow students to comment on posts and edit comments.  

Uses the browser session and AJAX to auto-save posts, and markdown for styling. 


##Featured and recent blogs view: 
![](/static/ss/3.png)

##Add post view: 
![](/static/ss/7.png)

#Build Instructions

##Environment 

You'll need virtualenv for this.  If you don't have it, run the following in your project folder: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ . env/bin/activate 
</code></pre>

This installs virtualenv, creates the env folder in your project folder with a local copy of python, activates the virtual environment. Then, install the requirements via pip: 

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>

##Database

To run the postgres server: download and run [postgres.app](http://postgresapp.com/) (for mac). 

Follow the instructions to set up postgres app (especially about setting your path).  

###Create database:

First in PostgreSQL:

<pre><code>$ psql
# CREATE DATABASE mrscdb;
</code></pre>

Then in Python (make sure your virtualenv is activated): 

<pre><code>(env)$ python -i model.py
(env)$ create_db()
</code></pre>

##Finally, run the app: 

<pre><code>(env)$ python app.py
</code></pre>

Point your browser to: localhost:5000.
