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
            first_name = data[0]
            last_name = data[1]
            email = data[2]
            password = data[3]
            period = data[4]
            school_id = data[5]
            salt=data[6]
            new_user = model.User(first_name=first_name,last_name=last_name,email=email,password=password,period=period,school_id=school_id,salt=salt)
            model.session.add(new_user)
        model.session.commit()
        f.close()


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
            desc = data[3]
            new_notes = model.Notes(id=id, link=link,created_on=ndate, description=desc)
            model.session.add(new_notes)
        model.session.commit()
        f.close()

def load_posts():
    with open("data/posts","rb") as f:
        reader=csv.reader(f,delimiter='\n')
        for row in reader:
            data = row[0].split('|')
            post_id = data[0]
            ndate = time.strptime(data[1],"%d-%b-%Y")
            ndate = date(ndate[0],ndate[1],ndate[2])
            content = data[2]
            user_id = data[3]
            title = data[4]
            new_posts = model.Post(post_id=post_id, timestamp=ndate, content=content, user_id=user_id,title=title)
            model.session.add(new_posts)
        model.session.commit()
        f.close()
