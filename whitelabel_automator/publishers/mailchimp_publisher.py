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
     filename='/var/log/whitelabel_automator.log',
     level=logging.INFO,
     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

class MailchimpPublisher(Publisher):

    def __init__(self, metadata, token, audience_id):
      super(MailchimpPublisher, self).__init__(metadata)

      zone = token.split('-')[-1]

      self.template_location = 'templates/mailchimp.html'
      self.endpoint = 'https://{}.api.mailchimp.com/3.0/'.format(zone)
      self.token = token
      self.payload = {}
      self.audience_id = audience_id

      self.title = ""
      self.soup = None

      # Load basic auth header
      auth_header = base64.b64encode('meaningless:{}'.format(token)) 
      self.headers = {'Authorization': 'Basic {}'.format(auth_header)}

      # Check if template exists
      if os.path.isfile(self.template_location):
          with open(self.template_location) as input_file:
              self.soup = bs4.BeautifulSoup(input_file)
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

      # Write file to local
      today = date.today().strftime("%d-%m-%Y")
      print str(self.soup)
      with open("/var/log/mailchimp_template-{}".format(today)) as f:
        f.write(str(soup))

    def publish(self):
      # Check if the message has been formatted

      # Generate campaign
      # Generate campaign content
      
      pass
