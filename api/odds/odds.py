from flask import Flask, render_template, request, g
import json
import datetime as DT
import sqlite3
import bovada

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
        cur.execute(("INSERT INTO odds "
                    "(MatchId, TeamOne, TeamTwo, Description, OddsOne, OddsTwo, OddsTie, Sport, Country, League, DateTime, Completed) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, false)"), 
                    (m.matchID, m.team1, m.team2, m.description, m.odds1,
                     m.odds2, m.oddsDraw, m.sport, m.country, m.league, m.time))

    json = "["
    for m in ms: 
        json += m.to_json() 
    return json + "]"
        

@app.route('/decided')
def get_decided(): 
    cur = get_db().cursor()
    # take the input for decided matches. 
    # update their "completed" information
    # clean week-old completed matches

@app.route('/put/decided')
def decide_matches():
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
        db.commit()
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