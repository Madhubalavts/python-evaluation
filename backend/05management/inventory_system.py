import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv

# Database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory(
id INTEGER PRIMARY KEY,
item TEXT,
supplier TEXT,
quantity INTEGER
)
""")

conn.commit()

# Add Item
def add_item():

    item = entry_item.get()
    supplier = entry_supplier.get()
    qty = int(entry_qty.get())

    cursor.execute(
    "INSERT INTO inventory(item,supplier,quantity) VALUES(?,?,?)",
    (item,supplier,qty)
    )

    conn.commit()

    listbox.insert(tk.END,f"{item} | {supplier} | Qty: {qty}")

    if qty < 5:
        messagebox.showwarning("Low Stock Alert","Stock is below 5!")

# Show Inventory
def view_items():

    listbox.delete(0,tk.END)

    rows = cursor.execute("SELECT item,supplier,quantity FROM inventory").fetchall()

    for r in rows:
        listbox.insert(tk.END,f"{r[0]} | {r[1]} | Qty: {r[2]}")

# Export Report
def export_report():

    rows = cursor.execute("SELECT * FROM inventory").fetchall()

    with open("inventory_report.csv","w",newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["ID","Item","Supplier","Quantity"])

        for row in rows:
            writer.writerow(row)

    messagebox.showinfo("Report","Inventory report exported!")

# GUI
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("400x420")

tk.Label(root,text="Item Name").pack()
entry_item = tk.Entry(root)
entry_item.pack()

tk.Label(root,text="Supplier").pack()
entry_supplier = tk.Entry(root)
entry_supplier.pack()

tk.Label(root,text="Quantity").pack()
entry_qty = tk.Entry(root)
entry_qty.pack()

tk.Button(root,text="Add Item",command=add_item).pack(pady=5)

tk.Button(root,text="View Inventory",command=view_items).pack(pady=5)

tk.Button(root,text="Export Report",command=export_report).pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH,expand=True)

root.mainloop()