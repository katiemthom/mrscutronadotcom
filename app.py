from flask import Flask, render_template, request, redirect, url_for
#from flask.ext.sqlalchemy import SQLAlchemy
import model

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mrscutrona.db'
#db = SQLAlchemy(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def process_login(): 
	#model.connect_to_db()
	username = request.form.get('username')
	password = request.form.get('password')
	return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)
