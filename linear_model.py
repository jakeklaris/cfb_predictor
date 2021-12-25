import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn import metrics

from data import create_data_frame
from rankings import load_rankings

def create_model(df):
    pass

def main():
    team_rankings = load_rankings()
    df = create_data_frame(team_rankings)
    create_model(df)

if __name__ == '__main__':
    main()