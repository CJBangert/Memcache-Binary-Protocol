
from typing import Dict


class Memcache:

    def __init__(self):
        
        self.cache = {}

    def setitem(self, key, value):
        
        self.cache[key] = value

        print("Successfully added value: ", self.cache[key])
            
        

    def getitem(self, key):

        if(key in self.cache):

            return self.cache[key]

        else:

            return None