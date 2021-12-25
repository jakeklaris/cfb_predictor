import pandas as pd

from odds import get_real_odds
from odds import get_games
from rankings import get_diffs

def add_spreads(data):
    # data == list[list]
    lines = get_real_odds()
    for game in data:
        if game[0] in lines.keys():
            game.append(lines[game[0]])
        else:
            game.append(1000)

def create_data_frame(rankings):
    # create pd df with:
    # SP+Diff (home - away), label = (home score - away score)
    
    # get all games
    game_data = get_games(year=2021, week=3)
    games = []
    for game in game_data:
        games.append({
            'id': game['id'],
            'week': game['week'],
            'home_team': game['home_team'],
            'away_team': game['away_team'],
            'home_score': game['home_points'],
            'away_score': game['away_points'],
            'conference_game': game['conference_game'],
            'neutral_site': game['neutral_site'],
            'home_elo' : game['home_pregame_elo'],
            'away_elo': game['away_pregame_elo']
        })
        
    data = []
    for game in games:
        try:
            o_dif, d_dif, st_dif = get_diffs(game['week'], game['home_team'], game['away_team'], rankings)
            cur_row = [
                game['id'],
                game['week'],
                game['home_team'],
                game['away_team'],
                o_dif,
                d_dif,
                st_dif,
                game['home_elo'] - game['away_elo'],
                game['conference_game'],
                game['neutral_site'],
                game['home_score'] - game['away_score'],
            ]
            data.append(cur_row)
        except (ValueError):
            print('Could not retrieve SP+ rankings for game {}, team 1: {}, team 2: {} in week {}'.format(game['id'], game['home_team'], game['away_team'], game['week']))
    
    add_spreads(data)

    df = pd.DataFrame(data, columns = [
        'GameID',
        'Week',
        'Home Team',
        'Away Team',
        'SP+ Offense Diff', 
        'SP+ Defense Diff', 
        'SP+ Special Teams Diff', 
        'ELO Dif',
        'Conference Game', 
        'Neutral Site', 
        'Score Diff', 
        'Real_Odds'
        ])
    
    return df