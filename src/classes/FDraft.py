import nba_api
import numpy as np
import enum

class FDraft:

    # People/Teams participating in draft
    draft_participants = []
    order_of_participants = []

    # FRules which will govern the league (ie. what determines how many fantasy points a player scores from his game stats)

    # FDraft player attributes
    players_at_start = [] # Will be equal to players_available + players_drafted
    players_available = []  # Will be equal to players_at_start - players_drafted
    players_drafted = []  # Will be equal to players_start - players_available
    players_available_filtered = []  # Will be the list of players that get's filtered. Should be able to sort this list with sort function
    players_available_sorted = []  # Will be the list of players that get's sorted. Should be able to add a filter to this list
    depth_chart = []  # Depth chart for the team of players that you've drafted

    # Filters (enum)

    # Sorters (enum)

    def add_player_to_draft(self, player):
        #TODO:
        pass
    def sort_players_available(self,  sorter):
        #TODO: Sort the list of players_available into one that's sorted by a certain variable
        pass
    def filter_players_available(self, filter):
        #TODO: add a filter to list of players in player_available_filtered
        pass

