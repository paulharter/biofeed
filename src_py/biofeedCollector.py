"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

import threading


class Channel(object):
    
    value = property(lambda self: self._getValue())
    lastValue = property(lambda self: self._getLastValue())
    history = property(lambda self: self._getHistory())

    def __init__(self, name, size, combine, lock, collector): 
        self.name = name
        self._value = 0.0
        self.size = 1
        self.reset = True
        self._history = size * [0.0]
        self.callibrate = False
        self.offset = 0.0
        self.multiplier = 1.0
        self.lock = lock
        self.collector = collector
        self.combine = combine
        self.historySize = size
        self.combineIndex = -1
        self.historyIndex = -1
        self.historyAccumulator = 0.0
        self.new = True
        
    def calibrate(self, offset, multiplier):
        self.callibrate = True
        self.offset = offset
        self.multiplier = multiplier
        
    def add(self, value):
        v = (value + self.offset) * self.multiplier if self.callibrate else value
        if self.reset:
            self._value = v
            self.size = 1
            self.reset = False
        else:
            self._value = self._value + v
            self.size = self.size + 1
            
        if self.combine > 1:
            self.combineIndex = self.combineIndex + 1
            self.historyAccumulator = self.historyAccumulator + v
            if self.combineIndex == self.combine - 1:
                self.historyIndex = self.historyIndex + 1
                if self.historyIndex == self.historySize:self.historyIndex = 0   
                self._history[self.historyIndex] = self.historyAccumulator/self.combine
                self.historyAccumulator = 0.0
            if self.combineIndex == self.combine:
                self.combineIndex = 0  
        else:
            self.historyIndex = self.historyIndex + 1
            if self.historyIndex == self.historySize:self.historyIndex = 0   
            self._history[self.historyIndex] = v
        
            
    
    def _getValue(self):
        self.lock.acquire()
        self.reset = True
        value = self._value/self.size
        self.lock.release()
        return value
    
    def _getLastValue(self):
        self.lock.acquire()
        self.reset = True
        value = self._history[self.historyIndex]
        self.lock.release()
        return value
    
    def _getHistory(self):
        self.lock.acquire()
        self.reset = True
        history = self._history[self.historyIndex+1:] + self._history[:self.historyIndex+1]
        size = float(self.combine)
        index = self.combineIndex + 1 if self.combineIndex < size-1 else 0
        fraction = index/size
        self.lock.release()
        return history, fraction
       

class DataCollector(object):
    """ a thread safe data collector with averaging"""
    """ also history of a channel"""
    
    def __init__(self, limit=None):
        self.lock = threading.Lock()
        self.channels = {}
        self.testCount = 0
        self.index = -1
        self.limit = limit
        self.reachedLimit = False
        
        
    def addChannel(self, name, size, combine):
        return self._getChannel(name, size, combine)
        
        
    def _getChannel(self, name, size=100, combine=1):
        #print "Combine", combine
        channel = self.channels.get(name)
        if not channel:
            #print "combinecombine"  , combine
            channel = Channel(name, size, combine, self.lock, self)
            self.channels[name] = channel
        return channel
        
        
    def put(self, data):
        if self.limit and self.testCount == self.limit:
            self.reachedLimit = True
            return
        self.lock.acquire()
        self.testCount = self.testCount + 1

        for name, value in data.iteritems():
            channel = self._getChannel(name)
            channel.add(value)
        self.lock.release()
    
