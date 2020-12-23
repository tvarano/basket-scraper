from flask import Flask, render_template, request, g
import json

app = Flask(__name__)
DATABASE = 'odds.db'

@app.route("/")
def home(): 
    return "why are you here"

@app.route('/put', methods=['POST'])
def put_odds(): 

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE)


@app.teardown_appcontext
def close_connection(exception): 
    db = getattr(g, '_database', None)
    if db is not None: 
        db.close()