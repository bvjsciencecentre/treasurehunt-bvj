import os
import psycopg2

#from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (StringField)
from wtforms.validators import InputRequired, Length

from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
#app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret string'

# database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_URL'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn
 

def check_type_query():
    conn = get_db_connection()
    cur = conn.cursor()
    # Execute a command: this creates a new table
    query1 = "SELECT pg_typeof(entered_unique_key) FROM public.location1 where entered_unique_key = ('1001');"
    cur.execute(query1)
    # stores the results of the query
    check_type = cur.fetchall()
    for result in check_type:
        if result == 'character varying':
            return procfurther()
        else:
            error = "Please enter the correct PIN " 
            return error

@app.route('/location')
def procfurther():
    conn = get_db_connection()
    cur = conn.cursor()
    query2 = "select next_riddle, next_unique_key from location1 where entered_unique_key = '1001';"
    cur.execute(query2)
    nextstep = cur.fetchall() 
    for r in nextstep:
        dispnext_riddle = r[0]
        dispnext_unique_key = r[1]
#    cur.close()
#    conn.close()
    return render_template('location.html', 
                            dispnext_riddle=dispnext_riddle, 
                            dispnext_unique_key=dispnext_unique_key)

# home page <---
@app.route('/home')
def home_view():
    return render_template("index.html")

# location page <---

class RiddleForm(FlaskForm):
    answer = StringField('Answer', validators=[InputRequired(),
                                             Length(min=1, max=20) ])
    
    @app.route("/location", methods=['GET', 'POST'])
    def form_view():
        form =  RiddleForm()
        return render_template('location.html', form=form)  

     
#cur.close()
#conn.close()