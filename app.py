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
        vaccines = db.execute("SELECT * FROM vaccines WHERE user_id = ?", (session["user_id"],)).fetchall()

        print(vaccines)

        return render_template("profiles.html", PROFILES=profiles, VACCINES=vaccines)
    else:
        name = request.form.get("name")
        birth = request.form.get("birthdate")
        blood = request.form.get("blood")
        allergies = request.form.get("allergies")
        chronic = request.form.get("chronic")
        procedures = request.form.get("procedures")
        medications = request.form.get("medications")
        smoke = request.form.get("smoke")
        alcohol = request.form.get("alcohol")

        # Ensure everything was submitted
        if not name or not birth or not blood or not allergies or not medications or not chronic or not procedures or not smoke or not alcohol:
            return render_template("error.html")

        # Insert new profile
        db.execute("INSERT INTO profiles (user_id, name, birthdate, blood, allergies, diseases, procedures, medications, smoke, alcohol) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (session["user_id"], name, birth, blood, allergies, chronic, procedures, medications, smoke, alcohol))
        conn.commit()

        return redirect("/profiles")


@app.route("/delete_profile", methods=["POST"])
@login_required
def delete():
    pf_id = request.form.get("profile_id")
    db.execute ("DELETE FROM profiles WHERE name = ?", (pf_id,))

    conn.commit()

    return redirect("/profiles")


@app.route("/vaccination", methods=["POST"])
@login_required
def vaccination():
    pf_id = request.form.get("profile_id")
    vac = request.form.get("vaccine")
    date = request.form.get("v_date") 

    db.execute ("INSERT INTO vaccines (user_id, profile_id, vaccine, date) VALUES (?, ?, ?, ?)", (session["user_id"], pf_id, vac, date))
    
    conn.commit()

    return redirect("/profiles")


@app.route("/bmi", methods=["GET", "POST"])
@login_required
def bmi():
    if request.method == "POST":
        if 'metric' in request.form:
            weight = float(request.form.get("m-weight"))
            height = float(request.form.get("m-height"))
        
        elif 'imperial' in request.form:
            weight = float(request.form.get("i-weight"))
            height = float(request.form.get("i-height"))
        
        else:
            return render_template("error.html")

        # Ensure values were submitted correctly
        if not weight or weight < 0 or not height or height < 0:
                return render_template("error.html")
        
        # Calculate BMI
        if 'metric' in request.form:
            result = f"{weight / (height * height):.1f}"

        if 'imperial' in request.form:
            result = f"{(703 * weight) / (height * height):.1f}"

        return render_template("bmi.html", RESULT=result)

    else:
        return render_template("bmi.html")


@app.route("/practices")
@login_required
def practices():
    return render_template("practices.html")
