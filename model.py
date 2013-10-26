import psycopg2

DB = None
CONN = None

def connect_to_db(): 
	global CONN 
	global connect_to_db
	CONN = psycopg2.connect('dbname=mrscutrona.db user=postgres')
	DB = CONN.cursor()
