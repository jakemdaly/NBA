from nba_api.stats.endpoints import *
from nba_api.stats.static import players
from nba_api_helpers import try_request

try:
    active_players = players.get_active_players()

    for player in active_players:

        if player['full_name'] == 'Stephen Curry':

            while True:
                dummy = try_request(commonplayerinfo.CommonPlayerInfo(player['id']))
                print('eggs')
except:
    print('got it')