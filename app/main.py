import os
import psycopg2
from urllib.parse import urlparse

#from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (StringField)
from wtforms.validators import InputRequired, Length
from flask import request
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
#app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret string'

# database connection
"""
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_URL'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn
"""
FLASK_ENV = os.environ["FLASK_ENV"]
def get_db_connection():
    if FLASK_ENV == "development":
        conn = psycopg2.connect(
            host=os.environ['DB_URL'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
        return conn
    elif FLASK_ENV == "production":
        url = urlparse(os.environ.get('DATABASE_URL'))
        db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
        schema = "schema.sql"
        conn = psycopg2.connect(db)
        return conn
    
 

def check_key_and_get_next_riddle(entered_unique_key,location):
    conn = get_db_connection()
    cur = conn.cursor()
    query1 = f"SELECT * FROM public.{location} where entered_unique_key = '{entered_unique_key}';"
    cur.execute(query1)
    query1_values = cur.fetchone()
    cur.close()
    conn.close()
    try:
        team_name = query1_values[2]
        next_riddle = query1_values[3]
        next_unique_key = query1_values[4]
        return (team_name, next_riddle, next_unique_key)
    except Exception as err:
        error = "Please enter the correct PIN or go to another location" 
        return ('',error, '')

def create_timestamp_for_team_at_location(team_name,location_name):
#table = team_location_time
#team_name, location_name, timestamp
    timestamp = int(datetime.now().timestamp())
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query2 = f"INSERT INTO public.team_location_time(team_name, location_name, timestamp) VALUES (%s,%s,%s);"
        cur.execute(query2,(team_name,location_name,timestamp))
        conn.commit()
    except Exception as err:
        print (err)
    cur.close()
    conn.close()
# home page <---
@app.route('/home')
def home_view():
    return render_template("index.html")

# location page <---
# location_name and location_route should be same
@app.route("/bvj_entry", methods=["GET", "POST"])
def register_with_key_bvj_entry():
    location_name = "bvj_entry"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("bvj_entry.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("bvj_entry.html")

@app.route("/history", methods=["GET", "POST"])
def register_with_key_history():
    location_name = "history"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("history.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("history.html")

@app.route("/journalism", methods=["GET", "POST"])
def register_with_key_journalism():
    location_name = "journalism"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("journalism.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("journalism.html")

@app.route("/biology", methods=["GET", "POST"])
def register_with_key_biology():
    location_name = "biology"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("biology.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("biology.html")

@app.route("/math", methods=["GET", "POST"])
def register_with_key_math():
    location_name = "math"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("math.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("math.html")

@app.route("/physics", methods=["GET", "POST"])
def register_with_key_physics():
    location_name = "physics"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("physics.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("physics.html")

@app.route("/psychology", methods=["GET", "POST"])
def register_with_key_psychology():
    location_name = "psychology"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("psychology.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("psychology.html")

@app.route("/iot", methods=["GET", "POST"])
def register_with_key_iot():
    location_name = "iot"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("iot.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("iot.html")

@app.route("/english", methods=["GET", "POST"])
def register_with_key_english():
    location_name = "english"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("english.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("english.html")

@app.route("/electronics", methods=["GET", "POST"])
def register_with_key_electronics():
    location_name = "electronics"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("electronics.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("electronics.html")

@app.route("/chemistry", methods=["GET", "POST"])
def register_with_key_chemistry():
    location_name = "chemistry"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("chemistry.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("chemistry.html")

@app.route("/bvj_exit", methods=["GET", "POST"])
def register_with_key_bvj_exit():
    location_name = "bvj_exit"
    if request.method == "POST":
        entered_unique_key = request.form.get("entered_unique_key")

        team_name, next_riddle, next_unique_key = check_key_and_get_next_riddle(entered_unique_key, location_name)
        create_timestamp_for_team_at_location(team_name,location_name)
        return render_template("bvj_exit.html", team_name=team_name, next_riddle=next_riddle, next_unique_key=next_unique_key)
    return render_template("bvj_exit.html")

@app.route("/register", methods=["GET", "POST"])
def register_team_name():
    from app.generate_data_for_team import create_team_data
    location_name = "bvj_exit"
    if request.method == "POST":
        team_name = request.form.get("team_name")

        first_key = create_team_data(team_name)
        return render_template("register.html", team_name=team_name, next_unique_key=first_key)
    return render_template("register.html")