import cfbd

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

def get_games(year, week):
    api = configure_game_api()
    # get all games
    response = api.get_games(year=year)
    games = [g.to_dict() for g in response]
    return games

def get_real_odds():
    odds = {}
    api = configure_betting_api()
    response = api.get_lines(year=2021)
    lines = [l.to_dict() for l in response]
    for line in lines:
        try:
            odds[line['id']] = float(line['lines'][0]['spread']) * -1
        except TypeError:
            print("couldnt get spread for game {}".format(line['id']))
    return odds
    