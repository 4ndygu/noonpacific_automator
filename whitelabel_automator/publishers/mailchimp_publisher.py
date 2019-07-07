from publisher import Publisher

import logging
import requests
import sys

# set up logging to file
logging.basicConfig(
     filename='/var/log/whitelabel_automator.log',
     level=logging.INFO,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

class MaklchimpPublisher(Publisher):

    def __init__(self, metadata, token, template_id, audience_id):
      super(MailchimpPublisher, self).__init__(metadata)

      zone = token.split('-')[-1]

      self.endpoint = 'https://{}.api.mailchimp.com/3.0/'.format(zone)
      self.token = token
      self.payload = {}
      self.template_id = template_id
      self.audience_id = audience_id

      # Load basic auth header
      var auth_header = base64.b64encode('meaningless:{}'.format(token)) 
      self.headers = {'Authorization': 'Basic {}'.format(auth_header)}

    def format(self):
      sanitized_metadata = [[item['title'], item['artist']] for item in self.track_metadata['results']]
      tracklist = ' '.join(['{} {} - {}'.format(index, item[0].encode('utf-8'), item[1].encode('utf-8')) for index, item in enumerate(sanitized_metadata)])

      self.payload['text'] = 'NOON // {} Photo // {} {}'.format(self.mixtape_metadata['id'], 
        self.mixtape_metadata['artwork_credit'], 
        tracklist)

      self.payload['media[photo]'] = self.mixtape_metadata['artwork_url']
      self.payload['profile_ids'] = self.profiles

    def publish(self):
      # Check if the message has been formatted
      if not self.payload:
          logger.error("Publish called before format! No payload to send.")
          sys.exit()

      # Generate campaign
      # Generate campaign content

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
