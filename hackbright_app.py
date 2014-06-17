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

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":

        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
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

    CONN.close()

if __name__ == "__main__":
    main()
