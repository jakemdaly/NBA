from nba_api.stats.endpoints import *
from nba_api.stats.library import data
from nba_api.stats.static import players
import re

# create a list of active players
act_plyr = players.get_active_players()
act_plyr_ids = []


# for each active player, get their season totals for last season
for plyr_dict in act_plyr:
    # act_plyr_ids.append(plyr_dict["id"])

    if plyr_dict["full_name"] == "Stephen Curry":
        tmp = commonplayerinfo.CommonPlayerInfo(plyr_dict['id']).get_dict()
        print(tmp['resultSets'][0])
        print()
        print(tmp['resultSets'][1])
        print()
        print(tmp['resultSets'][2])
        print()

        # game_log_dict = playergamelog.PlayerGameLog(plyr_dict["id"]).get_dict()
        #
        # print(game_log_dict['resultSets'][0]['rowSet'])
        # input()