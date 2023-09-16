from flask import redirect, render_template, session

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
