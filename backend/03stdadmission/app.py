from flask import Flask, render_template, request, redirect
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'madhu@gmail.com'
app.config['MAIL_PASSWORD'] = 'Madhu@26'

mail = Mail(app)

# Database
conn = sqlite3.connect("students.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY,
name TEXT,
email TEXT,
course TEXT,
status TEXT
)
""")

conn.commit()

# Student Registration
@app.route("/",methods=["GET","POST"])
def register():

    if request.method=="POST":

        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        cursor.execute(
        "INSERT INTO students(name,email,course,status) VALUES(?,?,?,?)",
        (name,email,course,"Pending")
        )

        conn.commit()

        return "Registration Submitted"

    return render_template("register.html")


# Admin Panel
@app.route("/admin")
def admin():

    students = cursor.execute("SELECT * FROM students").fetchall()

    return render_template("admin.html",students=students)


# Approve Student
@app.route("/approve/<int:id>")
def approve(id):

    cursor.execute(
    "UPDATE students SET status='Approved' WHERE id=?",(id,)
    )

    conn.commit()

    student = cursor.execute(
    "SELECT email FROM students WHERE id=?",(id,)
    ).fetchone()

    # Send email
    msg = Message(
    "Admission Approved",
    sender="your_email@gmail.com",
    recipients=[student[0]]
    )

    msg.body = "Congratulations! Your admission is approved."

    mail.send(msg)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)