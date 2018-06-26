import urllib.request, json 
import _thread
from time import sleep
from random import randint

def save_players(page):
	sleep(randint(0,100))
	with urllib.request.urlopen('https://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject=%7B%22page%22:' + str(page) + ',%22position%22:%22LF,CF,RF,ST,LW,LM,CAM,CDM,CM,RM,RW,LWB,LB,CB,RB,RWB%22%7D') as url:
	    data = json.loads(url.read().decode())
	    for player in data['items']:
	    	print(player['name'])
	    	with open('./players/' + player['id'] + '.json', 'w') as outfile:
			    json.dump(player, outfile)


pages = list(range(1,751))

for page in pages:
	_thread.start_new_thread( save_players, (page,) )  

while 1:
   pass