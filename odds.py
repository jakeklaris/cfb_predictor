import cfbd
import logging

def configure_game_api():
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = '4N4aszEtEwy4YdL5AyNyQO9zSv0y+4MoQDr8uc8DB/PuzLixp6+XPUAESEv89ncA'
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    return api_instance

def configure_betting_api():
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = '4N4aszEtEwy4YdL5AyNyQO9zSv0y+4MoQDr8uc8DB/PuzLixp6+XPUAESEv89ncA'
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_instance = cfbd.BettingApi(cfbd.ApiClient(configuration))
    return api_instance

def configure_ratings_api():
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = '4N4aszEtEwy4YdL5AyNyQO9zSv0y+4MoQDr8uc8DB/PuzLixp6+XPUAESEv89ncA'
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_instance = cfbd.RatingsApi(cfbd.ApiClient(configuration))
    return api_instance    

def get_games(year, week):
    api = configure_game_api()
    # get all games
    response = api.get_games(year=year)
    games = [g.to_dict() for g in response]
    return games

def get_elo_diff(home_team, away_team, week, year=2021):
    api = configure_ratings_api()
    response1 = api.get_elo_ratings(year=year, week=week,team=home_team)
    response2 = api.get_elo_ratings(year=year, week=week,team=away_team)

    elos = [response1[0].to_dict(), response2[0].to_dict()]
    return float(elos[0]['elo']) - float(elos[1]['elo']), \
        elos[0]['conference'] == elos[1]['conference']

def get_real_odds():
    odds = {}
    api = configure_betting_api()
    response = api.get_lines(year=2021)
    lines = [l.to_dict() for l in response]
    for line in lines:
        try:
            odds[line['id']] = float(line['lines'][0]['spread']) * -1
        except TypeError:
            logging.info("couldnt get spread for game {}".format(line['id']))
            odds[line['id']] = 1000
    return odds
 
if __name__ == '__main__':
    print(get_elo_diff('Rutgers', 'Michigan', 5))