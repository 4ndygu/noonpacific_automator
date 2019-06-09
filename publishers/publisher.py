from abc import ABCMeta, abstractmethod

import logging
import requests
import sys

class Publisher:
    __metaclass__ = ABCMeta
 
    def __init__(self, metadata):
        self.track_metadata = metadata["tracks"]
        self.mixtape_metadata = metadata["mixtape"]
    
    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def publish(self):
        pass
