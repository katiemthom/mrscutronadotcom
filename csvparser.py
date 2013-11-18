import model
import csv
from datetime import date
import datetime
import time
import urllib

def load_grade_csv(csv_file):
    with open("/static/grades/" + csv_file,"rb") as f:
        reader=csv.reader(f,delimiter='\n')
        recording = False
        for row in reader:
            data = row[0].split(',')
            if recording:
                student_id = int(data[0].strip())
                value = int(data[3].strip())
                # get user_id based on student id
                # get assignment by title
                # create new grade
                # add grade
            else: 
                if data[0].strip() == "Assignment Name:":
                    title = data[1].strip
                if data[0].strip() == "Student ID":
                    recording = True
        model.session.commit()
        f.close()