import json

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
    for k in json_obj:
        to_f = to_filter(k, json_obj[k])
        query += f' {to_f[0]} AND'
        inputs += to_f[1]
    
    # take off last and
    return (query[:len(query) - 4], inputs)

def to_json(rows, desc): 
    items = [dict(zip([key[0] for key in desc], row)) for row in rows]
    return json.dumps(items)