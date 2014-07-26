import json
from uuid import uuid

with open('data/mlb/box_scores.json', 'r') as f:
	box_scores = json.load(f)

player_stats = []

for box_score in box_scores:
	home_batters = box_score['home_batters']
	for batter in home_batters:
		name = batter['display_name']

		uuid = uuid.4()
		key = name.lower().replace(' ','_')


