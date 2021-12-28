from views.linear_model import RegressionModel
from views.neural_model import NeuralNet
from views.data import create_single_data_frame, create_data_frame
from views.rankings import load_rankings

def predict(home_team, away_team, week, neutral, fileno):
    # load team SP+ rankings and create DataFrame for game and old data
    team_rankings = load_rankings()
    new_game = create_single_data_frame(team_rankings, home_team=home_team, \
        away_team=away_team, neutral_site=neutral, week=week)
    training_games = create_data_frame(team_rankings)

    # create Linear model
    # linear_model = RegressionModel(team_rankings, training_games, 'Linear')
    # linear_model.create_model(test_size=.05)
    # linear_model.evaluate_model()
    # linear_prediction = linear_model.predict_single(new_game)[0]

    linear_model = RegressionModel(team_rankings, training_games, 'Linear')
    linear_file = 'linear' + str(fileno) + '.sav'
    linear_prediction = linear_model.predict_from_trained(new_game, linear_file)[0]

    # create Lasso model
    # lasso_model = RegressionModel(team_rankings, training_games, 'Lasso')
    # lasso_model.create_model(test_size=.05)
    # lasso_model.evaluate_model()
    # lasso_prediction = lasso_model.predict_single(new_game)[0]

    lasso_model = RegressionModel(team_rankings, training_games, 'Lasso')
    lasso_file = 'lasso' + str(fileno) + '.sav'
    lasso_prediction = lasso_model.predict_from_trained(new_game, lasso_file)[0]
    
    # create Neural Net
    # neural_net = NeuralNet(team_rankings,training_games)
    # neural_net.create_model(test_size=0)
    # neural_prediction = neural_net.predict_single(new_game)[0][0]


    # neural_net = NeuralNet(team_rankings,training_games)
    # neural_file = 'neural' + str(fileno) + '.pkl'
    # neural_prediction = neural_net.predict_from_trained(new_game, neural_file)[0][0]

    neural_prediction = 0

    print("Predictions: ")
    print("Linear: {}".format(linear_prediction))
    print("Lasso: {}".format(lasso_prediction))
    print("Neural Net: {}".format(neural_prediction))

    return linear_prediction, lasso_prediction, neural_prediction

if __name__ == '__main__':
    predict()
    