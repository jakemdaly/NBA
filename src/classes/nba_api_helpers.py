from nba_api.stats.endpoints import *
from abc import ABC, abstractmethod

def player_season_stats_basic(playerID, season):

    player_stats_basic = PlayerStatsBasic(playerID)

    return player_stats_basic


class PlayerStats(ABC):

    player_name = None
    player_id = None
    age = None

    @abstractmethod
    def __init__(self, playerID):
        self.player_id = playerID
        complyrinfo = commonplayerinfo.CommonPlayerInfo(playerID)
        self.player_name = complyrinfo[results]

        pass

class PlayerStatsBasic(PlayerStats):

    game_id = None
    game_date = None
    matchup = None
    WL = None
    min = None
    FGM = None
    FGA = None
    FG_PCT = None
    FG2M = None
    FG2A = None
    FG2_PCT = None
    FG3M = None
    FG3A = None
    FG3_PCT = None
    FTM = None
    FTA = None
    FT_PCT = None
    OREB = None
    DREB = None
    REB = None
    AST = None
    STL = None
    BLK = None
    TOV = None
    PF = None
    PTS = None
    plus_minus = None

    def __init__(self, playerID):
        super().__init__(playerID)

