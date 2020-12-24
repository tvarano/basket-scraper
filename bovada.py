import requests
from dataclasses import dataclass

# Constants
sports = ['football','soccer','basketball','golf','ufc-mma','tennis','baseball','boxing','hockey']

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
                        country = l
                        league = l
                        time = e['startTime']
                    except:
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

print(getSoccerMatches())