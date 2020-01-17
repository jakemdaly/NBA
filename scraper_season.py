from nba_api.stats.static import players
from nba_api.stats.endpoints import *
from nba_api.stats.library import parameters
from nba_api_helpers import get_season_str_YY
import datetime as dt
import json
import time
import traceback

try:
    print("Continue previous session? Y/N\n")
    cont_prev_sess = input()
    if cont_prev_sess == 'Y' or cont_prev_sess == 'y':
        continuing_scraping_sess = True
        print("MAKE SURE FILES ARE EDITED & PREPARED...THEN PRESS ENTER\n")
        input()
    else:
        continuing_scraping_sess = False

    earliest_year = 1997  # earliest year that we would like to start gathering data from
    datetime_now = dt.datetime.now()
    current_year = datetime_now.year
    data_path = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\'
    common_info_data_path = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\CommonPlayerInfo\\'
    CPI_header_path = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\'
    dash_by_season_data_path = 'C:\\Users\\jaked\\PycharmProjects\\NBA\\src\\Data_season_totals\\PlayerDashboard\\BySeason\\'
    all_players_cpi_array = []
    total_players = players.get_players()
    number_through_total_players = 0

    if not continuing_scraping_sess:
        # Create log file to write to
        log = open(data_path + 'log.txt', 'w+')
        all_players_cpi_file = open(data_path + 'ALL_PLAYERS_SINCE_{}_CPI.json'.format(earliest_year), 'w+')  # Open a file to write it to

        # Get a list of all players that were drafted since the 97-98 season.
        Players = total_players

        players_from_previous_run = []

    else:
        # Determine which players have already been done from total_players
        players_from_previous_run = json.load(open(CPI_header_path + 'ALL_PLAYERS_SINCE_{}_CPI.json'.format(earliest_year)))
        num_players_from_previous_run = len(players_from_previous_run)
        last_successful_player_write = players_from_previous_run[num_players_from_previous_run-1]['ID']

        for iter in range(0,len(total_players)):
            if total_players[iter]['id'] == last_successful_player_write:
                Players = total_players[iter+1:]
                number_through_total_players = iter

        # Open the CPI file to continue writing to
        all_players_cpi_file = open(CPI_header_path + 'ALL_PLAYERS_SINCE_{}_CPI.json'.format(earliest_year), 'w+')
        log = open(data_path + 'log.txt', 'a+')


    # For each player in this list, get the common player info and store this
    # players_for_cpi = []
    total_number_players = len(Players)
    number_finished_this_run = 0

    log.write("Begin the loop\n")

    for plyr in Players:

        # See how far along we are...
        percent_done = 100 * (number_finished_this_run + number_through_total_players) / total_number_players
        print("Part 1 percent done: {}".format(percent_done))

        # if plyr['full_name'] == 'Alan Williams' or plyr['full_name'] == 'Stephen Curry':

        common_info = commonplayerinfo.CommonPlayerInfo(plyr['id'])
        time.sleep(0.4)

        common_info_dict = common_info.get_normalized_dict()['CommonPlayerInfo'][0]
        from_year = common_info_dict['FROM_YEAR']

        if from_year==None:
            log.write('{} had no FROM_YEAR in CommonPlayerInfo. Not added to CPI log, not added to Players list\n'.format(plyr['full_name']))

            from_year = -200  # From year == none

        if (int(from_year) >= earliest_year):

            # This player is a valid player. We haven't gotten any of his data yet however, so all flags --> False
            cpi_dict = {'FullName': plyr['full_name']}


            # Save the common player info for this plyr to a json file
            common_info_json = common_info.get_normalized_json()
            common_info_file = open(common_info_data_path + '{}_{}_cpi.json'.format(plyr['last_name'],plyr['first_name']), 'w')
            common_info_file.write(common_info_json)
            common_info_file.close()

            cpi_dict = {'FullName': plyr['full_name']}

            # Figure out how many seasons we will check if there is data for
            to_year = int(common_info_dict['TO_YEAR'])
            seasons_to_compute = to_year-from_year+1

            # Reset the number of seasons that this player has been in league
            seasons_in_league = 0
            for season in range(from_year, to_year + 1):

                # format season
                season_first_half = season
                season_second_half = get_season_str_YY(season + 1)
                season_str = '{}-{}'.format(season_first_half, season_second_half)

                # Make sure to detect in the case that there's no data for this player for a season, don't record this
                dash_bas = playerdashboardbylastngames.PlayerDashboardByLastNGames(
                    **{'player_id': plyr['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.base,
                       'season': season_str, 'per_mode_detailed': parameters.PerModeDetailed.totals})
                time.sleep(0.4)
                # Make a query for the player's advanced stats for this season
                dash_adv = playerdashboardbylastngames.PlayerDashboardByLastNGames(
                    **{'player_id': plyr['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced,
                       'season': season_str, 'per_mode_detailed': parameters.PerModeDetailed.totals})
                time.sleep(0.4)

                # Only do the following data storage if the player had a dashboard of data for this season
                if (len(dash_bas.get_normalized_dict()['OverallPlayerDashboard']) == 0) and (len(dash_adv.get_normalized_dict()['OverallPlayerDashboard']) == 0):
                    log.write(
                        "{} had a len(OverallPlayerDashboard) = 0 for year {}\n".format(plyr['full_name'], season_str))

                else:
                    # Add one to the number of seasons the player has been in the league
                    seasons_in_league = seasons_in_league + 1
                    by_season_str = "Year{}\\".format(seasons_in_league)

                    # Get the json of each
                    dash_bas_dict = dash_bas.get_normalized_dict()
                    dash_adv_dict = dash_adv.get_normalized_dict()
                    dash_both_dict = {'DashBasic': dash_bas_dict['OverallPlayerDashboard'],
                                      'DashAdvanced': dash_adv_dict['OverallPlayerDashboard']}
                    dash_both_json = json.dumps(dash_both_dict)

                    # Store each of these into the stats file for this player
                    plyr_stats_json = open(
                        dash_by_season_data_path + by_season_str + '{}_{}_1{}_dash.json'.format(plyr['last_name'], plyr['first_name'], season),
                        'w')
                    plyr_stats_json.write(dash_both_json)
                    plyr_stats_json.close()

                    print("\tCompleted {}/{} seasons for {}\n".format(seasons_in_league, seasons_to_compute, plyr['full_name']))


            cpi_dict = {'FullName': plyr['full_name'], 'ID': plyr['id']}

            all_players_cpi_array.append(cpi_dict)

            # Add this to CPI JSON and log file

            log.write('Added {} seasons of {} to data\n'.format(seasons_in_league, plyr['full_name']))

        number_finished_this_run = number_finished_this_run + 1

except Exception as e:
    all_players_cpi_array = players_from_previous_run + all_players_cpi_array
    player_cpi_json = json.dumps(all_players_cpi_array)  # Convert the player dict to a json object
    all_players_cpi_file.write(player_cpi_json)  # Write the info to the json file
    print(e)
    print(traceback.format_exc())

finally:
    all_players_cpi_file.close()  # Close the file. You will need to add a bracket to close the file for later use

    log.close()