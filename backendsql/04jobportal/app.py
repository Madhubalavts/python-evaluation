from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

conn = sqlite3.connect("jobs.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobseekers(
id INTEGER PRIMARY KEY,
name TEXT,
email TEXT,
resume TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
id INTEGER PRIMARY KEY,
title TEXT,
company TEXT
)
""")

conn.commit()

# Job Seeker Registration
@app.route("/", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        file = request.files["resume"]

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        cursor.execute(
        "INSERT INTO jobseekers(name,email,resume) VALUES(?,?,?)",
        (name,email,file.filename)
        )

        conn.commit()

    return render_template("register.html")

# Employer Post Job
@app.route("/post", methods=["GET","POST"])
def post_job():

    if request.method=="POST":

        title = request.form["title"]
        company = request.form["company"]

        cursor.execute(
        "INSERT INTO jobs(title,company) VALUES(?,?)",
        (title,company)
        )

        conn.commit()

    return render_template("post_job.html")

# View Jobs
@app.route("/jobs")
def jobs():

    data = cursor.execute("SELECT * FROM jobs").fetchall()

    return render_template("jobs.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)