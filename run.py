#Importing Libraries
import pandas as pd
import numpy as np
# import scripts.player_performance
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
        if check_list_1:
            if res in check_list_1:
                return res
                flag += 1
            else:
                flag -= 1
        if check_list_2:
            if res in check_list_2:
                return res
                flag += 1
            else:
                flag -= 1
        if flag < 0:
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
    print('Available Services:\n1. Specific Player Performance\n2. Team Selection')
    choice = input('Enter desired service:')
    while True:
        try:
            choice = int(choice)
            choice == 1 | choice == 2
        except:
            print('invalid input.')
            continue
        else:
            
            if choice == 1:
                team = input_values('team', match_batsman_details['team'].unique().tolist())
                player_name = input_values('player name', match_batsman_details[match_batsman_details['team'] == team]['name'].unique().tolist(), match_bowler_details[match_bowler_details['team'] == team]['name'].unique().tolist())
                flag = (input('Specific opposition:\n"yes" or "no": ')).lower()
                if flag == 'yes':
                    opposition = input_values('opposition', match_batsman_details[match_batsman_details['name']==player_name]['opposition'].unique().tolist(), match_bowler_details[match_bowler_details['name'] == player_name]['opposition'].unique().tolist())
                option = (input('Specified venue:\n"yes" or "no": ')).lower()
                if option =='yes':
                    venue = input_values('venue', match_batsman_details[match_batsman_details['name']==player_name]['venue'].unique().tolist(), match_bowler_details[match_bowler_details['name']==player_name]['venue'].unique().tolist())
                if flag=='no': 
                    if option=='no':
                        res = player_performance(player_name,team)
                    else:
                        res = player_performance(player_name,team,None,venue)
                else:
                    if option=='no':
                        res = player_performance(player_name,team,opposition)
                    else:
                        res = player_performance(player_name,team,opposition,venue)
                exit()
    
            elif choice == 2:
                team1 = input_values('team1', match_batsman_details['team'].unique().tolist(), match_bowler_details['team'].unique().tolist())
                team2 = input_values('team2', match_batsman_details[match_batsman_details['team']==team1]['opposition'].unique().tolist(), match_bowler_details[match_bowler_details['team']==team1]['opposition'].unique().tolist())
                res = team_performance(team1,team2)
                exit()