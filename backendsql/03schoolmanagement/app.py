from flask import Flask,render_template,request,redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("school.db",check_same_thread=False)
cursor = conn.cursor()

# Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY,
name TEXT,
course TEXT,
parent_password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
id INTEGER PRIMARY KEY,
name TEXT,
subject TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
student_id INTEGER,
days_present INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
student_id INTEGER,
subject TEXT,
marks INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
id INTEGER PRIMARY KEY,
name TEXT,
subject TEXT
)
""")

conn.commit()

# Home - Add Students
@app.route("/",methods=["GET","POST"])
def index():

    if request.method=="POST":

        name=request.form["name"]
        course=request.form["course"]
        password=request.form["password"]

        cursor.execute(
        "INSERT INTO students(name,course,parent_password) VALUES(?,?,?)",
        (name,course,password)
        )

        conn.commit()

    students=cursor.execute("SELECT * FROM students").fetchall()

    return render_template("index.html",students=students)

# Add Attendance
@app.route("/attendance",methods=["GET","POST"])
def attendance():

    if request.method=="POST":

        sid=request.form["student_id"]
        days=request.form["days"]

        cursor.execute(
        "INSERT INTO attendance(student_id,days_present) VALUES(?,?)",
        (sid,days)
        )

        conn.commit()

    students=cursor.execute("SELECT * FROM students").fetchall()

    return render_template("attendance.html",students=students)

# Add Marks
@app.route("/marks",methods=["GET","POST"])
def marks():

    if request.method=="POST":

        sid=request.form["student_id"]
        subject=request.form["subject"]
        marks=request.form["marks"]

        cursor.execute(
        "INSERT INTO marks(student_id,subject,marks) VALUES(?,?,?)",
        (sid,subject,marks)
        )

        conn.commit()

    students=cursor.execute("SELECT * FROM students").fetchall()

    return render_template("marks.html",students=students)

# Parent Login
@app.route("/parent",methods=["GET","POST"])
def parent():

    result=None

    if request.method=="POST":

        sid=request.form["student_id"]
        password=request.form["password"]

        student=cursor.execute(
        "SELECT * FROM students WHERE id=? AND parent_password=?",
        (sid,password)
        ).fetchone()

        if student:

            attendance=cursor.execute(
            "SELECT * FROM attendance WHERE student_id=?",(sid,)
            ).fetchall()

            marks=cursor.execute(
            "SELECT * FROM marks WHERE student_id=?",(sid,)
            ).fetchall()

            result={"student":student,"attendance":attendance,"marks":marks}

    return render_template("parent.html",result=result)

@app.route("/teachers", methods=["GET","POST"])
def teachers():

    if request.method == "POST":

        name = request.form["name"]
        subject = request.form["subject"]

        cursor.execute(
        "INSERT INTO teachers(name,subject) VALUES(?,?)",
        (name,subject)
        )

        conn.commit()

    data = cursor.execute("SELECT * FROM teachers").fetchall()

    return render_template("teachers.html",data=data)    

if __name__=="__main__":
    app.run(debug=True)