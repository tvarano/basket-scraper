import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import re

# Constants
sports = ['football','soccer','basketball','golf','ufc-mma','tennis','baseball','boxing','hockey']
filter_headers = ['MatchId', 'Team', 'OddsWin', 'OddsTie', 'Sport', 'Country', 'League', 'DateTime', 'Completed']

def to_filter(k, v): 
    if k == 'Team': 
        return ('(TeamOne = ? OR TeamTwo = ?)', [v, v])
    elif k == 'OddsWin': 
        return ('(OddsOne = ? OR OddsTwo = ?)', [v, v])
    else: 
        return (f'{k} = ?', [v])

def filter_query(json_obj): 
    query = 'SELECT * FROM odds WHERE'
    inputs = []
    for k, v in json_obj
        to_f = to_filter(k, v)
        query += f' {to_f[0]} AND'
        inputs += to_f[1]
    
    # take off last and
    return (query[:len(query) - 4], inputs)

@dataclass_json
@dataclass
class Match:
    team1: str
    team2: str
    odds1: float
    odds2: float
    oddsDraw: float
    description: str
    sport: str
    country: str
    league: str
    time: int
    matchID: int

def getSoccerMatches():
    url_for_leagues = "https://services.bovada.lv/services/sports/event/v2/nav/A/description/soccer?lang=en"

    leagues = requests.get(url_for_leagues).json()['children']
    links = []

    # Gets links for all active soccer leagues/competitions
    for l in leagues:
        links.append(l['link'])

    # Initializes list of Matches, then iterates through each league to gather active matches.
    matches = []
    for l in links:
        url = "https://www.bovada.lv/services/sports/event/v2/events/A/description" + l
        
        r = requests.get(url).json()

        try:
            events = r[0]['events']
            for e in events:
                if e['type'] == 'GAMEEVENT':
                    try:
                        description = e['description']
                        matchID = e['id']
                        team1 = e['competitors'][0]['name']
                        team2 = e['competitors'][1]['name']
                        sport = e['sport']
                        lc = parse_lc(re.search("/soccer/([A-Za-z-]+)", l)[1])
                        league = lc[1]
                        country = lc[0]
                        time = e['startTime']
                    except Exception as e:
                        print(e)
                        print("Invalid event - " + l)

                    for m in e['displayGroups'][0]['markets']:
                        if m['description'] == '3-Way Moneyline' and m['period']['description'] == 'Regulation Time':
                            try:
                                for outcome in m['outcomes']:
                                    if outcome['description'] == team1:
                                        odds1 = outcome['price']['decimal']
                                    if outcome['description'] == team2:
                                        odds2 = outcome['price']['decimal']
                                    if outcome['description'] == 'Draw':
                                        oddsDraw = outcome['price']['decimal']
                                match = Match(team1, team2, odds1, odds2, oddsDraw, description, sport, country, league, time, matchID)
                                matches.append(match)
                            except:
                                print("Odds not valid " + l)
        except:
            print("Invalid response at " + l)
    
    return matches    

# def to_json(matches): 
    
# return country, league
def parse_lc(reg): 
    if reg == 'uefa-champions-league':
        return ("UEFA Champions League", "UEFA Champions League")
    elif reg == "south-america": 
        return ("South America", "South America")
    elif "-" in reg:
        sp = reg.split("-")
        return (sp[0].capitalize(), reg[len(sp[0])+1:].capitalize())
    else: 
        return (reg.capitalize(), reg.replace("-", " ").capitalize())

if __name__ == '__main__':
    mat = getSoccerMatches()
    for m in mat: 
        print(m)