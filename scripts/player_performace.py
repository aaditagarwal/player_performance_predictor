import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, cross_validation
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def player_performance(param,player_name,opposition=None,venue=None):

    res = {}

    overall_batsman_details = pd.read_excel('./../player_details/overall_batsman_details.xlsx', header=0)
    match_batsman_details = pd.read_excel('./../player_details/match_batsman_details.xlsx',header=0)
    overall_bowler_details = pd.read_excel('./../player_details/overall_bowler_details.xlsx',header=0)
    match_bowler_details = pd.read_excel('./../player_details/match_bowler_details.xlsx',header=0)
    match_batsman_details.loc[:, 'date'].ffill(inplace=True)
    match_bowler_details.loc[:, 'date'].ffill(inplace=True)

    # Initializing Models
        #XGBoost
    from xgboost import XGBClassifier
    def xgb_model(estimators,rate,boost):
        xgb = XGBClassifier(objective='multi:softmax',n_estimators=estimators,learning_rate=rate,booster=boost)
        return xgb    
        #RandomForestClassifier
    from sklearn.ensemble import RandomForestClassifier
    def rfc_model(estiamtors,criteria,leaf_split):
        rfc = RandomForestClassifier(n_estimators=estiamtors,criterion=criteria,random_state=42,min_samples_leaf=leaf_split)
        return rfc
        #SupportVectorMachine
    from sklearn.svm import SVC
    def svc_model(c,kernel,gamma):
        svc = SVC(C=c,kernel=kernel,gamma=gamma)
        return svc

    #Extracting Targets and Features
    if param == 1:
        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bat_overall_details = overall_batsman_details.loc['player_name',:]
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bat_targets = bat_match_details.loc[:,['runs']]
        predict_bat_features = [opposition, venue, bat_overall_details['innings'],bat_overall_details['average'],bat_overall_details['strike_rate'],bat_overall_details['centuries'],bat_overall_details['fifties'],bat_overall_details['zeros']]
    
    elif param == 2:
        bowl_match_details = match_bowler_details[match_bowler_details['name']==player_name]
        bowl_overall_details = overall_bowler_details.loc['player_name',:]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bowl_targets = bowl_match_details.loc[:,['wickets']]
        predict_bowl_features = [opposition, venue, bowl_overall_details['innings'],bowl_overall_details['average'],overall_bowler_details['strike_rate'],bowl_overall_details['economy'],bowl_overall_details['wicket_hauls']]

    elif param == 3:
        bat_match_details = match_batsman_details[match_batsman_details['name']==player_name]
        bowl_match_details = match_bowler_details[match_bowler_details['name'] == player_name]
        bat_overall_details = overall_batsman_details[overall_batsman_details['player_name']==player_name][['player_name','team','innings','runs','average','strike_rate','centuries','fifties','zeros']]
        bat_overall_details = overall_bowler_details[overall_bowler_details['player_name']==player_name][['player_name','team','innings','wickets','average','strike_rate','economy','wicket_hauls']]
        bat_features = bat_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_centuries','previous_fifties', 'previous_zeros']]
        bowl_features = bowl_match_details.loc[:,['opposition', 'venue', 'innings_played','previous_average', 'previous_strike_rate', 'previous_economy','previous_wicket_hauls']]
        bat_targets = bat_match_details.loc[['runs']]
        bowl_targets = bowl_match_details.loc[['wickets']]
        predict_bat_features = [opposition, venue, bat_overall_details['innings'],bat_overall_details['average'],bat_overall_details['strike_rate'],bat_overall_details['centuries'],bat_overall_details['fifties'],bat_overall_details['zeros']]
        predict_bowl_features = [opposition, venue, bowl_overall_details['innings'],bowl_overall_details['average'],overall_bowler_details['strike_rate'],bowl_overall_details['economy'],bowl_overall_details['wicket_hauls']]   

    #Pre_Processing
    le = preprocessing.LabelEncoder()
    sc = StandardScaler()

    #BatsmanPrediction
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
        
        #ParameterTuningformodels
        best_score = None
        best_params = None
            #XGBoost
        parameters = [{'estimators':[75,100,125],'rate':[0.1,0.01],'boost':['gbtree','dart']}]
        gridsearch_xgb = GridSearchCV(estimator=xgb_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_xgb.fit(bat_features,bat_targets)
        xgb_best_score = gridsearch_xgb.best_score_
        xgb_best_params = gridsearch_xgb.best_params_
        best_score = [xgb_best_score,'xgb']
        best_params = xgb_best_params
            #RandomForestClassifier
        parameters = [{'estimators':[75,100,125],'criteria':['gini','entropy'],'leaf_split':[1,2,3]}]
        gridsearch_rfc = GridSearchCV(estimator=rfc_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_rfc.fit(bat_features,bat_targets)
        rfc_best_score = gridsearch_rfc.best_score_
        if best_score < rfc_best_score:
            best_score = [rfc_best_score,'rfc']
            best_params = gridsearch_rfc.best_params_
            #SupportVectorMachine
        parameters = [{'c':[1,5,10],'kernel':['rbf','linear','sigmoid'],'gamma':['auto','scale']}]
        gridsearch_svc = GridSearchCV(estimator=svc_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_svc.fit(bat_features,bat_targets)
        svc_best_score = gridsearch_svc.best_score_
        if best_score < svc_best_score:
            best_params = gridsearch_svc.best_params_
            best_score = [svc_best_score,'svc']
        
        #FinalModeling
            #XGBoost
        if best_score[1] == 'xgb':
            classifier = XGBclassifier(objective='multi:softmax',n_estimators=best_params['estimators'],learning_rate=best_params['rate'],booster=best_params['boost'])
            classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features)}
            #RandomForestClassifier
        elif best_score[1] == 'rfc':
            classifier = RandomForestClassifier(n_estimators=best_params['estiamtors'],criterion=best_params['criteria'],random_state=42,min_samples_leaf=best_params['leaf_split'])
            classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features)}
            #SupportVectorMachine
        elif best_score[1] == 'svc':
            classifier = SVC(C=best_params['c'],kernel=best_params['kernel'],gamma=best_params['gamma'])
            classifier.fit(bat_features,bat_targets)
            res = {'bat_prediction':classifier.predict(predict_bowl_features)}
 
    #BowlerPrediciton 
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

        #ParameterTuningformodels
        best_score = None
        best_params = None
            #XGBoost
        parameters = [{'estimators':[75,100,125],'rate':[0.1,0.01],'boost':['gbtree','dart']}]
        gridsearch_xgb = GridSearchCV(estimator=xgb_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_xgb.fit(bowl_features,bowl_targets)
        xgb_best_score = gridsearch_xgb.best_score_
        xgb_best_params = gridsearch_xgb.best_params_
        best_score = [xgb_best_score,'xgb']
        best_params = xgb_best_params
            #RandomForestClassifier
        parameters = [{'estimators':[75,100,125],'criteria':['gini','entropy'],'leaf_split':[1,2,3]}]
        gridsearch_rfc = GridSearchCV(estimator=rfc_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_rfc.fit(bowl_features,bowl_targets)
        rfc_best_score = gridsearch_rfc.best_score_
        if best_score < rfc_best_score:
            best_score = [rfc_best_score,'rfc']
            best_params = gridsearch_rfc.best_params_
            #SupportVectorMachine
        parameters = [{'c':[1,5,10],'kernel':['rbf','linear','sigmoid'],'gamma':['auto','scale']}]
        gridsearch_svc = GridSearchCV(estimator=svc_model,param_grid=parameters,scoring='accuracy',cv=5)
        gridsearch_svc.fit(bowl_features,bowl_targets)
        svc_best_score = gridsearch_svc.best_score_
        if best_score < svc_best_score:
            best_params = gridsearch_svc.best_params_
            best_score = [svc_best_score,'svc']
        
        #FinalModeling
            
            #XGBoost
        if best_score[1] == 'xgb':
            classifier = XGBclassifier(objective='multi:softmax',n_estimators=best_params['estimators'],learning_rate=best_params['rate'],booster=best_params['boost'])
            classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features)}
            #RandomForestClassifier
        elif best_score[1] == 'rfc':
            classifier = RandomForestClassifier(n_estimators=best_params['estiamtors'],criterion=best_params['criteria'],random_state=42,min_samples_leaf=best_params['leaf_split'])
            classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features)}
            #SupportVectorMachine
        elif best_score[1] == 'svc':
            classifier = SVC(C=best_params['c'],kernel=best_params['kernel'],gamma=best_params['gamma'])
            classifier.fit(bowl_features,bowl_targets)
            res = {'bowl_prediction':classifier.predict(predict_bowl_features)}

    return res