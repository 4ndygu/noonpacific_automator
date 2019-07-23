from publisher import Publisher

import logging
import requests
import sys

# set up logging to file
logging.basicConfig(
     stream=sys.stdout,
     level=logging.INFO,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

class BufferPublisher(Publisher):

    def __init__(self, metadata, token, twitter=False):
      super(BufferPublisher, self).__init__(metadata)

      self.endpoint = 'https://api.bufferapp.com/1/updates/create.json'
      self.profiles_endpoint = 'https://api.bufferapp.com/1/profiles.json'
      self.token = token
      self.payload = {}

      # Get profiles for Buffer
      params = {'access_token': self.token}

      resp = requests.get(self.profiles_endpoint, params=params).json()

      self.profiles = [item['id'] for item in resp 
        if item['formatted_service'] != 'Twitter' and item['disabled'] == False
        and item['disconnected'] == False and item['locked'] == False
        and item['paused'] == False]
      self.twitter_profile = [item['id'] for item in resp 
        if item['formatted_service'] == 'Twitter' and item['disabled'] == False
        and item['disconnected'] == False and item['locked'] == False
        and item['paused'] == False]

    def format(self):
      sanitized_metadata = [[item['artist'], item['title']] for item in self.track_metadata['results']]
      tracklist = '\n '.join(['{} {} - {}'.format(index+1, item[0].encode('utf-8'), item[1].encode('utf-8')) for index, item in enumerate(sanitized_metadata)])

      self.payload['text'] = '\n{} \n 📷 {} \n {}'.format(self.mixtape_metadata['title'], 
        self.mixtape_metadata['artwork_credit'], 
        tracklist)

      self.payload['media[photo]'] = self.mixtape_metadata['artwork_url']
      self.payload['profile_ids'] = self.profiles

    def format_twitter(self):
      self.payload['text'] = '{} Now Streaming'.format(self.mixtape_metadata['title'])
      self.payload['media[photo]'] = self.mixtape_metadata['artwork_url']
      self.payload['profile_ids'] = self.twitter_profile

    def publish(self):
      # Check if the message has been formatted
      if not self.payload:
          logger.error('Publish called before format! No payload to send.')
          sys.exit()

      params = {'access_token': self.token}
      headers = {'Accept': 'application/json'}

      logger.info('Sending the following payload: {}'.format(self.payload))

      response = requests.post(self.endpoint, headers=headers,
        data=self.payload, params=params)

      logger.info('Response: {}'.format(response.json()))
      
      # error handling for the request
      if response.status_code == 200:
        if response.json()['success'] != 'true':
          logger.error('Failed to deploy publication')
      else:
        logger.error('Failed to deploy publication')
