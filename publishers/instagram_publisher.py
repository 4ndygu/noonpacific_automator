from publisher import Publisher

class InstagramPubisher(Publisher):

    def __init__(self, token, metadata):
      super().__init__()
      self.endpoint = "https://api.bufferapp.com/1/updates/create.json"
      self.token = token
      self.payload = {}

    def format(self):
      self.payload["text"] = ['{} - {}'.format(item['title'], item['artist']) 
        for item in self.track_metadata]
      self.payload["media"] = {"link": self.mixtape_metadata['artwork_url'], 
                               "description": "Art by {}".format(self.mixta_emetadata['artwork_credit'])}
      
