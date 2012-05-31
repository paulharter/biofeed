import time

import unittest
from biofeed import Biofeed

#live tests to be done when connected

PORT = 39


class BasicSetup(unittest.TestCase):
    
    def setUp(self):
        self.biofeed = Biofeed()

    def tearDown(self):
        pass
    
    
class Case01_Basic(BasicSetup): 
    
    def test01_canReadSomeData(self):
        biofeed = self.biofeed
        biofeed.addDsu(PORT, 8)
        ch1 = biofeed.addChannel("one", PORT, 1, [], 4, 1 )
        biofeed.start()
        time.sleep(5)
        biofeed.stop()
        print " %f samples per second" % (biofeed.collector.testCount/5.0)
        


if __name__ == '__main__':
    unittest.main()     
        