import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_URL'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
    return conn

locations_list = ["bvj_entry", "history", "journalism", "biology","math", "physics", "psychology", "iot", "english", "electronics", "chemistry", "bvj_exit"]

conn = get_db_connection()
for location in locations_list:
    cur = conn.cursor()
    try:
        query = f'CREATE TABLE IF NOT EXISTS public."{location}" (id SERIAL PRIMARY KEY NOT NULL, entered_unique_key TEXT NOT NULL, team_name TEXT NOT NULL, next_riddle TEXT NOT NULL, next_unique_key TEXT NOT NULL);'
        cur.execute(query)
    except Exception as err:
        print(err)
    conn.commit()
    cur.close()

conn.close()



