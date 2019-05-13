from nba_api.stats.endpoints import *
from nba_api.stats.library import data
from nba_api.stats.static import players
import re

act_plyr = players.get_active_players()

print(playergamelog.PlayerGameLog(201939).get_dict())