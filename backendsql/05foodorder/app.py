from flask import Flask, render_template, session, redirect

app = Flask(__name__)
app.secret_key="food123"

menu = {
1:{"name":"Pizza","price":200},
2:{"name":"Burger","price":120},
3:{"name":"Pasta","price":180}
}

orders=[]

@app.route("/")
def menu_page():
    return render_template("menu.html",menu=menu)

@app.route("/add/<int:id>")
def add(id):

    cart=session.get("cart",[])
    cart.append(menu[id])
    session["cart"]=cart

    return redirect("/cart")

@app.route("/cart")
def cart():

    cart=session.get("cart",[])
    total=sum(i["price"] for i in cart)

    return render_template("cart.html",cart=cart,total=total)

@app.route("/checkout")
def checkout():

    orders.append(session.get("cart",[]))
    session["cart"]=[]

    return "Order Placed!"

@app.route("/admin")
def admin():
    return render_template("admin.html",orders=orders)

if __name__=="__main__":
    app.run(debug=True)