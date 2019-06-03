from abc import ABC, abstractmethod

import requests

class Publisher(ABC):
 
    def __init__(self, metadata):
        self.track_metadata = metadata["tracks"]
        self.mixtape_metadata = metadata["mixtape"]
        super().__init__()
    
    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def publish(self):
        pass
