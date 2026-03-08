import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv
from datetime import date

# Create Database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
id INTEGER PRIMARY KEY,
customer TEXT,
product TEXT,
price REAL,
qty INTEGER,
total REAL,
date TEXT
)
""")

def generate_invoice():

    customer = entry_customer.get()
    product = entry_product.get()
    price = float(entry_price.get())
    qty = int(entry_qty.get())

    subtotal = price * qty
    gst = subtotal * 0.18
    total = subtotal + gst

    today = str(date.today())

    # Save to database
    cursor.execute(
        "INSERT INTO sales(customer,product,price,qty,total,date) VALUES(?,?,?,?,?,?)",
        (customer,product,price,qty,total,today)
    )
    conn.commit()

    # Create invoice text file
    filename = f"invoice_{customer}.txt"

    with open(filename,"w") as file:

        file.write("===== GST INVOICE =====\n")
        file.write(f"Date: {today}\n\n")

        file.write(f"Customer: {customer}\n")
        file.write(f"Product: {product}\n")
        file.write(f"Price: {price}\n")
        file.write(f"Quantity: {qty}\n\n")

        file.write(f"Subtotal: {subtotal}\n")
        file.write(f"GST (18%): {gst}\n")
        file.write(f"Total: {total}\n")

    messagebox.showinfo("Success","Invoice Generated")

def export_report():

    rows = cursor.execute("SELECT * FROM sales").fetchall()

    with open("sales_report.csv","w",newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["ID","Customer","Product","Price","Qty","Total","Date"])

        for row in rows:
            writer.writerow(row)

    messagebox.showinfo("Report","Sales report exported")

# GUI
root = tk.Tk()
root.title("Billing & Invoice System")
root.geometry("400x350")

tk.Label(root,text="Customer Name").pack()
entry_customer = tk.Entry(root)
entry_customer.pack()

tk.Label(root,text="Product").pack()
entry_product = tk.Entry(root)
entry_product.pack()

tk.Label(root,text="Price").pack()
entry_price = tk.Entry(root)
entry_price.pack()

tk.Label(root,text="Quantity").pack()
entry_qty = tk.Entry(root)
entry_qty.pack()

tk.Button(root,text="Generate Invoice",
command=generate_invoice).pack(pady=10)

tk.Button(root,text="Export Sales Report",
command=export_report).pack()

root.mainloop()