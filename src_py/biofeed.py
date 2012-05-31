"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

from biofeedSource import SerialDataSource
from biofeedGetter import BioDataGetter

import biofeedFilter

from biofeedCollector import DataCollector

HISTORY_SIZE = 100

class Dsu(object):
    
    def __init__(self, dst, serial, noise=None):
        self.serial = serial
        self.getter = BioDataGetter(self.serial, dst, noise=noise)
        
    def pump(self):
        self.serial.open()
        self.getter.pump()
        self.serial.close()
        
    def start(self):
        self.serial.open()
        self.getter.start()
        
    def stop(self):
        self.getter.stop()  
        self.serial.close()
          
        
class Biofeed(object):
    
    def __init__(self, limit=None):
        self.collector = DataCollector(limit=limit)
        self.manager = biofeedFilter.BioFilterManager(self.collector)
        #self.manager = biofeedFilter.BioFilterManager()
        self.dsus = []
        
    def start(self):
        self.manager.start()
        for dsu in self.dsus:
            dsu.start()
            
    def stop(self):
        for dsu in self.dsus:
            dsu.stop()
        self.manager.stop()
        
    def addDsu(self, port, channels, serial=None, saveToFile=None):
        """ 
        Add a DSU to biofeed, giving the com port number and the number of channels it has
        serial is intended for passing in a dummy when testing: ignore in normal use.
        """
        serialConnection = serial if serial else SerialDataSource(port, channels, saveToFile=saveToFile)
        self.dsus.append(Dsu(self.manager.src, serialConnection))
        
    def addChannel(self, name, port, ch, filters, size, combine):
        """ 
        Add a named channel to biofeed giving the com port, channel (0 based index of DSU ch) and a list of filters to apply
        """
        self.manager.addChannel(name, port, ch, filters)
        return self.collector.addChannel(name, size, combine)
        
    
    ## just for testing really
    def _pump(self):#single threaded single get/put
        for dsu in self.dsus:
            dsu.pump()
        self.manager.pump()
    
    def _hasReachedLimit(self):
        return self.collector.reachedLimit
        
    