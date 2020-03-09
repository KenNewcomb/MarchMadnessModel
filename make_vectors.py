'''make_vectors.py: Convert the raw data into cleaned vectors ready for learning.'''
import json
import pickle
import pandas as pd
from tqdm import tqdm
import numpy as np

# 1) Import every NCAA Tournament game from 1993-2019
with open('data/march_madness.json') as f:
    all_games = [i for i in json.load(f) if int(i['fields']['year']) >= 1993 and int(i['fields']['year']) < 2018]
print("Using {} games.".format(len(all_games)))

# 2) Process seasonal histories
years = {}
for year in tqdm(range(1993, 2020), desc='Processing years'):
    with open('data/{}data'.format(year), 'r') as f:
        print(year)
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
        data = data[['School', 'WinLossPCT', 'SRS', 'SOS', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'FGPCT', '3PPCT', 'FTPCT', 'TRB', 'AST', 'STL', 'BLK', 'TOV']]
        
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
    years[year] = {'data': data, 'adv_data': adv_data, 'rat_data': rat_data}

# 2) Iterate over games, making x/y vectors.
X_data = []
y_data = []
for game in tqdm(all_games, desc="Processing NCAA Bracket History..."):
    # Make x vectors
    year = int(game['fields']['year'])
    team1 = game['fields']['team_1']
    team2 = game['fields']['team_2']
    seed1 = game['fields']['seed_1']
    seed2 = game['fields']['seed_2']

    year_data = years[year]['data']
    year_adv_data = years[year]['adv_data']
    year_rat_data = years[year]['rat_data']

    d1 = year_data.loc[year_data['School'] == team1]
    d2 = year_data.loc[year_data['School'] == team2]
    ad1 = year_adv_data.loc[year_adv_data['School'] == team1]
    ad2 = year_adv_data.loc[year_adv_data['School'] == team2]
    rat1 = year_rat_data.loc[year_rat_data['School'] == team1]
    rat2 = year_rat_data.loc[year_rat_data['School'] == team2]

    total_d1 = d1.merge(ad1, on='School').merge(rat1, on='School').drop(columns=['School']).values
    total_d2 = d2.merge(ad2, on='School').merge(rat2, on='School').drop(columns=['School']).values
    X  = np.concatenate([total_d1, total_d2], axis=1)[0]
    Xa = np.concatenate([total_d2, total_d1], axis=1)[0]
    X_data.append(X)
    X_data.append(Xa)

    # Make y vectors
    score1 = int(game['fields']['score_1'])
    score2 = int(game['fields']['score_2'])

    if score1 > score2:
        y = 1
        y_other = 0
    elif score1 < score2:
        y = 0
        y_other = 1
    y_data.append(y)
    y_data.append(y_other)

    # Add other combination of win/loss
    # x = [seed1, seed2, t1_wlpercent, t1_srs, t1_sos, t1_fgp, t1_3pa, t1_ftp, t1_ftr, t1_3par, t1_ts, t1_ast, t2_wlpercent, t2_srs, t2_sos, t2_fgp, t2_3pa, t2_ftp, t2_ftr, t2_3par, t2_ts, t2_ast]

    #x_other = [t2_wlpercent, t2_srs, t2_sos, t2_fgp, t2_3pa, t2_ftp, t2_orb, t2_stl, t2_blk, t2_tov, t2_pf, t2_ftr, t2_3par, t2_ts, t2_trb, t2_ast, t2_pts, t2_opp, t2_mov, t1_wlpercent, t1_srs, t1_sos, t1_fgp, t1_3pa, t1_ftp, t1_orb, t1_stl, t1_blk, t1_tov, t1_pf, t1_ftr, t1_3par, t1_ts, t1_trb, t1_ast, t1_pts, t1_opp, t1_mov]
    #X_data.append(x_other)
    #y_data.append(y_other)
print(len(X_data))
print(X_data[0])
print(X_data[1])
print(y_data[0])
print(y_data[1])
    



with open('vectors/X_data', 'wb') as f:
    pickle.dump(X_data, f)
with open('vectors/y_data', 'wb') as f:
    pickle.dump(y_data, f)

