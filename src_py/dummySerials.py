"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

import math
import time


DUMMY_DATA = ((1, 129, 516, 576, 0, 0, 0, 0),
              (2, 129, 517, 576, 2, 4, 6, 8),
              (3, 129, 520, 576, 0, 0, 0, 0),
              (4, 129, 520, 576, 2, 4, 6, 8),
              (5, 129, 527, 576, 0, 0, 0, 0),
              (6, 129, 539, 576, 2, 4, 6, 8),
              (7, 129, 545, 576, 0, 0, 0, 0),
              (8, 129, 534, 576, 2, 4, 6, 8),
              (9, 129, 532, 576, 0, 0, 0, 0),
              (10, 129, 530, 576, 2, 4, 6, 8),
              (11, 129, 523, 576, 0, 0, 0, 0),
              (12, 129, 520, 576, 2, 4, 6, 8),
              (13, 129, 516, 576, 0, 0, 0, 0),
              (14, 129, 511, 576, 2, 4, 6, 8),
              (15, 129, 505, 576, 0, 0, 0, 0),
              (16, 129, 517, 576, 2, 4, 6, 8),
              (17, 129, 516, 576, 0, 0, 0, 0),
              (18, 129, 538, 576, 2, 4, 6, 8),
              (19, 129, 539, 576, 0, 0, 0, 0),
              (20, 129, 520, 576, 2, 4, 6, 8)
              )


def P3PacketAsStringFromChannels(channels):
    packet = 14 * [0]
    for i in range(4):
        j = 3 * i
        k = 2 * i
        packet[2 + j] = channels[0 + k] & 0b0001111111
        packet[3 + j] = channels[1 + k] & 0b0001111111
        packet[4 + j] = ((channels[0 + k] & 0b1110000000) >> 3) + ((channels[1 + k] & 0b1110000000) >> 7)
    packet[13] = packet[13] + 0b10000000
    data = []
    for b in packet:
        data.append(b)
    return data
#    for b in packet:
#        data.append(chr(b))
#    return "".join(data)
    
class DummySerialDataSource(object):
    
    def __init__(self, comport, channels, delay = 0.2):
        self.last = time.time()
        self.data = self.initDataStrings()
        self.comport = comport
        self.channels = channels
        self.delay = delay
        
    def initDataStrings(self):
        return P3PacketAsStringFromChannels((1, 129, 516, 576, 0, 0, 0, 0))
    
    def open(self):
        pass
        
    def close(self):
        pass
    
    def read(self):
        now = time.time()
        while now - self.last < self.delay:
            now = time.time()
        self.last = now
        return self.data
    
    
class RacingDummySerialDataSource(object):
    
    def __init__(self, comport, channels):
        self.last = time.time()
        self.data = self.initDataStrings()
        self.comport = comport
        self.channels = channels
        
    def initDataStrings(self):
        return P3PacketAsStringFromChannels((1, 129, 516, 576, 0, 0, 0, 0))
    
    def open(self):
        pass
        
    def close(self):
        pass
    
    def read(self):
        return self.data
    
    
    
    
class BigDummySerialDataSource(DummySerialDataSource):
    
    def __init__(self, comport, channels):
        self.index = 0
        super(BigDummySerialDataSource, self).__init__(comport, channels)
    
    def initDataStrings(self):
        return [P3PacketAsStringFromChannels(ch) for ch in DUMMY_DATA]
    
    def read(self):
        now = time.time()
        while now - self.last < 0.01:
            now = time.time()
        self.last = now
        value = self.data[self.index]
        self.index = self.index + 1
        if self.index == 20: self.index = 0
        return value
    
    
class SineWaveDummySerialDataSource(DummySerialDataSource):
    
    def __init__(self, comport, channels):
        self.index = 0
        super(SineWaveDummySerialDataSource, self).__init__(comport, channels)
        
        
#    def initDataStrings(self):
#        data = []
#        ch = 8 * [0]
#        for i in range(128):
#            v =  0
#            for j in range(8):ch[j] = v
#            data.append(P3PacketAsStringFromChannels(ch))
#        for i in range(128):
#            v =  2047
#            for j in range(8):ch[j] = v
#            data.append(P3PacketAsStringFromChannels(ch))
#        return data
        
        
#    def initDataStrings(self):
#        data = []
#        ch = 8 * [0]
#        for i in range(256):
#            v =  i * 8
#            for j in range(8):ch[j] = v
#            data.append(P3PacketAsStringFromChannels(ch))
#        return data
    
    def initDataStrings(self):
        data = []
        ch = 8 * [0]
        for i in range(256):
            sinValue = math.sin((float(i)*(2 * math.pi))/256.0)
            #print sinValue
            v = int((sinValue + 1.0) * 512.0) ## in range 0 - 2048
            #print v
            if v == 1024:
                v = 1023
            for j in range(8):
                if j ==5:
                    ch[j] = v/2
                else:
                    ch[j] = v
            data.append(P3PacketAsStringFromChannels(ch))
        return data
    
    
    def read(self):
        time.sleep(0.003)
        value = self.data[self.index]
        self.index = self.index + 1
        if self.index == 256: self.index = 0
        return value
    