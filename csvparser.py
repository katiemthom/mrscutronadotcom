import model
import csv
from datetime import date
import datetime
import time
import urllib
import sys

def load_period_2():
    with open("/Users/katiemthom/Desktop/projects/mrscutronadotcom/student_data/period2.txt","rb") as f:
        reader = csv.reader(f, delimiter = "\n")
        for row in reader:
            data = row[0].split(',')
            student_id = int(data[0])
            last_name = data[1].strip()
            first_name = data[2].strip()
            email = data[3].strip()
            new_user = model.create_user(first_name,last_name,email,"12345",2,student_id)
            model.session.add(new_user)
        model.session.commit()
        f.close()

def upload_grades(csv_string):
    rows = csv_string.split("\r") 
    print "rows"
    print "\n"
    print rows
    print "\n"
    header_row = rows[1].split(",")
    print header_row
    print "\n"
    print len(header_row)
    print "\n"
    print header_row[4]
    print "\n"
    grades_dict = {}
    for i in range(4, len(header_row)):
        grades_dict[header_row[i].strip()] = {}
        print header_row[i] + "\n"
    print grades_dict
    return    

def load_grade_csv(csv_file):
    print "opened file"
    reader=csv_file.split("\n")
    # recording = False
    for row in reader:
        print row
        print row[0]
        print row[0].strip()
        print row[0].strip()[1]
        if row[0].strip()[0] == "x":
            print "x found"
            return
        if row == []:
            continue
        # print "row"
        # print "\n"
        # print row
        data = row.split(',')
        # print "\n"
        # print "data"
        # print "\n"
        # print data
        # c += 1
        # if c == 5: 
        #     return
        if recording:
            student_id = int(data[0][1:-1].strip())
            try: 
                value = float(data[3][1:-1])
            except: 
                value = 0
            user = model.get_user_by_school_id(student_id)
            user_id = user.user_id
            try: 
                assignment = model.get_assignment_by_title(title)
                assignment_pk = assignment.assignment_pk
                grade = model.add_grade(assignment_pk,value,user_id)
                model.session.add(grade)
            except:
                return False 
        else: 
            # print "in else"
            # print "\n"
            # print "data"
            # print data[0][1:-1].strip()
            if data[0][1:-1].strip() == "Assignment Name:":
                # print "reached assignment name"
                title = data[1][1:-1].strip()
                # print title
                # return
            if data[0][1:-1].strip() == "Student ID":
                recording = True
    model.session.commit()
    return True

def load_grades_csv(csv_file):
    with open("/Users/katiemthom/Desktop/projects/mrscutronadotcom/static/grades/" + csv_file,"rU") as f:
        reader=csv.reader(f,dialect=csv.excel_tab)

        recording = False
        for row in reader:
            if row == []:
                continue
            data = row[0].split(',')
            print data
            # if recording:
            #     # student_id = int(data[0].strip())
            #     # print student_id
            #     # value = float(data[3][1:-1])
            #     # user = model.get_user_by_school_id(student_id)
            #     # user_id = user.user_id
            #     # try: 
            #     #     # assignment = model.get_assignment_by_title(title)
            #     #     # assignment_pk = assignment.assignment_pk
            #     #     # grade = model.add_grade(assignment_pk,value,user_id)
            #     #     # model.session.add(grade)
            #     # except:
            #     #     return False 
            # else: 
            #     counter += 1
            #     if counter == 4:
            #         recording = True 
        # model.session.commit()
        f.close()
        return True