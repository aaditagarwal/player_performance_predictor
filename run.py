#Importing Libraries
import pandas as pd
import numpy as np
from scripts.player_performance.py import player_performance
# import scripts.team_performance

#Input Function
def input_values(input_value, check_list_1=None, check_list_2=None):
    if check_list_1:
        print(f'Available {input_value} : \n',*check_list_1, sep='\t')
    if check_list_2:
        print(f'Available {input_value} : \n',*check_list_2, sep='\t')
    while True:
        flag = 0
        res = input(f'Enter the desired {input_value}: ')
        if check_list_1 != None:
            if res in check_list_1:
                flag += 1
        if check_list_2 != None:
            if res in check_list_2:
                flag += 2
        if flag > 0:
            return flag,res
        else:
            print('Invalid input.')
            continue

if __name__ == '__main__':
    
    #Data Loading
    overall_batsman_details = pd.read_excel('./player_details/overall_batsman_details.xlsx',header=0,index_col=0)
    match_batsman_details = pd.read_excel('./player_details/match_batsman_details.xlsx',header=0)
    overall_bowler_details = pd.read_excel('./player_details/overall_bowler_details.xlsx',header=0,index_col=0)
    match_bowler_details = pd.read_excel('./player_details/match_bowler_details.xlsx',header=0)

    #Filiing Missing Values
        #match_batsman_details
    match_batsman_details.loc[:, 'date'].ffill(inplace=True)
        #match_bowler_details
    match_bowler_details.loc[:, 'date'].ffill(inplace=True)

    #Input's
    print('Available Services:\nSpecific Player Performance\n')
    team,dump = input_values('team', match_batsman_details['team'].unique().tolist())
    player_name, param_player = input_values('player_name', match_batsman_details[match_batsman_details['team'] == team]['name'].unique().tolist(), match_bowler_details[match_bowler_details['team'] == team]['name'].unique().tolist())
    opposition, param_opp = input_values('opposition', match_batsman_details[match_batsman_details['name']==player_name]['opposition'].unique().tolist(), match_bowler_details[match_bowler_details['name'] == player_name]['opposition'].unique().tolist())
    venue, param_ven = input_values('venue', match_batsman_details[match_batsman_details['name']==player_name]['venue'].unique().tolist(), match_bowler_details[match_bowler_details['name']==player_name]['venue'].unique().tolist())
    param = param_player
    if param > param_opp:
        param = param_opp
    if param > param_ven:
        param = param_ven
    res = player_performance(param,player_name,team,opposition,venue)
    print(res)
    exit()