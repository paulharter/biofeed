import unittest
from biofeedSource import SerialDataSource
from dummySerials import DummySerialDataSource
from biofeedGetter import BioDataGetter

import time
#import numpy
import Queue

P3_INPUT = (0,
    0,
    1,
    1,
    1,
    4,
    64,
    68,
    0,
    0,
    0,
    0,
    0,
    128)


P3_OUTPUT = (1,
    129,
    516,
    576,
    0,
    0,
    0,
    0)

PORT_NUMBER = 39
CHANNELS = 8

class BasicSerialSetup(unittest.TestCase):
    
    def setUp(self):
        self.channels = CHANNELS
        self.port = PORT_NUMBER
        self.queue = Queue.Queue()
        #self.dataSource = SerialDataSource(self.port, self.channels)
        self.dataSource = DummySerialDataSource(self.port, self.channels)
        self.dataSource.open()
       
    def tearDown(self):
        print "closing connection"
        self.dataSource.close()



class Case01_DummySerialConnectionTests(BasicSerialSetup): 

    def test01_canReadFromSerialDevice(self):
        print "test01_hasInterface"
        #if not self.dataSource.serial.isOpen():self.fail("failed in test01_canReadFromSerialDevice: port not opened")
        try:
            data = self.dataSource.read()
        except:
            self.fail("failed in test01_canReadFromSerialDevice: read failed")
        self.assertEquals(14, len(data))
        self.assertEquals(type(data), type(["hello",]))
        
    def test02_canReadFromSerialDeviceAgain(self):
        print "test01_hasInterface"
        #if not self.dataSource.serial.isOpen():self.fail("failed in test02_canReadFromSerialDeviceAgain: port not opened")
        try:
            data = self.dataSource.read()
        except:
            self.fail("failed in test02_canReadFromSerialDeviceAgain: read failed")
        self.assertEquals(14, len(data))
        
        
class Case02_ProtocolParseTest(BasicSerialSetup):
        
    def test01_canGetData(self):
            getter = BioDataGetter(self.dataSource, self.queue)
            inputArray = getter._getData()
            for a, b in zip(inputArray, P3_INPUT):
                self.assertEquals(a, b)
            
            
    def test02_canParseP38channel(self):
            getter = BioDataGetter(self.dataSource, self.queue)
            input = getter._getData()
            output = getter._transformData(input)
            self.assertEquals(P3_OUTPUT, output[2])
            
            
    def test03_canParseP38channelFast(self):
            getter = BioDataGetter(self.dataSource, self.queue)
            input = getter._getData()
            start = time.time()
            for i in range(1000):
                output = getter._transformData(input)
            end = time.time()
            dur = (end - start)/1000.0
            self.assertTrue(dur < 0.0002)     
            
    def test04_canPutDataInQueue(self):
            getter = BioDataGetter(self.dataSource, self.queue)
            input = getter._getData()
            data = getter._transformData(input)
            getter._putData(data)
            out = getter.dst.get(True, 3)
            self.assertEquals(PORT_NUMBER, out[0])
            self.assertEquals(P3_OUTPUT, out[1])
            
if __name__ == '__main__':
    unittest.main()         
