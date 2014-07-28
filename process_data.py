import json
from collections import defaultdict
from uuid import uuid4


def all_mlb_player_stats():
    with open('data/mlb/boxscores.json', 'r') as f:
        box_scores = json.load(f)

    all_player_stats = defaultdict(list)

    for box_score in box_scores:
        home_abbr = box_score['home_team']['abbreviation']
        home_batters = box_score['home_batters']
        for player in home_batters:
            name = player['display_name'].replace(' ', '_').encode('utf-8')
            key = '{}_{}'.format(name, home_abbr).lower()

            all_player_stats[key].append(player)

        away_abbr = box_score['away_team']['abbreviation']
        away_batters = box_score['away_batters']
        for player in away_batters:
            name = player['display_name'].replace(' ', '_').encode('utf-8')
            key = '{}_{}'.format(name, away_abbr).lower()

            all_player_stats[key].append(player)

    return all_player_stats


def get_player_stats(player_stats):
    for game in player_stats:
        
    
