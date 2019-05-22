import json

with open('C:\\Users\\jakedaly\\PycharmProjects\\NBA\\src\\Data\\CommonPlayerInfo\\ALL_PLAYERS_CPI.json') as json_file:
    data = json.load(json_file)
    print(data['resource'])
