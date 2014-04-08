import model
import csv
from datetime import date
import datetime
import time
import urllib
import sys
import string

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

# def upload_grades(csv_string):
#     rows = csv_string.split("\r") 
#     print "rows"
#     print "\n"
#     print rows
#     print "\n"
#     header_row = rows[1].split(",")
#     print header_row
#     print "\n"
#     print len(header_row)
#     print "\n"
#     print header_row[4]
#     print "\n"
#     grades_dict = {}
#     for i in range(4, len(header_row)):
#         grades_dict[header_row[i].strip()] = {}
#         print header_row[i] + "\n"
#     print grades_dict[]
#     # need grades need to be added 
#     # grades dict looks like 
#     return    

# Need a catch for if grade is not a number
def load_grade_csv(csv_file):
    csv_file = string.replace(csv_file, "\n", "\r")
    reader = csv_file.split("\r")
    recording = False
    assignment_dict = {}
    title_counter = 0
    for row in reader:
        if row[:4].isdigit():
            recording = True
        if recording: 
            data = row.split(',')
            if len(data) < 4:
                pass
            else:
                grade = 0
                assignment_counter = 0
                for j in range(0,len(data)):
                    if j == 0:
                        student_id = int(data[j])
                    elif j > 3 and data[j] != '' and data[j] != "Ex":
                        grade = float(data[j])
                        assignment_dict[assignment_counter][1][student_id] = grade
                        assignment_counter += 1
        else: 
            i = string.find(row, ',"')
            if i != -1: 
                title = row[i+2:]
                assignment_dict[title_counter] = [title,{}]
                title_counter += 1
    for key in assignment_dict.keys():
        title = assignment_dict[key][0]
        grades_dict = assignment_dict[key][1]
        for student_id in grades_dict.keys():
            value = grades_dict[student_id]
            try:
                user = model.get_user_by_school_id(student_id)
                user_id = user.user_id
                print "user_id"
                print user_id
                try: 
                    print "title"
                    print title
                    assignment = model.get_assignment_by_title(title)
                    assignment_pk = assignment.assignment_pk
                    print "assignment_pk"
                    print assignment_pk
                    assignment_weight = assignment.weight
                    value = value * float(assignment_weight)
                    grade = model.add_grade(assignment_pk,value,user_id)
                    model.session.add(grade)
                except:
                    pass
            except:
                pass
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