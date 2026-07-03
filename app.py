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
        return redirect(url_for("login"))
    
    return render_template("dashboard.html", usename=session["username"])

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

app.run(debug=True)