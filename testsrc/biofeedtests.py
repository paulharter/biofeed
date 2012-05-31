import time

import unittest
from biofeed import Biofeed
from dummySerials import DummySerialDataSource, BigDummySerialDataSource, RacingDummySerialDataSource, SineWaveDummySerialDataSource

# some big end to end tests


class BasicSetup(unittest.TestCase):
    
    def setUp(self):
        self.biofeed = Biofeed(20)

    def tearDown(self):
        pass
    
    
class Case01_Basic(BasicSetup): 
    
    def test01_canMakeOne(self):pass
    
    def test02_canAddADsu(self):
        biofeed = self.biofeed
        dummy = DummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
    
    def test03_canAddAChannel(self):
        biofeed = self.biofeed
        dummy = DummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        biofeed.addChannel("one", 40, 0, [], 20, 1)

    def test04_canPassAValueThrough(self):
        biofeed = self.biofeed
        dummy = DummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 1, ["null"], 20, 1)
        biofeed._pump()
        self.assertEquals(129.0 , ch1.value)
        #how cool is that!
        
    def test05_canPassAValueThrough2(self):
        biofeed = self.biofeed
        dummy = DummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 1, [], 20, 1)
        biofeed._pump()
        self.assertEquals(129.0 , ch1.value)
        #how cool is that!
        
    def test06_canCalibrateAChannel(self):
        biofeed = self.biofeed
        dummy = DummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 1, [], 20, 1)
        ch1.calibrate(4.0, 0.5)
        biofeed._pump()
        self.assertEquals((129.0 + 4.0)*0.5 , ch1.value)
        
        

class Case02_Threaded(BasicSetup): 
    
    
    def test01_canRunThreadedWithDummy(self):
        biofeed = self.biofeed
        dummy = BigDummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 0, [], 20, 1)
        biofeed.start()
        while not biofeed._hasReachedLimit():pass
        biofeed.stop()
        self.assertEquals(20.0,  ch1.lastValue)
        self.assertEquals([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],  ch1.history[0])
        
        
    def test02_canGetMovingAverage(self):
        biofeed = self.biofeed
        dummy = BigDummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 0, [], 20, 1)
        ch2 = biofeed.addChannel("two", 40, 0, ["average"], 20, 1)
        biofeed.start()
        while not biofeed._hasReachedLimit():pass # does just 20 samples
        biofeed.stop()
        self.assertEquals([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],  ch1.history[0])
        self.assertEquals(20.0,  ch1.lastValue)
        self.assertEquals((15+16+17+18+19+20)/6.0,  ch2.lastValue)
    
    
    def test03_benchmark(self):
        biofeed = Biofeed()
        dummy = RacingDummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 1, ["emg"], 20, 1)
        ch2 = biofeed.addChannel("two", 40, 2, ["emg"], 20, 1)
        ch3 = biofeed.addChannel("three", 40, 3, ["gsr"], 20, 1)
        ch4 = biofeed.addChannel("four", 40, 4, ["ecg"], 20, 1)
        biofeed.start()
        time.sleep(10)
        biofeed.stop()
        print " %f samples per second benchmark with racing dummy" % (biofeed.collector.testCount/10.0)
        
        
    def test04_canUseSinWave(self):
        biofeed = Biofeed()
        dummy = SineWaveDummySerialDataSource(40, 8)
        biofeed.addDsu(40, 8, dummy)
        ch1 = biofeed.addChannel("one", 40, 1, ["emg"], 20, 1)
        ch2 = biofeed.addChannel("two", 40, 2, ["emg"], 20, 1)
        ch3 = biofeed.addChannel("three", 40, 3, ["gsr"], 20, 1)
        ch4 = biofeed.addChannel("four", 40, 4, ["ecg"], 20, 1)
        biofeed.start()
        time.sleep(10)
        biofeed.stop()
        print " %f samples per second benchmark with sine wave dummy" % (biofeed.collector.testCount/10.0)
        
   
if __name__ == '__main__':
    unittest.main()       
        