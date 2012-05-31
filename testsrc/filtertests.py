import unittest

from biofeedFilter import BioFilterManager 

import time
#import numpy
import Queue

TEST_DATA = ((39, (14, 55, 0, 0, 0, 0, 0, 0)),
             (39, (24, 76, 167, 0, 0, 0, 0, 0)),
             (4, (1, 2, 3, 4, 5, 6, 7, 8)),
             (8, (4, 0, 0, 0, 0, 0, 0, 0)),
             (0, (5, 0, 0, 0, 0, 0, 0, 0)),
             (1, (1, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)),
             (0, (0, 0, 0, 0, 0, 0, 0, 0)))
             

class BasicSetup(unittest.TestCase):
    
    def setUp(self):
        self.manager = BioFilterManager(Queue.Queue())
        for v in TEST_DATA:
            self.manager.src.put(v)

       
    def tearDown(self):
        self.src = None



class Case01_SettingInputs(BasicSetup): 
    
    def test01_canMakeOne(self):
        pass
    
    
    def test02_addChannelsWithoutFilters(self):
        manager = self.manager
        manager.addChannel("one", 39, 0, ())
        self.assertEquals(len(manager.channels), 1)
        self.assertEquals(len(manager.inputs), 1)
        
        self.assertTrue("one" in manager.channels.keys())
        self.assertTrue(len(manager.channels["one"].filters) == 1)
        port, ch = manager.channels["one"].getInputPortAndCh()
        self.assertEquals(port, 39)
        self.assertEquals(ch, 0)
        # add some more
        manager.addChannel("two", 39, 1, ())
        manager.addChannel("three", 39, 2, ())
        self.assertEquals(len(manager.channels), 3)
        self.assertEquals(len(manager.inputs), 3)
        self.assertTrue("one" in manager.channels.keys())
        self.assertTrue("two" in manager.channels.keys())
        self.assertTrue("three" in manager.channels.keys())
        
        port, ch = manager.channels["two"].getInputPortAndCh()
        self.assertEquals(port, 39)
        self.assertEquals(ch, 1)

        port, ch = manager.channels["three"].getInputPortAndCh()
        self.assertEquals(port, 39)
        self.assertEquals(ch, 2)
        
    def test03_failsIfYouAddTwoIdenticalChannels(self):
        ##I stopped this in nottingham for some reason I forget
        manager = self.manager
        manager.addChannel("three", 39, 2, ())
        self.assertRaises(Exception, manager.addChannel, "three", 39, 2, ())
        

class Case02_GettingPuttingData(BasicSetup):
    

    def test01_putsDataIntoChannels(self):
        manager = self.manager
        manager.addChannel("one", 39, 0, ())
        manager.addChannel("two", 39, 1, ())
        manager.addChannel("three", 39, 2, ())
        inputData = manager._getData()
        output = manager._transformData(inputData)
        #print "b", output.keys()
        self.assertEquals(len(output), 3)
        self.assertTrue("one" in output.keys())
        self.assertTrue("two" in output.keys())
        self.assertTrue("three" in output.keys())
        self.assertEquals(output["one"], 14)
        self.assertEquals(output["two"], 55)
        self.assertEquals(output["three"], 0)
        inputData = manager._getData()
        output = manager._transformData(inputData)
        self.assertEquals(output["one"], 24)
        self.assertEquals(output["two"], 76)
        self.assertEquals(output["three"], 167)
        inputData = manager._getData()
        output = manager._transformData(inputData)
        self.assertEquals(len(output), 0)


    def test02_putsDataIntoOutputCorrectly(self):
        manager = self.manager
        manager.addChannel("one", 39, 0, ())
        manager.addChannel("two", 39, 1, ())
        manager.addChannel("three", 39, 2, ())
        inputData = manager._getData()
        output = manager._transformData(inputData)
        manager._putData(output)
        out = manager.dst.get(True, 3)
        self.assertEquals(output, out)
            
            
class Case03_Filters(BasicSetup):
   
   
    def test01_canAddFilters(self):
       manager = self.manager
       manager.addChannel("one", 39, 0, ("null",))
       port, ch = manager.channels["one"].getInputPortAndCh()
       self.assertEquals(port, 39)
       self.assertEquals(ch, 0)
       self.assertEquals(len(manager.channels["one"].filters), 2)
       manager.addChannel("two", 39, 1, ("null",))
       manager.addChannel("three", 39, 0, ("average",))
       self.assertEquals(len(manager.channels), 3)
       
       
    def test02_canPutDataThroughFilters(self):
        manager = self.manager
        manager.addChannel("test", 39, 0, ("test",))
        manager.addChannel("one", 39, 0, ("null",))
        port, ch = manager.channels["one"].getInputPortAndCh()
        self.assertEquals(port, 39)
        self.assertEquals(ch, 0)
        self.assertEquals(len(manager.channels["one"].filters), 2)
        manager.addChannel("two", 39, 1, ("null", "average"))
        manager.addChannel("three", 39, 0, ("average",))
        self.assertEquals(len(manager.channels), 4)
        inputData = manager._getData()
        output = manager._transformData(inputData)
        inputData = manager._getData()
        output = manager._transformData(inputData)
        
        self.assertEquals(output["test"], 44.6)
        self.assertEquals(output["one"], 24.0)
        print output["two"]
        
        self.assertEquals(output["two"], (55+76.0)/6.0)
        print output["three"]
        self.assertEquals(output["three"], (14+24)/6.0)
        print manager
       


if __name__ == '__main__':
    unittest.main()  
    