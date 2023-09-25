import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import is_valid, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
conn = sqlite3.connect('htools.db', check_same_thread=False)
db = conn.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/error")
def error():
    return render_template("error.html")


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
            return render_template("error.html")
        
        # Ensure password has the correct format
        if is_valid(password) == False:
            return render_template("error.html")
        
        # Query for the username and check if it's already in use
        in_use = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        if in_use.fetchone() != None:
            return render_template("error.html")

        # Register the user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", 
                   (username, 
                   generate_password_hash(password, method="pbkdf2", salt_length=16),)
        )
        conn.commit()

        # Redirect to Login
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure everything was submitted correctly
        if not username or not password:
            return render_template("error.html")
        
        # Query, check if the user exists and if password is correct
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = user.fetchone()

        if row == None or not check_password_hash(row[2], password):
            return render_template("error.html")
        
        # Remember which user is logged in
        session["user_id"] = row[0]

        # Redirect to Profiles
        return redirect("/profiles")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user
    return redirect("/")


@app.route("/profiles", methods=["GET", "POST"])
@login_required
def profiles():
    if request.method == "GET":
        profiles = db.execute("SELECT * FROM profiles WHERE user_id = ?", (session["user_id"],)).fetchall()

        return render_template("profiles.html", PROFILES=profiles)
    else:
        name = request.form.get("name")
        blood = request.form.get("blood")
        allergies = request.form.get("allergies")
        medications = request.form.get("medications")

        # Ensure everything was submitted
        if not name or not blood or not allergies or not medications:
            return render_template("error.html")

        # Insert new profile
        db.execute("INSERT INTO profiles (user_id, name, blood, allergies, medications) VALUES (?, ?, ?, ?, ?)", 
                   (session["user_id"], name, blood, allergies, medications))
        conn.commit()

        return redirect("/profiles")


@app.route("/practices")
@login_required
def practices():
    return render_template("practices.html")
