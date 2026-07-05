import sqlite3
from flask import Flask,render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rohit123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT BALANCE FROM users WHERE username = ?", (session["username"],))
    balance = cursor.fetchone()[0]
    conn.close()
    return render_template("dashboard.html", username=session["username"], balance=balance)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out", "success")
    return redirect(url_for("login"))

@app.route("/login",
          methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM USERS WHERE username = ? AND password = ?", (username,password))
        user = cursor.fetchone()
        conn.close()
        if user:
            flash("Login successful", "success")
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))
    return render_template("login.html")
    
        

@app.route("/register",
           methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("register.html")
        
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("User with this email already exists", "error")
            return render_template("register.html")
        
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existing_username = cursor.fetchone()
        if existing_username:
            flash("username already exists", "error")
            return render_template("register.html")

        cursor.execute("""INSERT INTO users(username,email,password) 
                        values(?,?,?)""",(username,email,password))
        conn.commit()
        conn.close()
        
        flash("User registered successfully", "success")    
    return render_template("register.html")

@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        try:
            amount = int(request.form.get("amount"))
        except ValueError:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("deposit"))
        if amount <= 0:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("deposit"))
        
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute("SELECT BALANCE FROM users WHERE username = ?", (session["username"],))
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance + (amount)
        cursor.execute("UPDATE users SET BALANCE = ? WHERE username = ?", (new_balance, session["username"]))
        conn.commit()
        conn.close()
        flash(f"Deposited {amount} successfully", "success")
        return redirect(url_for("dashboard"))
    return render_template("deposit.html")

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        try:
            amount = int(request.form.get("amount"))
        except ValueError:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("withdraw"))
        if amount <= 0:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("withdraw"))
        
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute("SELECT BALANCE FROM users WHERE username = ?", (session["username"],))
        current_balance = cursor.fetchone()[0]
        new_balance = current_balance - amount
        cursor.execute("UPDATE users SET BALANCE = ? WHERE username = ?", (new_balance, session["username"]))
        conn.commit()
        conn.close()
        flash(f"Withdrew {amount} successfully", "success")
        return redirect(url_for("dashboard"))
    return render_template("withdraw.html")

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        receiver_username = request.form.get("receiver_username")
        try:
            amount = int(request.form.get("amount"))
        except ValueError:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("transfer"))
        if amount <= 0:
            flash("Please enter a valid amount", "error")
            return redirect(url_for("transfer"))

        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()

        cursor.execute("SELECT BALANCE FROM users WHERE username = ?", (session["username"],))
        current_balance = cursor.fetchone()[0]
        
        if current_balance < amount:
            flash("Insufficient balance", "error")
            return redirect(url_for("transfer"))
        
        cursor.execute("SELECT BALANCE FROM users WHERE username = ?", (receiver_username,))
        receiver_balance = cursor.fetchone()
        
        if not receiver_balance:
            flash("Receiver username does not exist", "error")
            return redirect(url_for("transfer"))
        
        if receiver_username == session["username"]:
            flash("You cannot transfer to yourself", "error")
            return redirect(url_for("transfer"))
        
        new_balance_sender = current_balance - amount
        new_balance_receiver = receiver_balance[0] + amount
        
        cursor.execute("UPDATE users SET BALANCE = ? WHERE username = ?", (new_balance_sender, session["username"]))
        cursor.execute("UPDATE users SET BALANCE = ? WHERE username = ?", (new_balance_receiver, receiver_username))
        
        conn.commit()
        conn.close()
        
        flash(f"Transferred {amount} to {receiver_username} successfully", "success")
        return redirect(url_for("dashboard"))
        
        
app.run(debug=True)