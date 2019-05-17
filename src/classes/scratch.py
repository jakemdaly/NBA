from nba_api.stats.endpoints import *
from nba_api.stats.library import data
from nba_api.stats.library import parameters
from nba_api.stats.static import players
from FRules import *
from FPointsCalc import *
import csv
from pandas import *
import time

# create a list of active players
act_plyr = players.get_active_players()

rules = FRules

fpoints_1819 = {}
fpoints_1718 = {}
fpoints_diff = {}

with open('fpoints_analysis.csv', 'w', newline='') as csvfile:
    wrtr = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    wrtr.writerow(['player', 'fpoints average'])

    # for each active player, get their season totals for last season
    for plyr_dict in act_plyr:

        # compute how many fantasy points this player had per game for the current season



        # compute how many fantasy points this player had per game for the season before - for rookies write none

        # compute the difference to see who had the largest improvements in fantasy points


        if plyr_dict["full_name"] == "Trae Young":

            # t1 = time.time()
            # cmmn_info = commonplayerinfo.CommonPlayerInfo(plyr_dict['id'])
            # cmmn_info_dict = cmmn_info.get_normalized_dict()
            # available_seasons = cmmn_info_dict['AvailableSeasons']
            # print(available_seasons)
            # time.sleep(.1)
            # t2 = time.time()
            # print("time for one: {}".format(t2-t1))

            plyr_dash_adv = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr_dict['id'], 'measure_type_detailed': parameters.MeasureTypeDetailed.advanced, 'season': '2018-19','per_mode_detailed': parameters.PerModeDetailed.per_game})
            plyr_dash_adv_df = plyr_dash_adv.get_data_frames()
            plyr_dash_adv_dict = plyr_dash_adv.get_normalized_dict()
            plyr_dash_bas = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr_dict['id'], 'season': '2018-19','per_mode_detailed': parameters.PerModeDetailed.per_game})
            plyr_dash_bas_df = plyr_dash_bas.get_data_frames()
            plyr_dash_bas_dict = plyr_dash_bas.get_normalized_dict()
            com_info = commonplayerinfo.CommonPlayerInfo(plyr_dict['id'])
            com_info_df = com_info.get_data_frames()
            com_info_dict = com_info.get_normalized_dict()

            print(com_info_dict['CommonPlayerInfo'][0]['SEASON_EXP'])

            # with ExcelWriter("LNGB_LNGA_CommInfo.xlsx") as writer:
            #     for i in range(0, 1):
            #         df = DataFrame(plyr_dash_bas_df[i])
            #         df.to_excel(writer, sheet_name="LastNGamesBas {}".format(i+1))
            #     for i in range(0, 1):
            #         df = DataFrame(plyr_dash_adv_df[i])
            #         df.to_excel(writer, sheet_name="LastNGamesAdv {}".format(i+1))
            #     for i in range(0, len(com_info_df)):
            #         df = DataFrame(com_info_df[i])
            #         df.to_excel(writer, sheet_name="CommonInfo {}".format(i+1))
