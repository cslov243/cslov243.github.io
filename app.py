import os
import datetime

from flask import Flask, flash, redirect, render_template, request, session
import sqlite3
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# connect to database file
conn = sqlite3.connect("exercises.db")
db = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weight REAL NOT NULL,
        reps INTEGER NOT NULL
    )
""")

# Save (commit) changes
conn.commit()

# Close when done
conn.close()
