import pathlib
from cfb_predictor.config import RANKINGS_FOLDER

NAME_CHANGE = {
    'Ohio St.': 'Ohio State',
    'Penn St.': 'Penn State',
    'Iowa St.': 'Iowa State',
    'Arizona St.': 'Arizona State',
    'N. Carolina': 'North Carolina',
    'Va. Tech': 'Virginia Tech',
    'Coastal Caro.': 'Coastal Carolina',
    'NC St.': 'NC State',
    'Michigan St.': 'Michigan State',
    'Boston Coll.': 'Boston College',
    'Oklahoma St.': 'Oklahoma State',
    'App. St.': 'Appalachian State',
    'Kansas St.': 'Kansas State',
    'Florida St.': 'Florida State',
    'Boise St.': 'Boise State',
    'Miss. St.': 'Mississippi State',
    'Fresno St.': 'Fresno State',
    'W. Virginia': 'West Virginia',
    'Wash. St.': 'Washington State',
    'S. Carolina': 'South Carolina',
    'Ga. Tech': 'Georgia Tech',
    'San Diego St.': 'San Diego State',
    'Arkansas St.': 'Arkansas State',
    'Oregon St.': 'Oregon State',
    'WKU': 'Western Kentucky',
    'FIU': 'Florida International',
    'EMU': 'Eastern Michigan',
    'ECU': 'East Carolina',
    'Georgia St.': 'Georgia State',
    'MTSU': 'Middle Tennessee',
    'CMU': 'Central Michigan',
    'N. Texas': 'North Texas',
    'WMU': 'Western Michigan',
    'Ball St.': 'Ball State',
    'Ga. Southern': 'Georgia Southern',
    'Hawaii': "Hawai'i",
    'Utah St.': 'Utah State',
    'Colorado St.': 'Colorado State',
    'S. Alabama': 'South Alabama',
    'Kent St.': 'Kent State',
    'NIU': 'Northern Illinois',
    'La. Tech': 'Louisiana Tech',
    'So. Miss': 'Southern Mississippi',
    'Texas St.': 'Texas State',
    'USF': 'South Florida',
    'Miami-OH': 'Miami (OH)',
    'BGSU': 'Bowling Green',
    'ULM': 'Louisiana Monroe',
    'ODU': 'Old Dominion',
    'UConn': 'Connecticut',
    'NMSU': 'New Mexico State',
    'FAU': 'Florida Atlantic',
    'San Jose St.': 'San José State',
    'App. St.': 'Appalachian State'
}

def load_rankings():
    team_rankings = {}
    dir = pathlib.Path(RANKINGS_FOLDER)
    for i in range(2,16):
        path = f'week{i}rankings.csv'
        file_path = dir/path
        with open(file_path, 'r') as f:
            first = True
            lines = f.readlines()
            for line in lines:
                if first:
                    first = False
                    continue
                name, overall, offense, defense, special_teams = line.strip().split(',')

                # extract team name
                names = name.split()
                team_name = names[1]
                if len(names) > 3:
                    index = 2
                    while index < len(names) - 1:
                        team_name += ' ' 
                        team_name += names[index]
                        index += 1
                
                overall = float(overall)
                offense = float(offense.split()[0])
                defense = float(defense.split()[0])
                special_teams = float(special_teams.split()[0])

                ratings = {
                    'overall': overall,
                    'offense': offense,
                    'defense': defense,
                    'special_teams': special_teams
                }

                if team_name in NAME_CHANGE.keys():
                    team_name = NAME_CHANGE[team_name]

                if team_name not in team_rankings.keys():
                    team_rankings[team_name] = {}
                team_rankings[team_name][i] = ratings
    return team_rankings

def get_diffs(week, team1, team2, TEAM_RANKINGS):
    week = int(week)

    if team1 not in TEAM_RANKINGS.keys() or team2 not in TEAM_RANKINGS.keys():
        raise ValueError('invalid team names')

    if week not in TEAM_RANKINGS[team1].keys():
        raise ValueError('invalid week')

    rank_1_o = TEAM_RANKINGS[team1][week]['offense']
    rank_1_d = TEAM_RANKINGS[team1][week]['defense']
    rank_1_st = TEAM_RANKINGS[team1][week]['special_teams']
    rank_2_o = TEAM_RANKINGS[team2][week]['offense']
    rank_2_d = TEAM_RANKINGS[team2][week]['defense']
    rank_2_st = TEAM_RANKINGS[team2][week]['special_teams']

    return rank_1_o - rank_2_o, rank_1_d - rank_2_d, rank_1_st - rank_2_st
