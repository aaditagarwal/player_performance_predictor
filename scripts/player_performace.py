import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def player_performance(param,player_name,opposition=None,venue=None):

    overall_batsman_details = pd.read_excel('./../player_details/overall_batsman_details.xlsx', header=0)
    match_batsman_details = pd.read_excel('./../player_details/match_batsman_details.xlsx',header=0)
    overall_bowler_details = pd.read_excel('./../player_details/overall_bowler_details.xlsx',header=0)
    match_bowler_details = pd.read_excel('./../player_details/match_bowler_details.xlsx',header=0)
    match_batsman_details.loc[:, 'date'].ffill(inplace=True)
    match_bowler_details.loc[:, 'date'].ffill(inplace=True)

    #Extracting Targets and Features

    if param == 1:
        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bat_overall_details = overall_batsman_details.loc['player_name',:]
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bat_targets = bat_match_details.loc[:,['runs']]
    elif param == 2:
        bowl_match_details = match_bowler_details[match_bowler_details['name']==player_name]
        bowl_overall_details = overall_bowler_details.loc['player_name',:]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bowl_targets = bowl_match_details.loc[:,['wickets']]

    elif param == 3:
        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bowl_match_details = match_bowler_details[match_bowler_details['name'] == player_name]
        #match_details = bat_details.merge(bowl_details, how='outer', left_on=['date', 'name', 'team', 'opposition', 'venue'], right_on=['date', 'name', 'team', 'opposition', 'venue'], suffixes=['_bat', '_bowl'])
        bat_overall_details = overall_batsman_details[overall_batsman_details['player_name']==player_name][['player_name','team','innings','runs','average','strike_rate','centuries','fifties','zeros']]
        bat_overall_details = overall_bowler_details[overall_bowler_details['player_name']==player_name][['player_name','team','innings','wickets','average','strike_rate','economy','wicket_hauls']]
        #overall_details = overall_bat_details.merge(overall_bowl_details, how='outer', left_on=['player_name', 'team'], right_on=['player_name', 'team'], suffixes=['_bat', '_bowl'])
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bat_targets = bat_match_details.loc[['runs']]
        bowl_targets = bowl_match_details.loc[['wickets']]

    le = preprocessing.LabelEncoder()
    sc = StandardScaler()

    if bat_match_details:
            #Categorizing Runs
        bins = [0,30,60,100,250]
        labels = ["0","1","2","3"]
        bat_targets = pd.cut(bat_targets,bins,labels=labels,include_lowest=True)
            #Categorizing Opposition and Venue
        bat_features.loc[:,['opposition']] = le.fit_transform(bat_features.loc[:,['opposition']])
        bat_features.loc[:,['venue']] = le.fit_transform(bat_features.loc[:,['venue']])
            #Scaling Non-Categorical Features
        bat_features['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros'] = sc.fit_transform(bat_features['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros'])

    if bowl_match_details:
            #Categorizing Runs
        bins = [0,1,3,6,10]
        labels = ['0','1','2','3']
        bowl_targets = pd.cut(bowl_targets['wickets'],bins,right=False,labels=labels,include_lowest=True)
            #Categorizing Opposition and Venue
        bowl_features['opposition'] = le.fit_transform(bowl_features['opposition'])
        bowl_features['venue'] = le.fit_transform(bowl_features['venue'])
            #Scaling Non-Categorical Features
        bowl_features['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls'] = sc.fit_transform(bowl_features['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls'])

    # Initializing Models