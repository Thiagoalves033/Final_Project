from flask import redirect, render_template, session
from functools import wraps

def is_valid(password):
    length = len(password)

    if length < 8 or length > 12:
        return render_template("wrong.html")
    else:
        number, upper, lower = False, False, False

        for character in password:
            if character.isdigit():
                number = True
            if character.islower():
                lower = True
            if character.isupper():
                upper = True

        if number and upper and lower:
            return True
        else:
            return False
        

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
