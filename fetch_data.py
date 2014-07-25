import gzip
import json
import os.path
import urllib2
from StringIO import StringIO
from time import sleep

BASE_DIR = 'data/'
BASE_URL = 'https://erikberg.com/'
API_KEY = '56b0e173-170f-4dcb-983f-111b642e2def'
USER_AGENT = 'fdbot/0.1 (jack@fanduel.com)'


def get_data(url):
    req = urllib2.Request(url)
    req.add_header("Authorization", "Bearer " + API_KEY)
    req.add_header("User-agent", USER_AGENT)
    req.add_header("Accept-encoding", "gzip")

    data = None
    response = urllib2.urlopen(req)
    sleep(10)
    if "gzip" == response.info().get("Content-encoding"):
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data_json = f.read()
    else:
        data_json = response.read()

    return json.loads(data_json)


def save_data(data, file_dir):
    """Save python data as JSON file"""
    with open(file_dir, 'w') as f:
        json.dump(data, f)


def load_data(file_dir):
    """Load JSON data into python"""
    with open(file_dir, 'r') as f:
        return json.load(f)


def get_teams(sport):
    file_dir = '{base}{sport}/teams.json'.format(
        base=BASE_DIR,
        sport=sport,
    )

    if os.path.isfile(file_dir):
        return load_data(file_dir)
    else:
        url = '{base}{sport}/teams.json'.format(
            base=BASE_URL,
            sport=sport,
            )

        data = get_data(url)
        save_data(data, file_dir)
        return data


def get_team_schedule(sport, team_id):
    file_dir = '{base}{sport}/results/{team_id}.json'.format(
        base=BASE_DIR,
        sport=sport,
        team_id=team_id,
    )

    if os.path.isfile(file_dir):
        return load_data(file_dir)
    else:
        url = '{base}{sport}/results/{team_id}.json?season=2014'.format(
            base=BASE_URL,
            sport=sport,
            team_id=team_id,
            )

        data = get_data(url)
        save_data(data, file_dir)
        return data


def get_box_score(sport, event_id):
    file_dir = '{base}{sport}/boxscore/{event_id}.json'.format(
        base=BASE_DIR,
        sport=sport,
        event_id=event_id,
    )

    if os.path.isfile(file_dir):
        return load_data(file_dir)
    else:
        url = '{base}{sport}/boxscore/{event_id}.json'.format(
            base=BASE_URL,
            sport=sport,
            event_id=event_id,
            )

        data = get_data(url)
        save_data(data, file_dir)
        return data


def get_all_box_scores(sport):
    teams = get_teams(sport)
    print 'teams fetched'

    box_scores = []
    for team in teams:
        team_id = team['team_id']
        schedule = get_team_schedule(sport, team_id)
        print '{} schedule fetched'.format(team_id)

        for event in schedule:
            event_id = event['event_id']
            event_status = event['event_status']
            season_type = event['event_season_type']

            if (event_status == 'completed' and
                    season_type == 'regular' or
                    season_type == 'post'):
                box_score = get_box_score(sport, event_id)
                print '{} box score fetched'.format(event_id)

                box_scores.append(box_score)

    file_dir = '{base}{sport}/boxscores.json'.format(
        base=BASE_DIR,
        sport=sport,
    )
    save_data(box_scores, file_dir)
    print 'completed'
    return box_scores

""" Next compile information on all players """
