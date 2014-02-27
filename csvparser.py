import model
import csv
from datetime import date
import datetime
import time
import urllib

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
    print "in upload_grades"
    print csv_string
    rows = csv_string.split("\n") 
    print rows
    header_row = row[1].split(",")
    print header_row
    grades_dict = {}
    for i in range(4, len(header_row)):
        grades_dict[header_row[i]] = {}
        print header_row[i]
    print grades_dict
    return    

def load_grade_csv(csv_file):
    with open("/Users/katiemthom/Desktop/projects/mrscutronadotcom/static/grades/" + csv_file,"rb") as f:
        print "opened file"
        reader=csv.reader(f,delimiter='\n')
        recording = False
        for row in reader:
            print "going through rows, e.g."
            print row
            if row == []:
                continue
            data = row[0].split(',')
            if recording:
                student_id = int(data[0].strip())
                print student_id
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
                if data[0].strip() == "Assignment Name:":
                    title = data[1][1:-1].strip()
                    print title
                if data[0].strip() == "Student ID":
                    recording = True
        model.session.commit()
        f.close()
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