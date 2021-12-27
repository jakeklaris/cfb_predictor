from cfb_predictor.views.linear_model import RegressionModel
from cfb_predictor.views.neural_model import NeuralNet
from cfb_predictor.views.data import create_single_data_frame, create_data_frame
from cfb_predictor.views.rankings import load_rankings

def predict(home_team, away_team, week, neutral):
    # load team SP+ rankings and create DataFrame for game and old data
    team_rankings = load_rankings()
    new_game = create_single_data_frame(team_rankings, home_team=home_team, \
        away_team=away_team, neutral_site=neutral, week=week)
    training_games = create_data_frame(team_rankings)

    # create Linear model
    linear_model = RegressionModel(team_rankings, training_games, 'Linear')
    linear_model.create_model(test_size=.05)
    linear_prediction = linear_model.predict_single(new_game)[0]

    # create Lasso model
    lasso_model = RegressionModel(team_rankings, training_games, 'Lasso')
    lasso_model.create_model(test_size=.05)
    lasso_prediction = lasso_model.predict_single(new_game)[0]
    
    # create Neural Net
    neural_net = NeuralNet(team_rankings,training_games)
    neural_net.create_model(test_size=.05)
    neural_prediction = neural_net.predict_single(new_game)[0][0]

    print("Predictions: ")
    print("Linear: {}".format(linear_prediction))
    print("Lasso: {}".format(lasso_prediction))
    print("Neural Net: {}".format(neural_prediction))

    return linear_prediction, lasso_prediction, neural_prediction

if __name__ == '__main__':
    predict()
    