import json
from collections import defaultdict
from uuid import uuid4

with open('data/mlb/boxscores.json', 'r') as f:
    box_scores = json.load(f)

player_stats = defaultdict(list)
player_keys = defaultdict(list)

for box_score in box_scores:
    home_batters = box_score['home_batters']
    for batter in home_batters:
        name = batter['display_name']

        uuid = uuid4()
        key = name.lower().replace(' ', '_')
        u_key = '{}-{}'.format(key.encode('utf-8'), uuid)

        player_stats[u_key].append(batter)
        player_keys[name].append(u_key)
