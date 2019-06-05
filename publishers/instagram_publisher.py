from publisher import Publisher

class BufferPubisher(Publisher):

    def __init__(self, metadata, tokens, pythontoken=[]):
      super().__init__()
      self.endpoint = "https://api.bufferapp.com/1/updates/create.json"
      self.tokens = tokens
      self.pythontoken = pythontoken
      self.payload = {}

    def format(self):
      self.payload["text"] = ['{} - {}'.format(item['title'], item['artist']) 
        for item in self.track_metadata]
      self.payload["media"] = {"link": self.mixtape_metadata['artwork_url'], 
                               "description": "Art by {}".format(self.mixtape_metadata['artwork_credit'])}}
      self.payload["text"] = "SOME SHIT"

    def format_twitter(self):
      self.payload["text"] = ['{} - {}'.format(item['title'], item['artist']) 
        for item in self.track_metadata]
      self.payload["media"] = {"link": self.mixtape_metadata['artwork_url'], 
                               "description": "Art by {}".format(self.mixtape_metadata['artwork_credit'])}}
      self.payload["text"] = "SOME SHIT"

    def publish(self):
      resp = requests.post(endpoint, payload=self.payload)
      
      # error handling for the request
      if resp.status_code != 200:
          if resp.json()["success"] != "true":
              pass


      
      
