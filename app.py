import sqlite3
from flask import Flask,render_template, request, flash

app = Flask(__name__)
app.secret_key = "rohit123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
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
            return "Passwords do not match"
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "User with this email already exists"
        cursor.execute("""INSERT INTO users(username,email,password) 
                        values(?,?,?)""",(username,email,password))
        conn.commit()
        conn.close()
        
        flash("User registered successfully")    
    return render_template("register.html")

app.run(debug=True)