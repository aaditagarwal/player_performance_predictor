#Importing Libraries
import pandas as pd
import numpy as np
import scripts.player_performance
import scripts.team_performance

#Input Function
def input_values(input_column, input_value):
    print(*match_batsman_details[input_column].unique(), sep='\n')
    while True:
        res = input(f'Enter the desired {input_value}: ')
        if input_column == 'index':
            if res in match_batsman_details.index:
                return res
            else:
                print('Invalid input.')
                continue
        else:
            if res in match_batsman_details[input_column].unique():
                return res
            else:
                print('Invalid input.')
                continue

if __name__ == '__main__':
    
    #Data Loading
    overall_batsman_details = pd.read_excel('./player_details/overall_batsman_details.xlsx',header=0,index_col=0)
    match_batsman_details = pd.read_excel('./player_details/match_batsman_details.xlsx',header=0)
    overall_bowler_details = pd.read_excel('./player_details/overall_bowler_details.xlsx',header=0,index_col=0)
    match_bowler_details = pd.read_excel('./player_details/match_bowler_details.xlsx',header=0)

    #Data Cleaning
    #match_batsman_details
    match_batsman_details.loc[:, 'date'].ffill(inplace=True)
    match_batsman_details.set_index(['date', 'name'], inplace=True, drop=True)
    #match_bowler_details
    match_bowler_details.loc[:, 'date'].ffill(inplace=True)
    match_bowler_details.set_index(['date', 'name'], inplace=True, drop=True)

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
                player_name = input_values('index','player name')
                opposition = input_values('team', 'opposition')
                option = input('For specified venue\n yes or no:')
                if option.lower != 'yes' or 'no':
                    option = 'no'
                if option =='yes':
                    venue = input_values('venue', 'venue')
                    res = player_performance(player_name,opposition,venue)
                else:
                    res = player_performance(player_name,opposition)
            elif choice == 2:
                team1 = input_values('team','team')
                team2 = input_values('team','team')
                option = input('For specified venue\n yes or no:')
                if option.lower != 'yes' or 'no':
                    option = 'no'
                if option == 'yes':
                    venue = input_values('venue', 'venue')
                    res = team_performance(player_name,opposition,venue)
                else:
                    res = team_performance(player_name,opposition)