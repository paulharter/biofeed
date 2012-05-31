import unittest
from biofeedCollector import DataCollector


TEST_DATA = ({"one":154.7,
             "two":66.0,
             "three":44.1,
             "four":5.6},
             {"one":158.4,
             "two":66.2,
             "three":55.3,
             "four":6.4},
             {"one":169.2,
             "two":66.5,
             "three":23.6,
             "four":5.3},
             {"one":181.2,
             "two":66.9,
             "three":77.8,
             "four":5.2},
             {"one":199.0,
             "two":67.1,
             "three":98.3,
             "four":5.8},
             {"one":218.5,
             "two":67.4,
             "three":45.3,
             "four":5.9})

HISTORY_SIZE = 4

class BasicSetup(unittest.TestCase):
    
    def setUp(self):
        self.collector = DataCollector()
        self.ch1 = self.collector.addChannel("one", 4, 1)
        self.ch2 = self.collector.addChannel("two", 4, 1)
        self.ch3 = self.collector.addChannel("three", 4, 1)
        self.ch4 = self.collector.addChannel("four", 4, 1)

    def tearDown(self):
        pass
    
    
class Case01_PuttingData(BasicSetup): 
    
    def test01_canPutDataIn(self):
        collector = self.collector
        collector.put(TEST_DATA[0])
        self.assertEquals(len(collector.channels), 4)
        
        
    def test02_canGetaluesOut(self):
        collector = self.collector
        collector.put(TEST_DATA[0])
        self.assertEquals(self.ch1.value, 154.7)
        self.assertEquals(self.ch3.value, 44.1)     
        self.assertEquals(self.ch1.value, 154.7)#repeats if no new value
        collector.put(TEST_DATA[1])
        self.assertEquals(self.ch1.value, 158.4)
        self.assertEquals(self.ch2.value, (66.0 + 66.2)/2)#average if not got for two or more
        self.assertEquals(self.ch4.value, (5.6 + 6.4)/2)   
        collector.put(TEST_DATA[2])
        self.assertEquals(self.ch2.value, 66.5)#reset by last get
        
        
    def test03_canGetHistory(self):
        collector = self.collector
        for i in range(4):
            collector.put(TEST_DATA[i])
        history = self.ch1.history
        self.assertEquals(history[0], [154.7, 158.4, 169.2, 181.2])
        for j in range(2):
            collector.put(TEST_DATA[j + 4])
        history = self.ch1.history
        self.assertEquals(history[0], [169.2, 181.2, 199.0, 218.5])
        
        
class Case02_Combining(unittest.TestCase):
    
    def setUp(self):
        print "***************"
        self.collector = DataCollector()
        self.ch1 = self.collector.addChannel("one", 2, 2)
        self.ch2 = self.collector.addChannel("two", 2, 3)

    def tearDown(self):
        pass
    
    
    def test01_WhatAboutCombining(self):
        collector = self.collector
        for i in range(6):
            collector.put(TEST_DATA[i])
        self.assertEquals(self.ch1.history[0], [175.2, 208.75])
        self.assertEquals(self.ch2.history[0], [198.7/3, 201.4/3])
       
        
        
if __name__ == '__main__':
    unittest.main()   
        