from nba_api_helpers import get_age
import time
import json
import datetime
import numpy as np
from nba_api_helpers import get_awards_points
import pandas

continuing_sess = False
###############################
path_ActPlyrs2017 = "C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerDashboard\\ActPlyrs12017\\"
path_CPI = "C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\CommonPlayerInfo\\"
open_json = open("C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerAwards\\PlayerAwards.json")
open_awards_json = json.load(open_json)
open_json.close()

out_data = []

now = datetime.datetime.now()
year_now = now.year
###############################
open_actplayers = open(path_ActPlyrs2017 + 'ActivePlayers2017.json')
players = json.load(open_actplayers)
open_actplayers.close()
regression_open = open("C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\regression_yearbyyear_GP40_MPG10.json")
regression_data = json.load(regression_open)
regression_open.close()

for player in players:
    if (player['DashBasic'][0]['GP'] > 40) and (player['DashBasic'][0]['MIN'] > 10):

        dash = {'DashBasic': player['DashBasic'], 'DashAdvanced': player['DashAdvanced']}

        # Get the name of the CPI file to open
        full_name = str(player['full_name'])
        index = full_name.find(' ')
        # add this pairing of [player, season] to array
        first_name = full_name[:index]
        last_name = full_name[index+1:]
        str_to_open = '{}_{}_cpi.json'.format(last_name, first_name)
        open_CPI = open(path_CPI + str_to_open)
        CPI = json.load(open_CPI)
        open_CPI.close()

        # Find out how many seasons of experience each player has
        # seasons_exp = CPI['CommonPlayerInfo'][0]['SEASON_EXP'] + 1
        # above: is the old way I would determine this. Instead, I fixed it to look at each FPoints_History file, and determine which one is the highest year file that the player appears in. His seasons of experience is one less than this
        seasons_exp = 0
        for i in range(2,20):
            seasons_exp += 1
            open_FPointsHistory = open(
                'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerDashboard\\BySeason\\FPoints_History\\Player_FPoints_History_Y{}.json'.format(
                    i))
            FPointsHistory = json.load(open_FPointsHistory)
            open_FPointsHistory.close()
            try:
                FPointsHistory_array = FPointsHistory[full_name]
            except:
                break

        if seasons_exp < 17:
            # Go and retrieve all of their past seasons of history from that Player_FPoints_History_YX.son file
            if seasons_exp == 1:
                FPointsHistory_array = []
            else:
                open_FPointsHistory = open('C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerDashboard\\BySeason\\FPoints_History\\Player_FPoints_History_Y{}.json'.format(seasons_exp))
                FPointsHistory = json.load(open_FPointsHistory)
                open_FPointsHistory.close()
                # try:
                FPointsHistory_array = FPointsHistory[full_name]
                # except:
                #     pass

            # Get the players stats for this most recent season
            # Age
            age_now = get_age(CPI["CommonPlayerInfo"][0]["BIRTHDATE"])
            AGE = age_now #- (year_now - int(player[2][:4])) (dont need this part)

            # SEASONS_IN_LEAGUE =
            # Going to leave this blank for now

            # Draft pick number
            draft_round = CPI["CommonPlayerInfo"][0]["DRAFT_ROUND"]
            draft_number = CPI["CommonPlayerInfo"][0]["DRAFT_NUMBER"]
            if (draft_number == "Undrafted") or (draft_number == None):
                DRAFT_PICK_NUMBER = 70
            else:
                DRAFT_PICK_NUMBER = int(draft_number)

            # Minutes per game
            MPG = dash["DashBasic"][0]["MIN"]

            # Games played
            GP = dash["DashBasic"][0]["GP"]

            # Player efficiency
            PIE = dash["DashAdvanced"][0]["PIE"]

            # Usage
            USG = dash["DashAdvanced"][0]["USG_PCT"]

            # True Shooting
            TS = dash["DashAdvanced"][0]["TS_PCT"]

            # Field goals made
            FGM = dash["DashBasic"][0]["FGM"]

            # Field goals attempted
            FGA = dash["DashBasic"][0]["FGA"]

            # Free throws made
            FTM = dash["DashBasic"][0]["FTM"]

            # Free throws attempted
            FTA = dash["DashBasic"][0]["FTA"]

            # Rebounds per game
            REB = dash["DashBasic"][0]["REB"]

            # Assists per game
            AST = dash["DashBasic"][0]["AST"]

            # Steals per game
            STL = dash["DashBasic"][0]["STL"]

            # Blocks per game
            BLK = dash["DashBasic"][0]["BLK"]

            # Turnovers per game
            TOV = dash["DashBasic"][0]["TOV"]

            # Points per game
            PTS = dash["DashBasic"][0]["PTS"]

            # ------------------- Points from Awards -------------------#
            # Compute how many points this player got from awards

            ## Get awards points
            year_str = player['DashBasic'][0]['GROUP_VALUE']
            AWARDS_POINTS = get_awards_points(player['player_id'], year_str, open_awards_json)

            # ----------------------------------------------------------#
            ###############################
            # Name and year of player
            NAME_YEAR = full_name + " ({})".format('2017-18')

            # Add all of this to a dataframe and store in a CSV
            training_example = [NAME_YEAR, AGE, DRAFT_PICK_NUMBER, MPG, GP, PIE, USG, TS, FGM, FGA, FTM, FTA, REB, AST, STL, BLK, TOV, PTS, AWARDS_POINTS]

            features = ["Name", "Age", "Draft_pick_number", "MPG", "GP", "PIE", "USG", "TS", "FGM", "FGA",
                        "FTM", "FTA", "REB", "AST", "STL", "BLK", "TOV", "PTS", "AWARDS_POINTS"]



            for ind in range(0, len(FPointsHistory_array)):
                features.append("FPoints_Y{}".format((ind+1)))
            for fpoints in FPointsHistory_array:
                training_example.append(fpoints)

            # load regression data
            reg_dict = regression_data["Year{}".format(seasons_exp)][0]
            thetas = reg_dict['thetas']
            mu = reg_dict['mu']
            sigma = reg_dict['sigma']

            X = training_example[1:]

            X_norm = [(X_-mu_)/sigma_ for X_,mu_,sigma_ in zip(X,mu,sigma)]
            X_norm = [1] + X_norm

            projection = np.sum([X_norm_*thetas_ for X_norm_,thetas_ in zip(X_norm, thetas)])
            if len(FPointsHistory_array)==0:
                FPointsHistory_array = [0]
            training_example = [training_example[0]] + [FPointsHistory_array[-1]] + [projection] + training_example[1:]
            training_example = training_example[0:21]

            out_data.append(training_example)

        else:
            print("Left {} out of analysis".format(player['full_name']))

features = ["Name", "FPoints N-1", "Projection", "Age", "Draft_pick_number", "MPG", "GP", "PIE", "USG", "TS", "FGM", "FGA", "FTM", "FTA", "REB", "AST", "STL", "BLK", "TOV", "PTS", "AWARDS_POINTS"]
###############################
with pandas.ExcelWriter("C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\projections_everyyear_12017.xlsx") as writer:
    df_wprojections = pandas.DataFrame(out_data, columns=features)
    df_wprojections.to_excel(writer)