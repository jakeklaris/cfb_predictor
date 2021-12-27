"""
CFB_PREDICTOR (main) view

URLs include:
/
"""
import flask
import cfb_predictor 
from cfb_predictor.views.predict import predict

@cfb_predictor.app.route('/')
def show_index():
    """Display / route."""

    print(flask.request.method)
    print(flask.request.args)
    if len(flask.request.args) == 0:
        return flask.render_template("index.html", 
        **{
            'empty': True
        })

    req = flask.request.args

    neutral_site = True if req['neutral_site'] == 'yes' else False
    week = int(req['week'])
    home_team = req['home_team']
    away_team = req['away_team']

    teams = {
        'home': home_team,
        'away': away_team
    }

    N = 3

    sum_linear = 0
    sum_lasso = 0
    sum_neural = 0

    for i in range(N):
        cur_linear, cur_lasso, cur_neural = predict(home_team,away_team,week,neutral_site)
        sum_linear += cur_linear
        sum_lasso += cur_lasso
        sum_neural += cur_neural
    
    linear = sum_linear / N
    lasso = sum_lasso / N
    neural = sum_neural / N

    linear = round(linear,1)
    lasso = round(lasso,1)
    neural = round(neural,1)
    average_prediction = round((linear + lasso + neural) / 3, 1)

    predictions = {
        'linear': linear,
        'lasso': lasso,
        'neural': neural
    }

    context = {
        'week': week,
        'neutral_site': neutral_site,
        'teams': teams,
        'predictions': predictions,
        'empty': False,
        'average': average_prediction
    }
    return flask.render_template("index.html", **context)

@cfb_predictor.app.route('/about/')
def show_about():
    return flask.render_template("about.html")