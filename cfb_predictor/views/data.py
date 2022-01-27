import pandas as pd
import logging

from odds import get_real_odds, get_games, get_elo_diff
from rankings import get_diffs

def add_spreads(data):
    # data == list[list]
    lines = get_real_odds()
    for game in data:
        if game[0] in lines.keys():
            game.append(lines[game[0]])
        else:
            game.append(1000)

def create_single_data_frame(rankings, home_team, away_team, neutral_site, week, year=2021):
    o_dif, d_dif, st_dif = \
        get_diffs(week, home_team, away_team, rankings) 
    
    elo_dif, same_conference = get_elo_diff(home_team,away_team,week)
    data = []
    row = [
        0,
        week,
        home_team,
        away_team,
        o_dif,
        d_dif,
        st_dif,
        elo_dif,
        same_conference,
        neutral_site,
        0,
        0
    ]

    data.append(row)

    df = pd.DataFrame(data, columns = [
        'GameID',
        'Week',
        'Home_Team',
        'Away_Team',
        'SP+_Offense_Diff', 
        'SP+_Defense_Diff', 
        'SP+_Special_Teams_Diff', 
        'ELO_Diff',
        'Conference_Game', 
        'Neutral_Site', 
        'Score_Diff', 
        'Real_Odds'
        ])

    return df

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
            logging.info('Could not retrieve SP+ rankings for game {}, team 1: {}, team 2: {} in week {}'.format(game['id'], game['home_team'], game['away_team'], game['week']))
    
    add_spreads(data)

    df = pd.DataFrame(data, columns = [
        'GameID',
        'Week',
        'Home_Team',
        'Away_Team',
        'SP+_Offense_Diff', 
        'SP+_Defense_Diff', 
        'SP+_Special_Teams_Diff', 
        'ELO_Diff',
        'Conference_Game', 
        'Neutral_Site', 
        'Score_Diff', 
        'Real_Odds'
        ])
    
    return df
    