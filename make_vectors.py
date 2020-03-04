'''make_vectors.py: Convert the raw data into cleaned vectors ready for learning.'''
import json
import pickle

# 1) Import every NCAA Tournament game from 1993-2019
with open('data/march_madness.json') as f:
    all_games = [i for i in json.load(f) if int(i['fields']['year']) >= 1993 and int(i['fields']['year']) < 2018]
print("Using {} games.".format(len(all_games)))
# 2) Iterate over games, making x/y vectors.
#            "score_1": 94,
#            "score_2": 78,
#            "team_1": "Memphis",
#            "team_2": "Oral Roberts",
#            "region": "2",
#            "year": "2006",
#            "seed_1": 1,
#            "seed_2": 16,
#            "round": "1"
X_data = []
y_data = []
for game in all_games:
    # Make x vectors
    year = game['fields']['year']    
    team1 = game['fields']['team_1']
    team2 = game['fields']['team_2']
    seed1 = game['fields']['seed_1']
    seed2 = game['fields']['seed_2']
    with open('data/{}data'.format(year), 'r') as f:
        for line in f.readlines():
            this_line = line.split(',')
            if this_line[0] == team1:
                t1_wlpercent = float(this_line[4])
                t1_srs       = float(this_line[5])
                t1_sos       = float(this_line[6])
                t1_fgp       = float(this_line[19])
                t1_3pa       = float(this_line[22])
                t1_ftp       = float(this_line[25])
            elif this_line[0] == team2:
                t2_wlpercent = float(this_line[4])
                t2_srs       = float(this_line[5])
                t2_sos       = float(this_line[6])
                t2_fgp       = float(this_line[19])
                t2_3pa       = float(this_line[22])
                t2_ftp       = float(this_line[25])
    x = [seed1, seed2, t1_wlpercent, t1_srs, t1_sos, t1_fgp, t1_3pa, t1_ftp, t2_wlpercent, t2_srs, t2_sos, t2_fgp, t2_3pa, t2_ftp]
    X_data.append(x)
    # Make y vectors
    score1 = int(game['fields']['score_1'])
    score2 = int(game['fields']['score_2'])

    if score1 > score2:
        y = 0
    elif score1 < score2:
        y = 1
    y_data.append(y)


print(X_data[0])

with open('vectors/X_data', 'wb') as f:
    pickle.dump(X_data, f)
with open('vectors/y_data', 'wb') as f:
    pickle.dump(y_data, f)

