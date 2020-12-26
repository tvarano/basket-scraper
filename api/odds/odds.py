from flask import Flask, render_template, request, g
import json
import datetime as DT
import sqlite3
import bovada
import format_query

app = Flask(__name__)
DATABASE = 'odds.db'

@app.route("/")
def home(): 
    return "why are you here"

@app.route('/scrape', methods=['GET'])
def scrape_run(): 
    # check creds? no need to yet
    # insert
    ms = bovada.getSoccerMatches()
    cur = get_db().cursor()

    for m in ms:
        cur.execute(("INSERT OR REPLACE INTO odds "
                    "(MatchId, TeamOne, TeamTwo, Description, OddsOne, OddsTwo, OddsTie, Sport, Country, League, DateTime) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"), 
                    (m.MatchId, m.TeamOne, m.TeamTwo, m.Description, m.OddsOne,
                     m.OddsTwo, m.OddsTie, m.Sport, m.Country, m.League, m.DateTime))

    json = "["
    for m in ms: 
        json += m.to_json() + ", "
    return json.rstrip(", ") + "]"

# takes filter as json string {key: value}
@app.route('/search', methods=['GET', 'POST'])    
def get_matches(): 
    # if get, get all
    # if post, get according to filters
    cur = get_db().cursor()
    if request.method == 'GET': 
        cur.execute('SELECT * FROM odds')
    else: 
        fs = json.loads(request.data)
        # format for filters shown in dbformat file
        if len(fs) != 0: 
            q_i = format_query.filter_query(fs)
            cur.execute(q_i[0], tuple(q_i[1]))
        else: 
            cur.execute('SELECT * FROM odds')
        
    return format_query.to_json(cur.fetchall(), cur.description)
        
    
# just a shortcut for searching with completed=trues
@app.route('/decided')
def get_decided(): 
    cur = get_db().cursor()
    cur.execute('SELECT * FROM odds WHERE Completed = true')
    rows = cursor.fetchall()
    # take the input for decided matches. 
    # update their "completed" information
    # clean week-old completed matches
    return format_query.to_json(rows, cur.description)

@app.route('/put/decided')
def decide_matches():
    # get all decided matches

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
        db.commit()
        db.close()

# given an array of matchids
# def insert_completed(matches): 


def clean_old_matches(): 
    cur = get_db().cursor()
    today = DT.date.today()
    yesterday = (today - DT.timedelta(days=1)).strftime("%Y-%m-%d")
    cur.execute('DELETE FROM odds WHERE Completed = true AND DateTime < ?', (yesterday))

if __name__ == '__main__':
    app.run()