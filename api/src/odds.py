from flask import Flask, render_template, request, g
import json
import datetime as DT
import sqlite3

app = Flask(__name__)
DATABASE = 'odds.db'

@app.route("/")
def home(): 
    return "why are you here"

@app.route('/scrape', methods=['POST'])
def scrape_run(): 
    # check creds? no need to yet
    # insert
    cur = get_db().cursor()
        

@app.route('/decided', methods=['GET', 'POST'])
def decide_matches(): 
    cur = get_db().cursor()
    if request.method == 'POST':
        # take the input for decided matches. 
        # update their "completed" information
        # clean week-old completed matches
        cur.commit()
    else: 
        # get all decided matches
        cur.execute('SELECT * FROM odds WHERE Completed = true')

        rows = curr.fetchall()
        for r in rows: 
            print(row)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    print('db opened.')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        print('db closed.')
        db.close()

# given an array of matchids
# def insert_completed(matches): 


def clean_old_matches(): 
    cur = get_db().cursor()
    today = DT.date.today()
    yesterday = (today - DT.timedelta(days=1)).strftime("%Y-%m-%d")
    cur.execute('DELETE FROM odds WHERE Completed = true AND DateTime < ?', (yesterday))

def to_json(rows): 
    return "json"

if __name__ == '__main__':
    app.run()