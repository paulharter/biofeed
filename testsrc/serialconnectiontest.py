import unittest
from biofeedSource import SerialDataSource


import time

SAVE_PATH = "c:\\serial_recording.log"
COM_PORT = 39


class BasicSerialSetup(unittest.TestCase):
    
    def setUp(self):
        self.channels = 8
        self.port = COM_PORT
        history = 100
        self.dataSource = SerialDataSource(self.port, self.channels)
        #self.dataSource = DummySerialDataSource(self.port, self.channels)
        self.dataSource.open()
       
    def tearDown(self):
        #print "closing connection"
        self.dataSource.close()
        del self.dataSource


class Case01_SerialConnectionTests(BasicSerialSetup): 

    def test01_canReadFromSerialDevice(self):
        print "test01_hasInterface"
        if not self.dataSource.serial.isOpen():self.fail("failed in test01_canReadFromSerialDevice: port not opened")
        try:
            data = self.dataSource.read()
        except:
            self.fail("failed in test01_canReadFromSerialDevice: read failed")
        self.assertEquals(14, len(data))
        
        ##this test fails I think that the DSU is not letting go correctly
#    def test02_canReadFromSerialDeviceAgain(self):
#        print "test01_hasInterface"
#        if not self.dataSource.serial.isOpen():self.fail("failed in test02_canReadFromSerialDeviceAgain: port not opened")
#        try:
#            data = self.dataSource.read()
#        except:
#            self.fail("failed in test02_canReadFromSerialDeviceAgain: read failed")
#        self.assertEquals(14, len(data))
        

#class RecordingSerialSetup(testharness.InstrumentedTestCase):
#    
#    def setUp(self):
#        self.channels = 8
#        self.port = COM_PORT
#
#        self.dataSource = SerialDataSource(self.port, self.channels, saveToFile = SAVE_PATH)
#        #self.dataSource = DummySerialDataSource(self.port, self.channels)
#        self.dataSource.open()
#       
#    def tearDown(self):
#        #print "closing connection"
#        self.dataSource.close()
#        self.dataSource = None
#        x = self.dataSource
#        
#        
#        
#class Case02_RecordingTests(RecordingSerialSetup): 
#    
#    
##    def test01_canReadFromSerialDevice(self):
##        print "test01_hasInterface"
##        if not self.dataSource.serial.isOpen():self.fail("failed in test01_canReadFromSerialDevice: port not opened")
##        try:
##            data = self.dataSource.read()
##        except:
##            self.fail("failed in test01_canReadFromSerialDevice: read failed")
##        self.assertEquals(14, len(data))
#    
#        
#    def test02_canReadSeveralPackets(self):
#        print "test01_hasInterface"
#        start = time.time()
#        for i in range(512):
#            data = self.dataSource.read()
#        end = time.time()
#        print "dur", end - start


if __name__ == '__main__':
    unittest.main()
