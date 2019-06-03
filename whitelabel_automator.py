#!/usr/bin/env python3
import argparse
import requests
import json

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s [%(levelname)s] (%(processName)-10s) %(message)s',
                    )

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
requests_log.propagate = True

WHITELABEL_MIXTAPE_ENDPOINT = 'https://beta.whitelabel.cool/api/mixtapes/latest'
WHITELABEL_TRACK_ENDPOINT = 'https://beta.whitelabel.cool/api/mixtapes/latest'

def pull_track_summaries(mixtape):
  headers = {'Accept': 'application/json',
             'Client': client_token}
  params = {'mixtape': mixtape}

  response = requests.get(WHITELABEL_TRACK_ENDPOINT, headers=headers
                                                   , params=params)

  if response.status_code == '200':
    # Check if today's mixtape is right
    response_data = response.json()

    if response_data:
      response_tracks = [item for item in response_data["results"] if item["mixtape"] == mixtape]
      return response_data
    else:
      # TODO: fail safely
      pass

def pull_latest_trackdata(client_token):
  headers = {'Accept': 'application/json',
             'Client': client_token}

  response = requests.get(WHITELABEL_MIXTAPE_ENDPOINT, headers=headers)

  if response.status_code == '200':
    # Check if today's mixtape is right
    response_data = response.json()
    
    track_metadata = pull_track_summaries(response_data['id'])

    result = {}
    result["mixtape"] = response_data
    result["tracks"] = track_metadata

    return result
  else:
    # TODO: Raise an error
    pass

def load_config():
  try:
    with open('config.yaml') as config_file:
      return yaml.safe_load(config_file)
  except Exception as e:
      LOG.error(f'Config ERROR: {e}')
      exit()

def main():
  parser = argparse.ArgumentParser()
  args = parser.parse_args()

  CONFIG = load_config()

  latest_trackdata = pull_latest_trackdata(CONFIG.get('whitelabel'))

  # send track data to endpoints

