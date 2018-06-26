import urllib.request, json 
from urllib.request import Request
import _thread
from time import sleep
from random import randint
from os import listdir
from os.path import isfile, join


# Takes player id and saves the JSON market data as player_id.json
def save_markets(player_id):
    print('https://www.futbin.com/18/playerGraph?type=daily_graph&year=18&player=' + str(player_id))
    try:
        with urllib.request.urlopen(Request('https://www.futbin.com/18/playerGraph?type=daily_graph&year=18&player=' + str(player_id), headers={'User-Agent': 'Mozilla/5.0'})) as url:
            data = json.loads(url.read().decode())
            with open('./markets/' + player_id + '.json', 'w') as outfile:
                json.dump(data, outfile)
    except:
        print("Error - Might be accidentally DDOSing!")
        

players_path = './players'
player_ids = [f for f in listdir(players_path) if isfile(join(players_path, f))]
player_ids = list(map(lambda x: x.split('.')[0], player_ids))


for player_id in player_ids:
    save_markets(player_id)
    sleep(0.25)