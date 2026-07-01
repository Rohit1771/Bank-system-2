from flask import Flask,render_template, request

app = Flask(__name__)

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
        print("Form Submitted")
        print(f"Username: {username}, Email: {email},Password: {password}, Confirm Password: {confirm_password}")

    return render_template("register.html")

app.run(debug=True)