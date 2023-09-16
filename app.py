import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import is_valid

# Configure application
app = Flask(__name__)

# Configure SQLite database
conn = sqlite3.connect('htools.db', check_same_thread=False)
db = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wrong")
def wrong():
    return render_template("wrong.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure everything was submitted correctly and the passwords match
        if not username or not password or not confirmation or password != confirmation:
            return render_template("wrong.html")
        
        # Ensure password has the correct format
        if is_valid(password) == False:
            return render_template("wrong.html")
        
        # Query for the username and check if it's already in use
        in_use = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        if in_use.fetchone() != None:
            return render_template("wrong.html")

        # Register the user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", 
                   (username, 
                   generate_password_hash(password, method="pbkdf2", salt_length=16),)
        )
        conn.commit()

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    