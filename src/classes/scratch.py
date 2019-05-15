from nba_api.stats.endpoints import *
from nba_api.stats.library import data
from nba_api.stats.library import parameters
from nba_api.stats.static import players
from FRules import *
from FPointsCalc import *
import csv

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


        if plyr_dict["full_name"] == "Stephen Curry":
            # overall_player_dash = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': plyr_dict['id'], 'season': '2018-19','per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()
            overall_player_dash = playerdashboardbylastngames.PlayerDashboardByLastNGames(plyr_dict['id'])

            print(overall_player_dash.overall_player_dashboard.get_dict())
            # # Get how many seasons of experience the player has, how many minutes per game they had, and how many games they played
            # szns_exp = commonplayerinfo.CommonPlayerInfo(plyr_dict['id']).get_normalized_dict()['CommonPlayerInfo'][0][
            #     'SEASON_EXP']
            # games_played = playerdashboardbylastngames.PlayerDashboardByLastNGames(
            #     **{'player_id': plyr_dict['id'], 'season': '2018-19',
            #        'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()[
            #     'OverallPlayerDashboard'][0]['GP']
            # minutes_per_game = playerdashboardbylastngames.PlayerDashboardByLastNGames(
            #     **{'player_id': plyr_dict['id'], 'season': '2018-19',
            #        'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()[
            #     'OverallPlayerDashboard'][0]['MIN']
            #
            # # compute how many fantasy points this player had per game for last season
            # fpoints_1718_val = calc_fpoints_from_season(plyr_dict['id'], rules, '2017-18')
            # dict_1718 = {plyr_dict['full_name']: fpoints_1718_val}
            # fpoints_1718.update(dict_1718)
            #
            # # compute how many fantasy points they had for this season
            # fpoints_1819_val = calc_fpoints_from_season(plyr_dict['id'], rules, '2018-19')
            # dict_1819 = {plyr_dict['full_name']: fpoints_1819_val}
            # fpoints_1819.update((dict_1819))
            #
            # # compute the difference
            # diff_1718_1819 = fpoints_1819_val - fpoints_1718_val
            # dict_val_diff = {plyr_dict['full_name']: diff_1718_1819}
            # fpoints_diff.update(dict_val_diff)
            #
            # total_fpoints_scored = games_played * fpoints_1819_val
            #
            # wrtr.writerow(
            #     [plyr_dict['full_name'], fpoints_1819_val, diff_1718_1819, szns_exp, games_played, minutes_per_game,
            #      total_fpoints_scored])

