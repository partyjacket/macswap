from arista_nest_helper import myhelper
from pprint import pprint as pp

test = ['1', '2', 'jason', 3, 4, 10]

students = [("Alejandro", ["CompSci", "Physics"]),
            ("Justin", ["Math", "CompSci", "Stats"]),
            ("Ed", ["CompSci", "Accounting", "Economics"]),
            ("Margot", ["InfSys", "Accounting", "Economics", "CommLaw"]),
            ("Peter", ["Sociology", "Economics", "Law", "Stats", "Music"])]

for v in test:
    print test.index(v)






def student_attr(student_name):
    for student, subjects in students:
        if student == student_name:
            print'%-10s takes  %s courses' % (student, ' and '.join(subjects))



for student, courses in students:
    student_attr(student)
print '\n'

def get_num_courses():
    for name, courses in students:
        course_len = len(courses)
        print "%-20s takes %20d %1s" % (name, course_len, 'courses')

get_num_courses()

