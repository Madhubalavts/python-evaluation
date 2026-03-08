from flask import Flask,render_template,request,redirect
import sqlite3
import csv
from reportlab.pdfgen import canvas

app = Flask(__name__)

conn = sqlite3.connect("payroll.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
id INTEGER PRIMARY KEY,
name TEXT,
salary INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
emp_id INTEGER,
days INTEGER
)
""")

conn.commit()

# Add Employee
@app.route("/",methods=["GET","POST"])
def employees():

    if request.method=="POST":
        name=request.form["name"]
        salary=request.form["salary"]

        cursor.execute(
        "INSERT INTO employees(name,salary) VALUES(?,?)",
        (name,salary)
        )
        conn.commit()

    data=cursor.execute("SELECT * FROM employees").fetchall()

    return render_template("employees.html",data=data)

# Attendance
@app.route("/attendance",methods=["GET","POST"])
def attendance():

    if request.method=="POST":

        emp_id=request.form["emp_id"]
        days=request.form["days"]

        cursor.execute(
        "INSERT INTO attendance(emp_id,days) VALUES(?,?)",
        (emp_id,days)
        )

        conn.commit()

    employees=cursor.execute("SELECT * FROM employees").fetchall()

    return render_template("attendance.html",employees=employees)

# Export Excel
@app.route("/excel")
def excel():

    rows=cursor.execute("""
    SELECT employees.name,attendance.days,employees.salary
    FROM employees
    JOIN attendance
    ON employees.id=attendance.emp_id
    """).fetchall()

    with open("payroll_report.csv","w",newline="") as f:

        writer=csv.writer(f)
        writer.writerow(["Name","Days Worked","Salary"])

        for r in rows:
            writer.writerow(r)

    return "Excel Report Generated"

# Export PDF
@app.route("/pdf")
def pdf():

    rows=cursor.execute("""
    SELECT employees.name,attendance.days,employees.salary
    FROM employees
    JOIN attendance
    ON employees.id=attendance.emp_id
    """).fetchall()

    c=canvas.Canvas("payroll_report.pdf")

    y=800

    for r in rows:
        text=f"Name: {r[0]}  Days: {r[1]}  Salary: {r[2]}"
        c.drawString(100,y,text)
        y-=30

    c.save()

    return "PDF Generated"

if __name__=="__main__":
    app.run(debug=True)