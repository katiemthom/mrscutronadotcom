import model
import csv
from datetime import date
import time
import urllib

def load_users():
    with open("data/users","rb") as f:
        reader=csv.reader(f,delimiter='\n')
        for row in reader:
            data = row[0].split('|')
            id = data[0]
            first_name = data[1]
            last_name = data[2]
            email = data[3]
            password = data[4]
            period = data[5]
            new_user = model.User(id=id,first_name=first_name,last_name=last_name,email=email,password=password,period=period)
            model.session.add(new_user)
        model.session.commit()
        f.close()


# class Notes(Base): 
# 	__tablename__ = 'notes'
# 	id = Column(Integer, primary_key = True)
# 	link = Column(String(120), nullable = True)
# 	date = Column(DateTime)
def load_notes():
    with open("data/notes","rb") as f:
        reader=csv.reader(f,delimiter='\n')
        for row in reader:
            data = row[0].split('|')
            id = data[0]
            link = data[1]
            link = urllib.quote(link)
            ndate = time.strptime(data[2],"%d-%b-%Y")
            ndate = date(ndate[0],ndate[1],ndate[2])
            new_notes = model.Notes(id=id, link=link,created_on=ndate)
            model.session.add(new_notes)
        model.session.commit()
        f.close()

def load_posts():
    with open("data/posts","rb") as f:
        reader=csv.reader(f,delimiter='\n')
        for row in reader:
            data = row[0].split('|')
            id = data[0]
            ndate = time.strptime(data[1],"%d-%b-%Y")
            ndate = date(ndate[0],ndate[1],ndate[2])
            content = data[2]
            author_id = data[3]
            new_posts = model.Post(id=id, timestamp=ndate, content=content, author_id=author_id)
            model.session.add(new_posts)
        model.session.commit()
        f.close()
