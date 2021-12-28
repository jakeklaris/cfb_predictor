import pathlib
from fastai.learner import load
import numpy as np
import pandas as pd
from fastai.tabular import *
from fastai.tabular.all import *

from views.data import create_data_frame
from views.rankings import load_rankings


class NeuralNet:

    def __init__(self,rankings,data):
        self.rankings = rankings
        self.df = data
    
    def create_model(self, test_size=.1):
        self.test_df = self.df.sample(frac = test_size)
        self.train_df = self.df.drop(self.test_df.index)
        
        excluded = ['GameID','Week','Home_Team','Away_Team','Score_Diff','Real_Odds']
        categorical = ['Conference_Game', 'Neutral_Site']
        continuous = [c for c in self.df.columns.to_list() if c not in categorical and c not in excluded]

        # split training data into training and validation sets
        splits = RandomSplitter(valid_pct=0.2)(range_of(self.train_df))
        table = TabularPandas(self.train_df, 
                    procs=[Categorify, Normalize],
                    y_names="Score_Diff",
                    cat_names = categorical,
                    cont_names = continuous,
                    splits=splits)
        
        self.dls = table.dataloaders(bs=64)
            
        # train the model
        self.learn = tabular_learner(self.dls, metrics=mae, lr=10e-3)
        self.learn.fit(4)

        # cwd = pathlib.Path(os.getcwd())
        # self.learn.path = cwd/'trained_models'
        # self.learn.export('neural1.pkl')

    def predict_from_trained(self, single_df, file):
        path = pathlib.Path(os.getcwd())/'trained_models'
        file_path = path/file
        model = load_learner(file_path)
        dl = model.dls.test_dl(single_df)
        prediction = model.get_preds(dl=dl)[0].numpy()    
        return prediction

    def predict_single(self, single_df):
        dl = self.learn.dls.test_dl(single_df)
        prediction = self.learn.get_preds(dl=dl)[0].numpy()    
        return prediction

    def predict(self,row):
        return 'Home' if row['Predicted_Margin'] > row['Real_Odds'] else 'Away'

    def check_result(self, row):
        return 'Home' if row['Score_Diff'] > row['Real_Odds'] else 'Away'

    def predict_against_spread(self, train=False):
        # print df with predicted score margin

        predicted_df = self.train_df.copy() if train else self.test_df.copy()
        dl = self.learn.dls.test_dl(predicted_df)
        predicted_df['Predicted_Margin'] = self.learn.get_preds(dl=dl)[0].numpy()

        # generate prediction on whether to take Home or Away against spread
        predicted_df['Prediction'] = predicted_df.apply(lambda row: self.predict(row), axis=1)
        self.prediction_df = predicted_df

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

    # create Neural Network
    neural_net = NeuralNet(team_rankings,data)
    neural_net.create_model()

    # run and evaluate neural net on training data
    percent_correct, num_trials = neural_net.predict_against_spread(train=True)
    print("{}% Correct over {} Predictions on Training Data\n".format(percent_correct*100, num_trials))

    # run and evaluate neural net on testing data
    percent_correct, num_trials = neural_net.predict_against_spread(train=False)
    print("{}% Correct over {} Predictions on Test Data\n".format(percent_correct*100, num_trials))
      

if __name__ == '__main__':
    main()
