import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))

    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def project_by_title(project_title):
    query = """SELECT (?), description, max_grade FROM Projects"""
    DB.execute(query, (project_title,))

    row = DB.fetchone()
    print """\
Project: %s
Project Description: %s
Max Grade: %d"""%(row[0], row[1], row[2])

def add_project(project_name, project_description, max_grade):
    query = """INSERT INTO Projects VALUES (?, ?, ?)"""
    DB.execute(query, (project_name, project_description, max_grade))

    CONN.commit()
    print "Successfully added project %s" % (project_name)

def get_student_grade(student_github, project_title):
    query = """SELECT grade 
    FROM Grades WHERE project_title = (?) 
    AND student_github = (?)"""
    DB.execute(query, (project_title, student_github))

    row = DB.fetchone()

    print "%s got %d on %s" % (student_github, row[0], project_title)

def give_grade(student_github, project_title, grade):
    query = """UPDATE Grades 
    SET grade = (?) WHERE student_github = (?) 
    AND project_title = (?)"""
    DB.execute(query, (grade, student_github, project_title))

    CONN.commit()
    print "Successfully added grade: %s for %s on %s" % (grade, student_github, project_title)

def show_grades(student_github):
    query = """SELECT * FROM Grades WHERE student_github = (?)"""
    DB.execute(query, (student_github, ))

    row = DB.fetchall()
    for project in row:
        print """Project Title: %s 
Student Grade: %s

""" % (project[1], project[2])



def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":

        input_string = raw_input("HBA Database> ")
        #tokens = input_string.strip()
        tokens = input_string.split(", ")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            project_by_title(*args)
        elif command == "new_project":
            add_project(*args)
        elif command == "get_student_grade":
            get_student_grade(*args)
        elif command == "give_grade":
            give_grade(*args)
        elif command== "show_grades":
            show_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
