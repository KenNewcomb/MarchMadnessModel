import numpy as np
import pandas as pd
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.preprocessing.text import Tokenizer

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
def predict(year, team1, team2):
	with open('data/{}data'.format(year), 'r') as f:
		headers = ['School', 'OverallGames', 'OverallWins', 'OverallLosses', 'WinLossPCT', 'SRS', 'SOS', 'ConfWins', 'ConfLosses', 'HomeWins', 'HomeLosses', 'AwayWins', 'AwayLosses', 'TeamPoints', 'OppPoints', 'DC1','MP', 'FG', 'FGA', 'FGPCT', '3P', '3PA', '3PPCT', 'FT', 'FTA', 'FTPCT', 'ORB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
		data = pd.read_csv(f, index_col=False, names=headers)
		data.dropna(axis='columns',  inplace=True, how='all')
		data.drop(columns=['MP'], inplace=True)
		data.fillna(data.mean(), inplace=True)

		# Normalize certain columns
		data['SRS']=(data['SRS']-data['SRS'].mean())/data['SRS'].std()
		data['SOS']=(data['SOS']-data['SOS'].mean())/data['SOS'].std()
		data['FG']=(data['FG']-data['FG'].mean())/data['FG'].std()
		data['FGA']=(data['FGA']-data['FGA'].mean())/data['FGA'].std()
		data['3P']=(data['3P']-data['3P'].mean())/data['3P'].std()
		data['3PA']=(data['3PA']-data['3PA'].mean())/data['3PA'].std()
		data['FT']=(data['FT']-data['FT'].mean())/data['FT'].std()
		data['FTA']=(data['FTA']-data['FTA'].mean())/data['FTA'].std()
		data['TRB']=(data['TRB']-data['TRB'].mean())/data['TRB'].std()
		data['AST']=(data['AST']-data['AST'].mean())/data['AST'].std()
		data['STL']=(data['STL']-data['STL'].mean())/data['STL'].std()
		data['BLK']=(data['BLK']-data['BLK'].mean())/data['BLK'].std()
		data['TOV']=(data['TOV']-data['TOV'].mean())/data['TOV'].std()
		if year == 2002: # Personal fouls are messed up from this year. Use last year's number for the team
		    data['PF'] = 0
		else:
		    data['PF']=(data['PF']-data['PF'].mean())/data['PF'].std()
		data = data[['School', 'WinLossPCT', 'SRS', 'SOS', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'FGPCT', '3PPCT', 'FTPCT', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']]

	with open('data/{}dataadvanced'.format(year), 'r') as f:
		headers = ['School', 'OverallGames', 'OverallWins', 'OverallLosses', 'WinLossPCT', 'SRS', 'SOS', 'ConfWins', 'ConfLosses', 'HomeWins', 'HomeLosses', 'AwayWins', 'AwayLosses', 'TeamPoints', 'OppPoints', 'DropThisColumn','Pace', 'ORtg', 'FTr', '3PAr', 'TSPCT', 'TRBPCT', 'ASTPCT', 'STLPCT', 'BLKPCT', 'EFGPCT', 'TOVPCT', 'ORBPCT', 'FTDIVFGA']
		adv_data = pd.read_csv(f, index_col=False, names=headers)
		adv_data.dropna(axis='columns',  inplace=True, how='all')
		adv_data.fillna(adv_data.mean(), inplace=True)

		adv_data = adv_data[['School', 'FTr', '3PAr', 'TSPCT', 'TRBPCT', 'ASTPCT', 'BLKPCT', 'EFGPCT', 'TOVPCT', 'FTDIVFGA']]

	with open('data/{}dataratings'.format(year), 'r') as f:
		headers = ['School', 'Conf', 'DC1', 'Win', 'Loss', 'Pts', 'Opp', 'MOV', 'DC2', 'SOS', 'DC3', 'OSRS', 'DSRS', 'SRS', 'ORtg','DRtg', 'NRtg']
		rat_data = pd.read_csv(f, index_col=False, names=headers)
		rat_data.dropna(axis='columns',  inplace=True, how='all')
		rat_data.fillna(rat_data.mean(), inplace=True)
		rat_data['Pts']=(rat_data['Pts']-rat_data['Pts'].mean())/rat_data['Pts'].std()
		rat_data['Opp']=(rat_data['Opp']-rat_data['Opp'].mean())/rat_data['Opp'].std()
		rat_data['MOV']=(rat_data['MOV']-rat_data['MOV'].mean())/rat_data['MOV'].std()
		rat_data['OSRS']=(rat_data['OSRS']-rat_data['OSRS'].mean())/rat_data['OSRS'].std()
		rat_data['DSRS']=(rat_data['DSRS']-rat_data['DSRS'].mean())/rat_data['DSRS'].std()
		rat_data = rat_data[['School', 'Pts', 'Opp', 'MOV', 'OSRS', 'DSRS']]

	d1 = data.loc[data['School'] == team1]
	d2 = data.loc[data['School'] == team2]
	ad1 = adv_data.loc[adv_data['School'] == team1]
	ad2 = adv_data.loc[adv_data['School'] == team2]
	rat1 = rat_data.loc[rat_data['School'] == team1]
	rat2 = rat_data.loc[rat_data['School'] == team2]
	try:
		total_d1 = d1.merge(ad1, on='School').merge(rat1, on='School').drop(columns=['School']).values
		total_d2 = d2.merge(ad2, on='School').merge(rat2, on='School').drop(columns=['School']).values
		x  = np.concatenate([total_d1, total_d2], axis=1)[0]
	except ValueError:
		print("Issue producing vectors for teams {} {} {}".format(team1, team2, year))
		exit()
	model = tf.keras.models.load_model('model.h5')
	x = np.asarray(x)
	x = np.reshape(x, (1, 64))
	return(model.predict([np.asarray(x)]))
