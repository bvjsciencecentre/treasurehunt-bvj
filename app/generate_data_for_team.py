import string
import random
import psycopg2
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
load_dotenv()
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
        url = urlparse(os.environ['DATABASE_URL'])
        db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
        schema = "schema.sql"
        conn = psycopg2.connect(db)
        return conn

def key_generator(size=10):
    # Takes random choices from 
    # ascii_letters and digits
    generate_pass = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(size)])
    return generate_pass 

def generate_location_list(location_list):
    #print(random.sample(location_list, len(location_list)))
    list_to_return = []
    list_to_return.append(location_list[0])
    for entry in random.sample(location_list[1:-1], len(location_list[1:-1])):
        list_to_return.append(entry)
    list_to_return.append(location_list[-1:][0])
    return list_to_return


def upload_data_to_db(team_identifier, ordered_location_list, locations_to_question_dict, location_to_key_dict):

    conn = get_db_connection()

    list_to_upload = []
    for index in range(len(ordered_location_list)-1):
        cur = conn.cursor()
        this_location_key = str(location_to_key_dict[ordered_location_list[index]])
        next_question = str(locations_to_question_dict[ordered_location_list[index+1]])
        next_location_key = str(location_to_key_dict[ordered_location_list[index+1]])
        list_to_upload.append((this_location_key, team_identifier, next_question, next_location_key))
        try:
            query = f'INSERT INTO public."{ordered_location_list[index]}" (entered_unique_key, team_name, next_riddle, next_unique_key) VALUES(%s, %s, %s, %s)'
            cur.execute(query, (this_location_key, team_identifier, next_question, next_location_key))
            conn.commit()
            cur.close()
        except Exception as e:
            print(e)
            cur.close()
    try:
        cur = conn.cursor()
        query = f'INSERT INTO public."{ordered_location_list[-1:][0]}" (entered_unique_key, team_name, next_riddle, next_unique_key) VALUES(%s, %s, %s, %s)'
        cur.execute(query, (location_to_key_dict[ordered_location_list[-1:][0]], team_identifier, "Like they say, the greatest treasure of all time is time itself. We are looking at your times and doing some fancy math in the back to choose the winner. Please wait for the result, You might just be the winner. Everyone is at the end. Thank you for Participating in the Treasure Hunt.", " "))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    conn.close()
    list_to_upload.append((location_to_key_dict[ordered_location_list[-1:][0]], team_identifier, 'thanks_text', 'no_key'))

    return location_to_key_dict[ordered_location_list[0]], list_to_upload
    
def upload_ordered_location_name(team_name, ordered_location_list):
    try:
        conn = get_db_connection()

        cur = conn.cursor()
        query = f'INSERT INTO public."team_location_order_list" (team_name, ordered_location_list) VALUES(%s, %s)'
        cur.execute(query, (team_name, ordered_location_list))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as err:
        return err


def create_team_data(team_identifier):
    locations_list = ["bvj_entry", "history", "journalism", "biology", "math", "physics", "psychology", "iot", "english", "electronics", "chemistry", "bvj_exit"]
    questions_list = ["This is an entry question doesn't matter", "Stories as told by our ancestors in the old stone building.",
            "House of public, republic, ANI, etc.,", 
            "Dissection of life through what it holds.", 
            "PG club of universal language.", 
            "A parliament of extremely long & complicated formulas to describe how a ball rolls.", 
            "There they tell what I know about me in the words that I don’t follow.", 
            "Laboratory of talking machines.", 
            "House of commons.", 
            "Don’t alternate your flow, go here directly.", 
            "S O Ur Ti H kitchen",
            "The end is always a new beginning, return to where you started"]
    location_to_question_dict = {}
    for i in range(len(locations_list)):
        location_to_question_dict[locations_list[i]] = questions_list[i]
    #print(locations_list)
    ordered_location_list = generate_location_list(locations_list)
    location_to_key_dict = {}
    for location in ordered_location_list:
        unique_key = key_generator()
        location_to_key_dict[location] = unique_key

    first_key, list_to_print = upload_data_to_db(team_identifier, ordered_location_list, location_to_question_dict, location_to_key_dict)
    upload_oll = upload_ordered_location_name(team_identifier, ordered_location_list)

    return first_key
