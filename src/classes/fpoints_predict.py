from nba_api.stats.endpoints import *
from nba_api.stats.library import data
from nba_api.stats.library import parameters
from nba_api.stats.static import players
from FRules import *
from FPointsCalc import *
import csv
import time
from FPointsCalc import *
from FRules import *
import pandas as pd
from nba_api_helpers import get_age

# PART 1: Gather data for the current players who were active this season and last season

# create a list of active players
act_plyr = players.get_active_players()

this_season = '2018-19'
last_season = '2017-18'

PLAYERS = []
data = []

# for plyr_dict in act_plyr:
#     if plyr_dict['full_name']=='Alan Williams':
#
#
#         common_player_info = commonplayerinfo.CommonPlayerInfo(plyr_dict['id']).get_normalized_dict()
#
#         if common_player_info['CommonPlayerInfo'][0]['SEASON_EXP'] > 0:
#
#             overall_player_dash = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr_dict['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced, 'season': this_season, 'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()
#
#             if len(overall_player_dash['OverallPlayerDashboard']) == 1:
#                 games_played = overall_player_dash['OverallPlayerDashboard'][0]['GP']
#                 minutes_per_game = overall_player_dash['OverallPlayerDashboard'][0]['MIN']
#
#                 if (games_played > 0 and minutes_per_game > 0):
#
#                     package = [plyr_dict, overall_player_dash, common_player_info]
#
#                     PLAYERS.append(package)
#
#         print(plyr_dict['full_name'])
#         time.sleep(.2)

count = 0

# Loop through the active players. If they are not a rookie and played more than 30 games @ 5 MPG, add them to a separate list
for plyr_dict in act_plyr:

    print('Part 1... Percent Complete: [{}]'.format(100*count/len(act_plyr)))

    # Import that the data that will allow us to look at how many seasons of experience the player has
    common_player_info = commonplayerinfo.CommonPlayerInfo(plyr_dict['id']).get_normalized_dict()

    # Filter out the rookies because they don't have data from the previous season
    if common_player_info['CommonPlayerInfo'][0]['SEASON_EXP'] > 0:

        overall_player_dash = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr_dict['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced, 'season': this_season, 'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()

        # Some players who never played a game don't have anything under their dashboard... so skip these
        if len(overall_player_dash['OverallPlayerDashboard']) == 1:
            games_played = overall_player_dash['OverallPlayerDashboard'][0]['GP']
            minutes_per_game = overall_player_dash['OverallPlayerDashboard'][0]['MIN']

            # Excluded players that didn't play a lot of games/minutes
            if (games_played > 30 and minutes_per_game > 5):

                # Because we will use the data imported by the two calls above, we will pack this data up so that we can use it later in the program
                package = [plyr_dict, overall_player_dash, common_player_info]

                PLAYERS.append(package)

    # print(plyr_dict['full_name'])
    time.sleep(.2)
    count = count + 1


# Create an FRules object
rules = FRules

# Calculate each players fantasy points production for both seasons
len_PLAYERS = len(PLAYERS)
count = 0

# Loop through the players we just specified above
for package in PLAYERS:

    print('Part 2... Percent Complete: [{}]'.format(100*count/len_PLAYERS))

    # Get the data required for x and y variables
    plyr_dsh_lstNgms_last_season_norm_dict = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': package[0]['id'], 'season': last_season, 'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()
    plyr_dsh_lstNgms_this_season_norm_dict = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': package[0]['id'], 'season': this_season, 'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()
    plyr_dsh_lstNgms_last_season_ADV_norm_dict = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': package[0]['id'], 'season': last_season, 'per_mode_detailed': parameters.PerModeDetailed.per_game, 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced}).get_normalized_dict()
    plyr_dsh_lstNgms_this_season_ADV_norm_dict = package[1]
    plyr_cmmn_info_norm_dict = package[2]
    time.sleep(.25) # limit rate that we're grabbing data in loop

    # Get fantasy production for this player for this season
    points_this_season = calc_fpoints_from_season(package[0]['id'], rules, this_season, plyr_dsh_lstNgms_this_season_norm_dict)

    # Get fantasy production for this player for last season
    points_last_season = calc_fpoints_from_season(package[0]['id'], rules, last_season, plyr_dsh_lstNgms_last_season_norm_dict)

    # Compute how much they improved or declined
    improvement = points_this_season - points_last_season

    # Get minutes per game
    if len(plyr_dsh_lstNgms_last_season_norm_dict['OverallPlayerDashboard']) == 1:
        minutes_per_game = plyr_dsh_lstNgms_last_season_norm_dict['OverallPlayerDashboard'][0]['MIN']
    else:
        minutes_per_game = -100

    # Get draft number
    if len(plyr_cmmn_info_norm_dict['CommonPlayerInfo']) == 1:
        draft_pick_number = plyr_cmmn_info_norm_dict['CommonPlayerInfo'][0]['DRAFT_NUMBER']
        if draft_pick_number == 'Undrafted':
            draft_pick_number = 61
        else:
            draft_pick_number = int(draft_pick_number)
    else:
        draft_pick_number = -100

    # Get seasons of experience
    if len(plyr_cmmn_info_norm_dict['CommonPlayerInfo']) == 1:
        seasons_in_league = plyr_cmmn_info_norm_dict['CommonPlayerInfo'][0]['SEASON_EXP']
    else:
        seasons_in_league = -100

    # Get age
    if len(plyr_cmmn_info_norm_dict['CommonPlayerInfo']) == 1:
        age = get_age(plyr_cmmn_info_norm_dict['CommonPlayerInfo'][0]['BIRTHDATE'])
    else:
        age = -100

    # Get efficiency
    if len(plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard']) == 1:
        PIE = plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard'][0]['PIE']
    else:
        PIE = -100


    # Get USG %
    if len(plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard']) == 1:
        USG = plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard'][0]['USG_PCT']
    else:
        USG = -100

    # Get TS %
    if len(plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard']) == 1:
        TS = plyr_dsh_lstNgms_last_season_ADV_norm_dict['OverallPlayerDashboard'][0]['TS_PCT']
    else:
        TS = -100

    #Add all of this information to data
    data.append([package[0]['full_name'], points_this_season, points_last_season, improvement, minutes_per_game, draft_pick_number, seasons_in_league, age, PIE, USG, TS])

    count = count + 1


df = pd.DataFrame(data, columns=['Player', 'FPoints {}'.format(this_season), 'FPoints {}'.format(last_season), 'Improvement', 'MPG', 'Draft Pick Number', '# Seasons in League', 'Age', 'PIE', 'USG', 'TS'])


with pd.ExcelWriter(r"C:\Users\jakedaly\PycharmProjects\NBA\src\classes\data\player_data.xlsx") as writer:
    df.to_excel(writer, sheet_name="Sheet1")