# Player Prediction Predictor

Predicting cricket player's performance to decide the playing 11 for an One Day International match using Machine Learning. 

## Data Acquiistion

The data for the player's information and stats are scrapped from [Espncricinfo](https://www.espncricinfo.com/ci/content/player/index.html) website using the Parsehub application. The application is free and available at [parsehub.com](https://www.parsehub.com).

## Player Stats 

#### Batsman Information
1.	 inninings		- The number of innings played by the batsman.\
					  This gives us an insight into the experience of the batsman.
2.	 average 		- The average of runs scored by the batsman.\
					  This provides us with the batsman's scoring abilities as well as consistency.
3.	 strike_rate	- The rate of scoring runs by the batsman.\
					  This provides us with the pace at which the batsman can score, which is crucial in limited overs matches.
4.	 centuries		- The number of centuries scored by the batsman.
5.	 fifties		- The number of fifties scored by the batsman.\
					  These stats provide us with the achievements of the batsman.
6.	 highest_scored - The highest score scored by the batsman.
7.	 not_outs		- The number of innings the batsman hasn't been dismissed.

#### Bowler Information
1.	 inninings 		- The number of innings player by the bowler.
2.	 overs			- The number of overs bowled by the player.\
					  These stats give us an insight into the experience of the bowler.
3.	 average		- The numbers of runs consided by the bowler per wicket taken.\
					  This provides us with information about the bowler's capabilities.
4.	 strike_rate	- The number of balls bowled by the bowler per wicket taken.\
					  This provides us with the pace at which the bowler can take wickets.
5.	 Wicket Hauls	- The number of four/five wickets hauls taken by the bowler.\
					  This provides us with the achievements of the bowler.

## Derived Stats
1.	 consistency - This attribute represents how experienced and consistent the player is.
2.	 form 		 - This attribute represents the player’s current form.
3.	 opposition	 - This attribute represents the player’s performance against the team with which
the match is being played.
4.	 venue		 - This attribute represents the player’s performance at the ground at which the match is
being played.