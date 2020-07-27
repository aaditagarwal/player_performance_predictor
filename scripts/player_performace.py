import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initializing Models
    #XGBoost
from xgboost import XGBClassifier
xgb = XGBClassifier(objective='multi:softmax')
    #RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(random_state=42)
    #SupportVectorMachine
from sklearn.svm import SVC
svc = SVC()

def player_performance(param,player_name,opposition=None,venue=None):

    res = {}

    #Extracting Targets and Features
    if param == 1:
    	overall_batsman_details = pd.read_excel('./player_details/overall_batsman_details.xlsx', header=0)
        match_batsman_details = pd.read_excel('./player_details/match_batsman_details.xlsx',header=0)
        match_batsman_details.loc[:, 'date'].ffill(inplace=True)

        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bat_overall_details = overall_batsman_details[overall_batsman_details['player_name']==player_name]
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bat_targets = bat_match_details.loc[:,['runs']]
            
    elif param == 2:
    	overall_bowler_details = pd.read_excel('./player_details/overall_bowler_details.xlsx',header=0)
        match_bowler_details = pd.read_excel('./player_details/match_bowler_details.xlsx',header=0)
        match_bowler_details.loc[:, 'date'].ffill(inplace=True)

        bowl_match_details = match_bowler_details[match_bowler_details['name']==player_name]
        bowl_overall_details = overall_bowler_details[overall_bowler_details['player_name']==player_name]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bowl_targets = bowl_match_details.loc[:,['wickets']]

    elif param == 3:
        overall_batsman_details = pd.read_excel('./player_details/overall_batsman_details.xlsx', header=0)
        match_batsman_details = pd.read_excel('./player_details/match_batsman_details.xlsx',header=0)
        overall_bowler_details = pd.read_excel('./player_details/overall_bowler_details.xlsx',header=0)
        match_bowler_details = pd.read_excel('./player_details/match_bowler_details.xlsx',header=0)
        match_batsman_details.loc[:, 'date'].ffill(inplace=True)
        match_bowler_details.loc[:, 'date'].ffill(inplace=True)

        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bowl_match_details = match_bowler_details[match_bowler_details['name'] == player_name]
        bat_overall_details = overall_batsman_details[overall_batsman_details['player_name']==player_name][['player_name','team','innings','runs','average','strike_rate','centuries','fifties','zeros']]
        bat_overall_details = overall_bowler_details[overall_bowler_details['player_name']==player_name][['player_name','team','innings','wickets','average','strike_rate','economy','wicket_hauls']]
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bat_targets = bat_match_details.loc[['runs']]
        bowl_targets = bowl_match_details.loc[['wickets']]

    #Pre_Processing
    le = preprocessing.LabelEncoder()
    sc = StandardScaler()

    #BatsmanPrediction
    if (param == 1 or param == 3):
        
        #Categorizing Runs
        bins = [0,30,60,100,250]
        labels = ["0","1","2","3"]
        bat_targets = pd.cut(bat_targets,bins,labels=labels,include_lowest=True)
        
        #Categorizing Opposition and Venue
        le.fit(bat_features.loc[:,['opposition']])
        opp_bat = le.transform([opposition])
        le.fit(bat_features.loc[:,['venue']])
        ven_bat = le.transform([venue])
        bat_features.loc[:,['opposition']] = le.fit_transform(bat_features.loc[:,['opposition']])
        bat_features.loc[:,['venue']] = le.fit_transform(bat_features.loc[:,['venue']])

        predict_bat = bat_overall_details[['innings','average','strike_rate','centuries','fifties','zeros']].values[0]
        
        #Scaling Non-Categorical Features
        bat_means = bat_features.loc[:,['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros']].mean()
        bat_std = bat_features.loc[:,['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros']].std()
        predict_bat = ((predict_bat-bat_means)/bat_std).tolist()
        bat_features.loc[:,['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros']] = sc.fit_transform(bat_features.loc[:,['innings_played','previous_average','previous_strike_rate','previous_centuries','previous_fifties','previous_zeros']])
        
        predict_bat.insert(0,ven_bat[0])
        predict_bat.insert(0,opp_bat[0])

        #Array
        bat_features.values
        bat_targets.values
        predict_bat_features = np.array(predict_bat).reshape(-1,1)
        predict_bat_features = predict_bat_features.T

        print('Batting Parameters Tuning begins...')
        
        #ParameterTuningformodels
        best_score = None
        best_params = None
            #XGBoost
        parameters = {'n_estimators':[75,100,125],'learning_rate':[0.1,0.01],'booster':['gbtree','dart']}
        gridsearch_xgb = GridSearchCV(estimator=xgb_model,param_grid=parameters,scoring='accuracy',cv=2)
        gridresult_xgb = gridsearch_xgb.fit(bat_features,bat_targets)
        xgb_best_score = gridresult_xgb.best_score_
        xgb_best_params = gridresult_xgb.best_params_
        best_score = [xgb_best_score,'xgb']
        best_params = xgb_best_params
            #RandomForestClassifier
        parameters = {'n_estimators':[75,100,125],'criterion':['gini','entropy'],'min_samples_leaf':[1,2,3]}
        gridsearch_rfc = GridSearchCV(estimator=rfc_model,param_grid=parameters,scoring='accuracy',cv=2)
        gridresult_rfc = gridsearch_rfc.fit(bat_features,bat_targets)
        rfc_best_score = gridresult_rfc.best_score_
        if best_score[0] < rfc_best_score:
            best_score = [rfc_best_score,'rfc']
            best_params = gridresult_rfc.best_params_
            #SupportVectorMachine
        parameters = {'C':[1,5,10],'kernel':['rbf','linear','sigmoid'],'gamma':['auto','scale']}
        gridsearch_svc = GridSearchCV(estimator=svc_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridresult_svc = gridsearch_svc.fit(bat_features,bat_targets)
        svc_best_score = gridresult_svc.best_score_
        if best_score[0] < svc_best_score:
            best_params = gridresult_svc.best_params_
            best_score = [svc_best_score,'svc']

        print(f'Batting Prediction Accuracy={best_score[0]} with classifier={best_score[1]}')
        
        print('Batting Prediction begins...')
        
        #FinalModeling
            #XGBoost
        if best_score[1] == 'xgb':
            classifier = XGBclassifier(objective='multi:softmax',n_estimators=best_params['n_estimators'],learning_rate=best_params['learning_rate'],booster=best_params['booster'])
            classifier = classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features[0])}
            #RandomForestClassifier
        elif best_score[1] == 'rfc':
            classifier = RandomForestClassifier(n_estimators=best_params['n_estiamtors'],criterion=best_params['criterion'],random_state=42,min_samples_leaf=best_params['min_samples_leaf'])
            classifier = classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features[0])}
            #SupportVectorMachine
        elif best_score[1] == 'svc':
            classifier = SVC(C=best_params['C'],kernel=best_params['kernel'],gamma=best_params['gamma'])
            classifier = classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features[0])}
 
        print('Batting Prediction Ends!')

    #BowlerPrediciton 
    if (param == 2 or param == 3):
        
        #Categorizing Runs
        bins = [0,1,3,6,10]
        labels = ['0','1','2','3']
        bowl_targets = pd.cut(bowl_targets['wickets'],bins,right=False,labels=labels,include_lowest=True)
        
        #Categorizing Opposition and Venue
        le.fit(bowl_features['opposition'])
        opp_bowl = le.transform([opposition])
        le.fit(bowl_features['venue'])
        ven_bowl = le.transform([venue])
        bowl_features['opposition'] = le.fit_transform(bowl_features['opposition'])
        bowl_features['venue'] = le.fit_transform(bowl_features['venue'])

        predict_bowl = bowl_overall_details[['innings','average','strike_rate','economy','wicket_hauls']].values[0]
        
        #Scaling Non-Categorical Features
        bowl_means = bowl_features.loc[:,['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']].mean()
        bowl_std = bowl_features.loc[:,['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']].std()
        predict_bowl = ((predict_bowl-bowl_means)/bowl_std).tolist()
        bowl_features.loc[:,['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']] = sc.fit_transform(bowl_features.loc[:,['innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']])

        predict_bowl.insert(0, ven_bowl[0])
        predict_bowl.insert(0, opp_bowl[0])

        #Array 
        bowl_features.values
        bowl_targets.values
        predict_bowl_features = np.array(predict_bowl).reshape(-1,1)
        predict_bowl_features = predict_bowl_features.T

        print('Bowling Parameter Tuning begins...')

        #ParameterTuningformodels
        best_score = None
        best_params = None
            #XGBoost
        parameters = [{'n_estimators':[75,100,125],'learning_rate':[0.1,0.01],'booster':['gbtree','dart']}]
        gridsearch_xgb = GridSearchCV(estimator=xgb_model,param_grid=parameters,scoring='accuracy',cv=2)
        gridresult_xgb = gridsearch_xgb.fit(bowl_features,bowl_targets)
        xgb_best_score = gridresult_xgb.best_score_
        xgb_best_params = gridresult_xgb.best_params_
        best_score = [xgb_best_score,'xgb']
        best_params = xgb_best_params
            #RandomForestClassifier
        parameters = [{'n_estimators':[75,100,125],'criterion':['gini','entropy'],'min_leaf_samples':[1,2,3]}]
        gridsearch_rfc = GridSearchCV(estimator=rfc_model,param_grid=parameters,scoring='accuracy',cv=2)
        gridresult_rfc = gridsearch_rfc.fit(bowl_features,bowl_targets)
        rfc_best_score = gridresult_rfc.best_score_
        if best_score[0] < rfc_best_score:
            best_score = [rfc_best_score,'rfc']
            best_params = gridresult_rfc.best_params_
            #SupportVectorMachine
        parameters = [{'C':[1,5,10],'kernel':['rbf','linear','sigmoid'],'gamma':['auto','scale']}]
        gridsearch_svc = GridSearchCV(estimator=svc_model,param_grid=parameters,scoring='accuracy',cv=2)
        gridresult_svc = gridsearch_svc.fit(bowl_features,bowl_targets)
        svc_best_score = gridresult_svc.best_score_
        if best_score[0] < svc_best_score:
            best_params = gridresult_svc.best_params_
            best_score = [svc_best_score,'svc']

        print(f'The bowling prediction accuracy={best_score[0]} with classifier={best_score[1]}')
        
        print('Bowling Prediction begins...')
        
        #FinalModeling
            
            #XGBoost
        if best_score[1] == 'xgb':
            classifier = XGBclassifier(objective='multi:softmax',n_estimators=best_params['n_estimators'],learning_rate=best_params['learning_rate'],booster=best_params['booster'])
            classifier = classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features[0])}
            #RandomForestClassifier
        elif best_score[1] == 'rfc':
            classifier = RandomForestClassifier(n_estimators=best_params['n_estiamtors'],criterion=best_params['criterion'],random_state=42,min_samples_leaf=best_params['min_leaf_samples'])
            classifier = classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features[0])}
            #SupportVectorMachine
        elif best_score[1] == 'svc':
            classifier = SVC(C=best_params['C'],kernel=best_params['kernel'],gamma=best_params['gamma'])
            classifier = classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features[0])}

        print('Bowling Prediction Ends!')

    return res