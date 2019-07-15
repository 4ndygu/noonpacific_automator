from publisher import Publisher

from datetime import date

import base64
import bs4
import logging
import os
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

class MailchimpPublisher(Publisher):

    def __init__(self, metadata, token, audience_id):
      super(MailchimpPublisher, self).__init__(metadata)

      zone = token.split('-')[-1]

      self.template_location = '/etc/secrets/mailchimp.html'
      self.endpoint_template = 'https://{}.api.mailchimp.com/3.0/templates'.format(zone)
      self.endpoint_campaign = 'https://{}.api.mailchimp.com/3.0/campaigns'.format(zone)
      self.token = token
      self.payload = {}
      self.audience_id = audience_id
      self.template_id = ""

      self.title = ""
      self.soup = None

      # Load basic auth header
      auth_header = base64.b64encode('meaningless:{}'.format(token)) 
      self.headers = {'Authorization': 'Basic {}'.format(auth_header)}

      # Check if template exits
      if os.path.isfile(self.template_location):
        with open(self.template_location) as input_file:
          self.soup = bs4.BeautifulSoup(input_file, features='lxml')
      else:
        logger.error("No mailchimp template file")
        sys.exit()

      if not self.soup:
        logger.error("self.soup was not initialized")
        sys.exit()

    def format(self):
      sanitized_metadata = [[item['title'], item['artist']] for item in self.track_metadata['results']]

      self.title = 'NOON // {}'.format(self.mixtape_metadata['id'])

      # Change title
      title_block = self.soup.find(id="automator_title")
      title_block.string = self.title

      # Change image
      image_block = self.soup.find(id="automator_image")
      image_block['src'] = self.mixtape_metadata['artwork_url']

      # Change image credits
      image_credit_block = self.soup.find(id="automator_image_credit")
      image_credit_block.string = self.mixtape_metadata['artwork_credit']

      # Roll thorugh metadata, change songs
      for index,item in enumerate(sanitized_metadata):
        artist_block = self.soup.find(id="automator_artist_{}".format(index+1))
        song_block = self.soup.find(id="automator_song_{}".format(index+1))
        artist_block.string = sanitized_metadata[index][1]
        song_block.string = sanitized_metadata[index][0]

      # Write file to local
      today = date.today().strftime("%d-%m-%Y")
      with open("/var/log/mailchimp_template-{}".format(today), 'w') as f:
        f.write(str(self.soup))

      logger.info('Mailchimp: Sending request to create template')

      # Push template north 
      self.payload["name"] = "NOON {}".format(today)
      self.payload["html"] = str(self.soup)

      response = requests.post(self.endpoint_template, headers=self.headers,
        json=self.payload)

      logger.info('Mailchimp: Response: {}'.format(response.json()))

      if response.status_code != 200:
        logger.error('Mailchimp: Response errored out, see above')
        sys.exit()

      self.template_id = int(response.json()['id'])

    def publish(self):
      # Check if the message has been formatted
      if not self.template_id:
        logger.error('Mailchimp: No template found')
        sys.exit()

      # Generate campaign
      self.payload = {}
      self.payload['type'] = 'regular'
      self.payload['recipients'] = {}
      self.payload['recipients']['list_id'] = str(self.audience_id)
      self.payload['settings'] = {}
      self.payload['settings']['subject_line'] = self.title
      self.payload['settings']['title'] = self.title
      self.payload['settings']['template_id'] = self.template_id

      logger.info('Mailchimp: Creating Campaign')

      response = requests.post(self.endpoint_campaign, headers=self.headers,
        json=self.payload)

      logger.info('Mailchimp: Response: {}'.format(response.json()))

      if response.status_code != 200:
        logger.error('Mailchimp: Response errored out, see above')
        sys.exit()
