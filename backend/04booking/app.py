from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect("clinic.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
id INTEGER PRIMARY KEY,
patient TEXT,
doctor TEXT,
date TEXT,
time TEXT
)
""")

conn.commit()

# Patient booking page
@app.route("/", methods=["GET","POST"])
def book():

    if request.method == "POST":

        patient = request.form["patient"]
        doctor = request.form["doctor"]
        date = request.form["date"]
        time = request.form["time"]

        cursor.execute(
        "INSERT INTO appointments(patient,doctor,date,time) VALUES(?,?,?,?)",
        (patient,doctor,date,time)
        )

        conn.commit()

        return "Appointment Booked Successfully"

    return render_template("book.html")


# Doctor dashboard
@app.route("/dashboard")
def dashboard():

    data = cursor.execute(
    "SELECT * FROM appointments"
    ).fetchall()

    return render_template("dashboard.html",data=data)


# Delete appointment (manage schedule)
@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
    "DELETE FROM appointments WHERE id=?",(id,)
    )

    conn.commit()

    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)