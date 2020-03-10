from predict import predict
import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger('tensorflow').disabled = True


matchups = [('Minnesota', 'Louisville'), ('Yale', 'Louisiana State'), ('Vermont', 'Florida State'), ('Belmont', 'Maryland'), ('Villanova', 'Purdue'), ('Auburn', 'North Carolina')]

for matchup in matchups:
    results = predict(2019, matchup[0], matchup[1])[0][0]
    if results[0] > results[1]:
        print("{} vs. {}: {} wins.".format(matchup[0], matchup[1], matchup[1]))
    else:
        print("{} vs. {}: {} wins.".format(matchup[0], matchup[1], matchup[0]))

