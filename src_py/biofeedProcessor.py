"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

import threading

class BioThreadedDataProcessor(object):
    """just a base class for common threading bits"""
    
    def __init__(self, src, dst):
        self.thread = None
        self.alive = threading.Event()
        self.src = src
        self.dst = dst

    def start(self):
        self._StartThread()
        
    def stop(self):
        self._StopThread()

    def _StartThread(self):     
        self.thread = threading.Thread(target=self._threadEntry)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()

    def _StopThread(self):
        if self.thread is not None:
            self.alive.clear()          #clear alive event for thread
            self.thread.join()          #wait until thread has finished
            self.thread = None

    def _threadEntry(self):
        while self.alive.isSet():self.pump()
            
    def pump(self):
        data = self._getData()  
        if not data is None:
            data = self._transformData(data)
            self._putData(data)
            
    ##You have to write these
            
    def _getData(self):
        return 0
    
    def _putData(self, data):
        # put somedata in dst
        pass
    
    def _transformData(self, data):
        return data