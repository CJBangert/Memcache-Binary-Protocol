
from typing import Dict


class Memcache:

    def __init__(self):
        
        self.cache = {}

    def setitem(self, key, value):
        
        self.cache[key] = value

        print("Successfully added value: ", self.cache[key], flush=True)
            
        

    def getitem(self, key):

        if(key in self.cache):

            val = self.cache[key]

            print("Got value: ", val, flush=True)

            return val

        else:

            print("Key not found: ", key, flush=True)

            return None