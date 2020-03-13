from predict import predict
import warnings
warnings.filterwarnings("ignore")
import logging
logging.getLogger('tensorflow').disabled = True


round1_matchups = [('Duke', 'North Dakota State'), ('Virginia Commonwealth', 'Central Florida'), ('Mississippi State', 'Liberty'), ('Virginia Tech', 'Saint Louis'), ('Maryland', 'Belmont'), ('Minnesota', 'Louisville'), ('Yale', 'Louisiana State'), ('Michigan State', 'Bradley'), ('Gonzaga', 'Fairleigh Dickinson'), ('Syracuse', 'Baylor'), ('Marquette', 'Murray State'), ('Vermont', 'Florida State'), ('Buffalo', 'Arizona State'), ('Texas Tech', 'Northern Kentucky'), ('Nevada', 'Florida'), ('Michigan', 'Montana'), ('Virginia', 'Gardner-Webb'), ('Mississippi', 'Oklahoma'), ('Wisconsin', 'Oregon'), ('Kansas State', 'UC-Irvine'), ('Villanova', "Saint Mary's (CA)"), ('Purdue', 'Old Dominion'), ('Cincinnati', 'Iowa'), ('Tennessee', 'Colgate'), ('North Carolina', 'Iona'), ('Utah State', 'Washington'), ('Auburn', 'New Mexico State'), ('Kansas', 'Northeastern'), ('Iowa State', 'Ohio State'), ('Houston', 'Georgia State'), ('Wofford', 'Seton Hall'), ('Kentucky', 'Abilene Christian')]

round2_matchups = [('Duke', 'Virginia Commonwealth'), ('Liberty', 'Virginia Tech'), ('Maryland', 'Louisiana State'), ('Minnesota', 'Michigan State'), ('Gonzaga', 'Syracuse'), ('Marquette', 'Florida State'), ('Buffalo', 'Texas Tech'), ('Florida', 'Michigan'), ('Virginia', 'Oklahoma'), ('Oregon', 'UC-Irvine'), ("Saint Mary's (CA)", 'Purdue'), ('Cincinnati', 'Tennessee'), ('North Carolina', 'Washington'), ('Auburn', 'Kansas'), ('Iowa State', 'Houston'), ('Wofford', 'Kentucky')]

round3_matchups = [('Duke', 'Virginia Tech'), ('Louisiana State', 'Michigan'), ('Gonzaga', 'Florida State'), ('Texas Tech', 'Michigan'), ('Virginia', 'Oregon'), ('Purdue', 'Tennessee'), ('North Carolina', 'Auburn'), ('Houston', 'Kentucky')]

round4_matchups = [('Duke', 'Michigan State'), ('Gonzaga', 'Texas Tech'), ('Virginia', 'Tennessee'), ('Auburn', 'Houston')]

round5_matchups = [('Michigan State', 'Gonzaga'), ('Virginia', 'Auburn')]

final =  [('Michigan State', 'Auburn')]

rounds = [('First Round', round1_matchups), ('Second Round', round2_matchups), ('Third Round', round3_matchups), ('Fourth Round', round4_matchups), ('Final Four', round5_matchups), ('NCAA Champsionship', final)]

for r in rounds:
    print(r[0])
    matchups = r[1]
    for matchup in matchups:
        results = predict(2019, matchup[0], matchup[1])[0][0]
        if results[0] > results[1]:
            print("{} vs. {}: {} wins.".format(matchup[0], matchup[1], matchup[1]))
        else:
            print("{} vs. {}: {} wins.".format(matchup[0], matchup[1], matchup[0]))
