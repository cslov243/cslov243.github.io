import os
import datetime

from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
import sqlite3
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure applicatio
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# connect to database file
conn = sqlite3.connect("exercises.db")
db = conn.cursor()
db.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL NOT NULL,
        reps INTEGER NOT NULL
    )
""")

# Save (commit) changes
conn.commit()
@app.before_request
def before_request():
    """Ensure a fresh SQLite connection is used for each request."""
    g.db = sqlite3.connect("exercises.db")
    g.db.row_factory = sqlite3.Row  # Optional, allows accessing columns by name

@app.teardown_request
def teardown_request(exception=None):
    """Close the database connection after each request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    passw = request.form.get("password")
    passc = request.form.get("confirmation")
    user = request.form.get("username")
    if request.method == "POST":
        try:
            if passw:
                hash1 = generate_password_hash(passw, method='scrypt', salt_length=16)
                if passc == passw:
                    if user:
                        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", user, hash1)
                        return render_template("register.html")
                    else:
                        return apology("Username?")
                else:
                    return apology("passwords dont match at all dude")
            else:
                return apology("Where your password at negsa")
        except ValueError:
            return apology("This username is already in use")
    else:
        return render_template("register.html")

# Close when done
conn.close()
