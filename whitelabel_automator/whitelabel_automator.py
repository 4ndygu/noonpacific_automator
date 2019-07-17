#!/usr/bin/env python3
from datetime import date, datetime

import argparse
import json
import logging
import requests
import sys
import yaml

from publishers.buffer_publisher import BufferPublisher 
from publishers.mailchimp_publisher import MailchimpPublisher 

# set up logging to file
logging.basicConfig(
     stream=sys.stdout,
     level=logging.INFO,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

WHITELABEL_MIXTAPE_ENDPOINT = 'https://beta.whitelabel.cool/api/mixtapes/latest'
WHITELABEL_TRACK_ENDPOINT = 'https://beta.whitelabel.cool/api/tracks'

def pull_track_summaries(mixtape, client_token):
  headers = {'Accept': 'application/json',
             'Client': client_token}
  params = {'mixtape': mixtape}

  response = requests.get(WHITELABEL_TRACK_ENDPOINT, headers=headers, 
    params=params)

  if response.status_code == 200:
    # Check if today's mixtape is right
    response_data = response.json()

    if response_data:
      response_tracks = [item for item in response_data["results"] if item["mixtape"] == mixtape]

      return response_data
    else:
      logger.error("Unable to pull track summaries")
      sys.exit()

def pull_latest_trackdata(client_token):
  headers = {'Accept': 'application/json',
             'Client': client_token}

  response = requests.get(WHITELABEL_MIXTAPE_ENDPOINT, headers=headers)

  if response.status_code == 200:
    # Check if today's mixtape is right
    response_data = response.json()
    
    track_metadata = pull_track_summaries(response_data['id'], client_token)

    result = {}
    result["mixtape"] = response_data
    result["tracks"] = track_metadata

    return result
  else:
    logger.error("Unable to pull track metadata")
    sys.exit()

def load_config():
  try:
    with open('/etc/secrets/config.yaml') as config_file:
      return yaml.safe_load(config_file)
  except Exception as e:
    logger.exception("Fatal error in config load")
    exit()

def main():
  parser = argparse.ArgumentParser()
  args = parser.parse_args()

  CONFIG = load_config()

  # Check what day it is
  day = date.today().weekday()
  if day > 2:
      logger.error("Not running report on day: {}".format(day))
      sys.exit()
  else:
      logger.info("Running report on day: {}".format(day))


  latest_trackdata = pull_latest_trackdata(CONFIG.get('whitelabel'))

  # send track data to endpoints
  if CONFIG.get('buffer'):
    publisher = BufferPublisher(latest_trackdata, CONFIG.get('buffer'), CONFIG.get('buffer_twitter'))

    publisher.format()
    publisher.publish()

    publisher.format_twitter()
    publisher.publish()

  if CONFIG.get('mailchimp'):
    publisher = MailchimpPublisher(latest_trackdata, 
            CONFIG.get('mailchimp'), CONFIG.get('mailchimp_audience'))

    publisher.format()
    publisher.publish()

if __name__ == '__main__':
    main()
