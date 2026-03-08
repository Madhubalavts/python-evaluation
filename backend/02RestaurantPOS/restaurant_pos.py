import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database
conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY,
table_no TEXT,
item TEXT,
price REAL
)
""")

conn.commit()

# Add Order
def add_order():

    table = entry_table.get()
    item = entry_item.get()
    price = entry_price.get()

    cursor.execute(
        "INSERT INTO orders(table_no,item,price) VALUES(?,?,?)",
        (table,item,price)
    )

    conn.commit()

    listbox.insert(tk.END,f"Table {table} - {item} - {price}")

    messagebox.showinfo("Success","Order Added")


# Kitchen Screen
def show_kitchen():

    kitchen = tk.Toplevel()
    kitchen.title("Kitchen Orders")

    orders = cursor.execute("SELECT table_no,item FROM orders").fetchall()

    for o in orders:
        tk.Label(kitchen,text=f"Table {o[0]} : {o[1]}").pack()


# Generate Bill
def generate_bill():

    table = entry_table.get()

    orders = cursor.execute(
        "SELECT item,price FROM orders WHERE table_no=?",(table,)
    ).fetchall()

    total = 0

    bill_text = "----- Restaurant Bill -----\n\n"

    for item,price in orders:
        bill_text += f"{item} - {price}\n"
        total += price

    bill_text += "\nTotal: " + str(total)

    bill = tk.Toplevel()
    bill.title("Bill")

    tk.Label(bill,text=bill_text).pack()

    messagebox.showinfo("Bill","Bill Generated")


# GUI
root = tk.Tk()
root.title("Restaurant POS System")
root.geometry("400x400")

tk.Label(root,text="Table Number").pack()
entry_table = tk.Entry(root)
entry_table.pack()

tk.Label(root,text="Item Name").pack()
entry_item = tk.Entry(root)
entry_item.pack()

tk.Label(root,text="Price").pack()
entry_price = tk.Entry(root)
entry_price.pack()

tk.Button(root,text="Add Order",command=add_order).pack(pady=5)

tk.Button(root,text="Kitchen Screen",command=show_kitchen).pack(pady=5)

tk.Button(root,text="Generate Bill",command=generate_bill).pack(pady=5)

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH,expand=True)

root.mainloop()