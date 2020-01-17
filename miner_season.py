from nba_api_helpers import *
from FPointsCalc import calc_fpoints_from_season
from FRules import *
import json
import datetime
import csv
import pandas
from regression import *


regression_yearbyyear = {}

GP_boundary = 15
MPG_boundary = 5

pl_count = 0
running_average_error = 0
running_average_error_denom=0

# Paths
path_BySeason = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerDashboard\\BySeason\\'
path_CommonPlayerInfo = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\CommonPlayerInfo\\'
path_Data = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\'
open_json = open("C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerAwards\\PlayerAwards.json")
open_awards_json = json.load(open_json)
open_json.close()

# Decide the number of seasons that we want to run this analysis for
number_seasons_to_analyze = 20
seasons_array = []
for i in range(1,number_seasons_to_analyze+1):
    seasons_array.append(i)

# Fantasy rules which we will use
rules = FRules
now = datetime.datetime.now()
year_now = now.year


with pandas.ExcelWriter("C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\player_data_everyyear_GP{}_MPG{}.xlsx".format(GP_boundary, MPG_boundary)) as writer:
    # Begin looping through each of the years (eg. Year1 through Year16)
    for season in seasons_array:

        # Determine which players had a fantasy score in year n+1 AND had all the feature data from year n
        #--# Get the list of players who have a json file in year n+1
        players_year_n1 = get_players_from_json_list(get_list_of_jsons_from_YearN(path_BySeason + 'Year{}'.format(season+1)))
        #--# Get the list of players who have a json file in year n
        players_year_n = get_players_from_json_list(get_list_of_jsons_from_YearN(path_BySeason + 'Year{}'.format(season)))
        #--# Create a new list of players who appear in both lists
        players_from_both_years = []
        for plyr_n1 in players_year_n1:
            for plyr_n in players_year_n:
                if (plyr_n1[0] + ' ' + plyr_n1[1]) == (plyr_n[0] + ' ' + plyr_n[1]):
                    players_from_both_years.append([plyr_n1[0], plyr_n1[1], plyr_n[2], plyr_n1[2]]) # [firstname, lastname, year1, year2]

        print("List of players from Year{}/Year{} analysis\n".format(season, season+1))
        print(players_from_both_years)
        print('\n')

        player_data = []
        player_dict_FPoints_data = {}

        # Loop through each of these players
        for player in players_from_both_years:

            # Compute the values of the features for this player for year n
            #--# First, load this player's CPI and dash. We need to go back to lastname_firstname format ...
            lastname_firstname = player[1] + '_' + player[0]
            cpi_open = open(path_CommonPlayerInfo + '{}_cpi.json'.format(lastname_firstname))
            dash_open = open(path_BySeason + 'Year{}\\{}_1{}_dash.json'.format(season, lastname_firstname, player[2][:4]))
            dash_n1_open = open(path_BySeason + 'Year{}\\{}_1{}_dash.json'.format(season+1, lastname_firstname, player[3][:4]))
            CPI = json.load(cpi_open)
            dash = json.load(dash_open)
            dash_N1 = json.load(dash_n1_open)
            cpi_open.close()
            dash_open.close()
            dash_n1_open.close()

            # Compute the number of fantasy points this player produced in year n+1
            #--# Get the ID for the person
            player_id = get_ID_from_fullname(player[0] + ' ' + player[1]) #player[0] is name of player 'Firstname Lastname'
            FPOINTS_N1 = calc_fpoints_from_season(player_id, rules, player[3], dash_N1) #season argument (player[3]) doesn't matter, it's using dash_N1 to compute

            #------------------- FPoints Years Previous --------------------#
            # Load the FPoints for previous years (list of values)
            if season == 1:
                FPOINTS_PAST = []
            else:
                FPoints_past_json = json.load(open(path_BySeason + 'FPoints_History\\Player_FPoints_History_Y{}.json'.format(season)))
                FPOINTS_PAST = FPoints_past_json[(player[0] + ' ' + player[1])]

            # Compute the fantasy points for this year, append it to array of FPoints from previous years
            FPOINTS_N = [calc_fpoints_from_season(player_id, rules, player[2], dash)]

            # Store this array into a dictionary with the player name, in the folder of the next year
            FPOINTS_N = FPOINTS_PAST + FPOINTS_N
            dict_fpoints_n = {(player[0] + ' ' + player[1]): FPOINTS_N}
            player_dict_FPoints_data.update(dict_fpoints_n)
            # --------------------------------------------------------------#

            # Age
            age_now = get_age(CPI["CommonPlayerInfo"][0]["BIRTHDATE"])
            AGE = age_now-(year_now - int(player[2][:4]))

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

            ## Find player in open JSON

            ## Get awards points
            year = player[2]
            AWARDS_POINTS = get_awards_points(player_id, year, open_awards_json)

            # ----------------------------------------------------------#

            # Name and year of player
            NAME_YEAR = player[0] + ' ' + player[1] + " ({})".format(player[2])

            # Add all of this to a dataframe and store in a CSV
            training_example = [NAME_YEAR, FPOINTS_N1, AGE, DRAFT_PICK_NUMBER, MPG, GP, PIE, USG, TS, FGM, FGA, FTM, FTA, REB, AST, STL, BLK, TOV, PTS, AWARDS_POINTS]

            # Need to add in this players past seasons of FPoints
            for ind in range(0, len(FPOINTS_PAST)):
                training_example.append(FPOINTS_PAST[ind])

            # Append all the seasons of past FPoints to this training example
            if (GP > GP_boundary) and (MPG > MPG_boundary):
                player_data.append(training_example)

        # Write fpoints dictionary to json
        Player_FPoints_History = open(path_BySeason + 'FPoints_History\\Player_FPoints_History_Y{}.json'.format(season+1), 'w')
        player_dict_FPoints_data_json = json.dumps(player_dict_FPoints_data)
        Player_FPoints_History.write(player_dict_FPoints_data_json)
        Player_FPoints_History.close()

        features = ["Name", "Fpoints_N1", "Age", "Draft_pick_number", "MPG", "GP", "PIE", "USG", "TS", "FGM", "FGA", "FTM", "FTA", "REB", "AST", "STL", "BLK", "TOV", "PTS", "AWARDS_POINTS"]
        years_history_fpoints = []
        for ind in range(0, len(FPOINTS_PAST)):
            years_history_fpoints.append(ind+1)
            features.append("FPoints Y{}".format((ind+1)))

        df = pandas.DataFrame(player_data, columns=features)

        [thetas, X, projections, mu, sigma] = regression(df, .1, 20, False)
        thetas = thetas.tolist()
        thetas=thetas[0]
        mu = mu.tolist()
        mu = mu[0]
        sigma = sigma.tolist()
        sigma=sigma[0]

        regression_yearbyyear.update({"Year{}".format(season): [{'thetas': thetas, 'mu': mu, 'sigma': sigma}]})

        player_data_wprojections = []
        for pr in range(0,len(projections)):
            error_between_proj_act_data = projections[pr] - player_data[pr][1]
            list_to_insert = player_data[pr][:1] + [error_between_proj_act_data] + [projections[pr]] + player_data[pr][1:]
            player_data_wprojections.append(list_to_insert)

        features_wprojections = features[:1] + ["Projection_error"] + ["Projection"] + features[1:]
        df_wprojections = pandas.DataFrame(player_data_wprojections, columns=features_wprojections)
        df_wprojections.to_excel(writer, sheet_name="Year{}".format(season))




        # Do the regression on this data

    regression_yearbyyear_file = open(path_Data + 'regression_yearbyyear_GP{}_MPG{}.json'.format(GP_boundary, MPG_boundary), 'w')
    regression_json = json.dumps(regression_yearbyyear)
    regression_yearbyyear_file.write(regression_json)
    regression_yearbyyear_file.close()
