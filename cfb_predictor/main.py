import flask
from views.rankings import load_rankings
from views.predict import predict
from views.rankings import load_rankings_from_disc

app = flask.Flask(__name__)

@app.route('/')
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


    team_rankings = load_rankings()

    # max 5 --> 5 trained models per ml type
    N = 1

    sum_linear = 0
    sum_lasso = 0
    sum_neural = 0


    for i in range(N):
        cur_linear, cur_lasso, cur_neural = predict(home_team,away_team,week,neutral_site,i,team_rankings)
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

@app.route('/about/')
def show_about():
    return flask.render_template("about.html")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)