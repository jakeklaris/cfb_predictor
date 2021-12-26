import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn import metrics

from data import create_data_frame
from rankings import load_rankings

class RegressionModel:

    def __init__(self,rankings,data,model_type):
        assert(model_type in ['Linear','Lasso'])
        self.rankings = rankings
        self.model_type = model_type
        self.df = data
    
    def create_model(self):
        self.df.replace({'Conference_Game': {True: 1, False: 0}}, inplace=True)
        self.df.replace({'Neutral_Site': {True: 1, False: 0}}, inplace=True)

        features = self.df.drop(['GameID','Week','Home_Team','Away_Team','Score_Diff','Real_Odds'], axis=1)
        labels = self.df['Score_Diff']
        self.descriptions = self.df[['GameID','Week','Home_Team','Away_Team','Real_Odds']]

        # Split data into training and test data
        self.train_features, self.test_features, self.train_labels, self.test_labels = \
            train_test_split(features, labels, test_size=0.1, random_state=3)
        
        # Train linear regression model
        if self.model_type == 'Linear':
            self.model = LinearRegression()
            print("Generated Linear Regression Model\n")
        elif self.model_type == 'Lasso':
            self.model = Lasso()
            print("Generated Lasso Regression Model\n")


        self.model.fit(self.train_features, self.train_labels)
    
    def evaluate_model(self,plot=False,train=False):
        features = self.train_features if train else self.test_features
        actual_labels = self.train_labels if train else self.test_labels
        
        self.predicted_labels = self.model.predict(features)

        r_squared_error = metrics.r2_score(actual_labels, self.predicted_labels)
        mean_squared_error = metrics.mean_squared_error(actual_labels, self.predicted_labels)

        message = "Training" if train else "Test"
        print(message, "Data Error: r^2: {}".format(str(r_squared_error)))
        print(message, "Data Error: MSE: {}".format(str(mean_squared_error)))

        if plot:
            # Visualize the actual and predicting margin of scores
            plt.scatter(actual_labels, self.predicted_labels)
            plt.xlabel("Actual Score Margin")
            plt.ylabel("Predicted Score Margin")
            plt.title("Actual vs Predicted Score Margin")
            plt.show()
    
    def predict(self,row):
        return 'Home' if row['Predicted_Margin'] > row['Vegas_Spread'] else 'Away'

    def check_result(self, row):
        return 'Home' if row['Real_Margin'] > row['Vegas_Spread'] else 'Away'

    def predict_against_spread(self, train=False):
        # print df with predicted score margin

        prediction_df = self.train_features.copy() \
            if train else self.test_features.copy()
        
        prediction_df['Real_Margin'] = self.train_labels \
            if train else self.test_labels
        
        prediction_df['Predicted_Margin'] = self.predicted_labels
        prediction_df['Vegas_Spread'] = self.descriptions['Real_Odds']
        prediction_df['Prediction'] = prediction_df.apply(lambda row: self.predict(row), axis=1)
        self.prediction_df = prediction_df

        # check prediction correctness
        self.prediction_df['Correct'] = \
            self.prediction_df.apply(lambda row: self.check_result(row), axis=1)

        self.prediction_df['Won'] = \
            self.prediction_df['Correct'] == self.prediction_df['Prediction']

        num_correct = self.prediction_df[self.prediction_df.Won == True].shape[0]
        num_predictions = self.prediction_df.shape[0]

        percent_correct = num_correct / num_predictions
        return percent_correct, num_predictions


def main():
    # load team SP+ rankings and full DataFrame
    team_rankings = load_rankings()
    data = create_data_frame(team_rankings)

    # create Linear model
    model = RegressionModel(team_rankings, data, 'Linear')
    model.create_model()

    # run and evaluate model on training data
    model.evaluate_model(train=True)
    percent_correct, num_trials = model.predict_against_spread(train=True)
    print("{}% Correct over {} Predictions\n".format(percent_correct*100, num_trials))

    # run and evaluate model on test data
    model.evaluate_model(train=False)
    percent_correct, num_trials = model.predict_against_spread(train=False)
    print("{}% Correct over {} Predictions\n".format(percent_correct*100, num_trials))


    # create Lasso model
    model = RegressionModel(team_rankings, data, 'Lasso')
    model.create_model()

    # run and evaluate model on training data
    model.evaluate_model(train=True)
    percent_correct, num_trials = model.predict_against_spread(train=True)
    print("{}% Correct over {} Predictions\n".format(percent_correct*100, num_trials))

    # run and evaluate model on test data
    model.evaluate_model(train=False)
    percent_correct, num_trials = model.predict_against_spread(train=False)
    print("{}% Correct over {} Predictions\n".format(percent_correct*100, num_trials))


if __name__ == '__main__':
    main()