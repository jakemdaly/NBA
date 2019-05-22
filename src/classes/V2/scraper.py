from nba_api.stats.static import players
from nba_api.stats.endpoints import *
from nba_api.stats.library import parameters
import datetime as dt
import json
import time
import sys
import os

earliest_year = 2015  # earliest year that we would like to start gathering data from
datetime_now = dt.datetime.now()
current_year = datetime_now.year
data_path = 'C:\\Users\\jakedaly\\PycharmProjects\\NBA\\src\\Data\\'
common_info_data_path = 'C:\\Users\\jakedaly\\PycharmProjects\\NBA\\src\\Data\\CommonPlayerInfo\\'
dash_by_season_data_path = 'C:\\Users\\jakedaly\\PycharmProjects\\NBA\\src\\Data\\PlayerDashboard\\BySeason\\'

# Get a list of all players that were drafted since the 97-98 season.
all_players = players.get_active_players()
file = open("myfile.txt", 'w')
file.write('{}'.format(all_players))
Players = []
plyr_dict_for_json = []

try:
    # For each player in this list, get the common player info and store this
    for plyr in all_players:

        # if plyr['full_name'] == 'Alan Williams' or plyr['full_name'] == 'Stephen Curry':
        #
        #     common_info = commonplayerinfo.CommonPlayerInfo(plyr['id'])
        #     common_info_dict = common_info.get_normalized_dict()['CommonPlayerInfo'][0]
        #     print(type(common_info_dict['DRAFT_YEAR']))

        common_info = commonplayerinfo.CommonPlayerInfo(plyr['id'])
        time.sleep(.3)
        common_info_dict = common_info.get_normalized_dict()['CommonPlayerInfo'][0]
        from_year = common_info_dict['FROM_YEAR']
        if from_year==None:
            print(plyr['full_name'])
            from_year = -200  # From year == none
        if (int(from_year) >= earliest_year):

            # Save the common player info for this plyr to a json file
            common_info_json = common_info.get_normalized_json()
            common_info_file = open(common_info_data_path + '{}_cpi.json'.format(plyr['full_name']), 'w')
            common_info_file.write(common_info_json)
            common_info_file.close()

            # Save the player's info to the array which will later be converted to json
            plyr_dict_for_json.append({'full_name': '{}'.format(plyr['full_name']), 'id': plyr['id']})

            # Append this player and the common info to the Players array
            Players.append(plyr)

    # Create the json file which will allow us to find which players came into the league since earliest_year
    all_players_cpi_json = json.dumps(plyr_dict_for_json)  # Convert the player dict to a json object
    all_players_cpi_file = open(data_path + 'ALL_PLAYERS_SINCE_{}_CPI.json'.format(earliest_year), 'w')  # Open a file to write it to
    all_players_cpi_file.write(all_players_cpi_json)  # Write the info to the json file
    all_players_cpi_file.close()  # Close the file


    # For each player in this filtered list, loop through each season and pull the basic and advanced stats from the endpoint
    for plyr in Players:

        # Figure out how many seasons we will check if there is data for
        open_json = json.load(open(common_info_data_path + '{}_cpi.json'.format(plyr['full_name'])))
        to_year = int(open_json['CommonPlayerInfo'][0]['TO_YEAR'])
        from_year = int(open_json['CommonPlayerInfo'][0]['FROM_YEAR'])

        # Reset the number of seasons that this player has been in league
        seasons_in_league = 0

        for season in range(from_year, to_year+1):

            #format season
            season_str = '{}-{}'.format(from_year, (from_year-1999))

            # Make sure to detect in the case that there's no data for this player for a season, don't record this
            dash_bas = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.base, 'season': season_str, 'per_mode_detailed': parameters.PerModeDetailed.per_game})
            time.sleep(.3)
            # Only do the following data storage if the player had a dashboard of data for this season
            if (len(dash_bas.get_normalized_dict()['OverallPlayerDashboard']) == 0):
                # Do Nothing
            elif:
                # Add one to the number of seasons the player has been in the league
                seasons_in_league = seasons_in_league + 1
                by_season_str = "Year{}\\".format(seasons_in_league)

                # Make a query for the player's advanced stats for this season
                dash_adv = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced, 'season': season_str, 'per_mode_detailed': parameters.PerModeDetailed.per_game})
                time.sleep(.3)
                # Get the json of each
                dash_bas_dict = dash_bas.get_normalized_dict()
                dash_adv_dict = dash_adv.get_normalized_dict()
                dash_both_dict = {'DashBasic': dash_bas_dict['OverallPlayerDashboard'], 'DashAdvanced': dash_adv_dict['OverallPlayerDashboard']}
                dash_both_json = json.dumps(dash_both_dict)

                # Store each of these into the stats file for this player
                plyr_stats_json = open(dash_by_season_data_path + by_season_str + '{}_1{}_dash.json'.format(plyr['full_name'], season), 'w')
                plyr_stats_json.write(dash_both_json)
                plyr_stats_json.close()

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    input()

