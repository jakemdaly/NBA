import sys
from nba_api.stats.library import parameters
from nba_api.stats.endpoints import *

def calc_fpoints_from_game(playerID, rules, game):

    # this is what will get returned at the end
    fpoints = 0


    # FGM =

    # Get the player's stats for each of the rules in FRules

    for rule in rules:
        if rule == 'FGM':
            # fpoints = fpoints + rules.
            pass
        elif rule == 'FGA':
            pass
        elif rule == 'FTM':
            pass
        elif rule == 'FTA':
            pass
        elif rule == 'REB':
            pass
        elif rule == 'AST':
            pass
        elif rule == 'STL':
            pass
        elif rule == 'BLK':
            pass
        elif rule == 'TO':
            pass
        elif rule == 'EJ':
            pass
        elif rule == 'TD':
            pass
        elif rule == 'PTS':
            pass

    return fpoints

def calc_fpoints_from_season(playerID, rules, season, plyr_dsh_lstNgms_norm_dict = None):

    # this is what will get returned at the end
    fpoints = 0.0
    if (plyr_dsh_lstNgms_norm_dict != None):
        plyr_dshbrd_lst_n_gms = plyr_dsh_lstNgms_norm_dict
    else:
        plyr_dshbrd_lst_n_gms = playerdashboardbylastngames.PlayerDashboardByLastNGames(**{'player_id': playerID, 'season': season,'per_mode_detailed': parameters.PerModeDetailed.per_game}).get_normalized_dict()

    len_plyr_dshbrd_lst_n_gms = len(plyr_dshbrd_lst_n_gms['OverallPlayerDashboard'])
    if len_plyr_dshbrd_lst_n_gms != 1:
        print("length: {}, player {}".format(len_plyr_dshbrd_lst_n_gms, playerID))
        return 0
    overall_player_dashboard = plyr_dshbrd_lst_n_gms['OverallPlayerDashboard'][0]

    # Get the player's stats for each of the rules in FRules

    for rule in [a for a in dir(rules) if not a.startswith('__') and not callable(getattr(rules, a))]:
        if rule == 'FGM':
            plyr_fpoints_FGM = rules.FGM*overall_player_dashboard['FGM']
            fpoints += plyr_fpoints_FGM

        elif rule == 'FGA':
            plyr_fpoints_FGA = rules.FGA * overall_player_dashboard['FGA']
            fpoints += plyr_fpoints_FGA

        elif rule == 'FTM':
            plyr_fpoints_FTM = rules.FTM * overall_player_dashboard['FTM']
            fpoints += plyr_fpoints_FTM

        elif rule == 'FTA':
            plyr_fpoints_FTA = rules.FTA * overall_player_dashboard['FTA']
            fpoints += plyr_fpoints_FTA

        elif rule == 'REB':
            plyr_fpoints_REB = rules.REB * overall_player_dashboard['REB']
            fpoints += plyr_fpoints_REB

        elif rule == 'AST':
            plyr_fpoints_AST = rules.AST * overall_player_dashboard['AST']
            fpoints += plyr_fpoints_AST

        elif rule == 'STL':
            plyr_fpoints_STL = rules.STL * overall_player_dashboard['STL']
            fpoints += plyr_fpoints_STL

        elif rule == 'BLK':
            plyr_fpoints_BLK = rules.BLK * overall_player_dashboard['BLK']
            fpoints += plyr_fpoints_BLK

        elif rule == 'TOV':
            plyr_fpoints_TOV = rules.TOV * overall_player_dashboard['TOV']
            fpoints += plyr_fpoints_TOV

        elif rule == 'EJ':
            pass

        elif rule == 'TD':
            pass

        elif rule == 'PTS':
            plyr_fpoints_PTS = rules.PTS * overall_player_dashboard['PTS']
            fpoints += plyr_fpoints_PTS

    return fpoints