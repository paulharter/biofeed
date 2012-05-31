"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

import serial
import time
import socket
from collections import deque

class SerialDataSource(object):
    """ reads from the given com port number a P3 data packet with a given number of channels as a string"""
    
    def __init__(self, comport, channels, saveToFile=None):
        self.sync = 0
        self.comport = comport
        self.serial = None
        self.packetSize = ((channels/2)*3) + 2
        self.saveToFile = saveToFile
        self.saveTo = None
        self.channels = channels
        self.data = 14 * [1]
        self.last = 0
    
    def open(self):
        self.serial = serial.Serial(self.comport, timeout=1)
        if self.saveToFile:
            self.saveTo = file(self.saveToFile, "w")
        
    def close(self):
        #print "closing"
        self.serial.close()
        if self.saveTo:
            self.saveTo.close()
            
            
    def read(self):
        while self.sync == 0:
            input = self.serial.read()
            if input:
                x = ord(input)
                self.sync = x & 0b10000000
                
        now = time.clock()
        dur = now - self.last
        while dur < 0.0039062:
            now = time.clock()
            dur = now - self.last
        #print dur
        self.last = now
        if self.serial.inWaiting() > self.packetSize * 100:
            #print "flushing"
            self.serial.flushInput()
        for i in range(self.packetSize):
            v = self.serial.read()
            self.data[i]= ord(v)
            if self.saveTo:self.saveTo.write(v)

        self.sync = self.data[-1]& 0b10000000
        #if self.saveTo:self.saveTo.write(self.data)
        return self.data
        
#    def read(self):
#        while self.sync == 0:
#            input = self.serial.read()
#            if input:
#                x = ord(input)
#                self.sync = x & 0b10000000
#                
#
#        if self.serial.inWaiting() > self.packetSize * 1000:
#            self.serial.flushInput()
#        for i in range(self.packetSize):
#            self.data[i]= ord(self.serial.read())
#
#        self.sync = self.data[-1]& 0b10000000
#        #if self.saveTo:self.saveTo.write(self.data)
#        return self.data
    
#    def read(self):
#        while self.sync == 0:
#            input = self.serial.read()
#            if input:
#                x = ord(input)
#                self.sync = x & 0b10000000
#
#        if self.serial.inWaiting() > self.packetSize * 4: 
#            print "flushing"
#            self.serial.flushInput()
#        while self.serial.inWaiting() < self.packetSize:pass
#        data = self.serial.read(self.packetSize)
#        self.sync = self.data[-1]& 0b10000000
#
#        return data

class WifiTCPDataSource(object):
    """ reads from the given address a P3 data packet with a given number of channels as a string"""
    
    def __init__(self, port, channels, saveToFile=None):
        self.sync = 0
        self.s=None
        self.packetSize = ((channels/2)*3) + 2
        self.saveToFile = saveToFile
        self.saveTo = None
        self.channels = channels
        self.comport=port
        self.data = self.packetSize * [1]
        self.last = 0
        self.buffer = deque()
        self.pollString="RING\n"
    
    def open(self):
        HOST = '169.254.1.1'                 
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print "try connect"
        self.s.connect((HOST,2000))
        print "connected - wait for response"
        print self.s.recv(8)
        print "poll"
        self.s.send(self.pollString)
        print "poll"
        self.s.send(self.pollString)
        print "connected okay"
        self.s.settimeout(5.0)
        self.sync=0
#        print str
#        for c in str: 
#            print ord(c),",",
        if self.saveToFile:
            self.saveTo = file(self.saveToFile, "w")
        
    def close(self):
        #print "closing"
        self.s.close()
        if self.saveTo:
            self.saveTo.close()
            

#    def getMoreData(self):
#        input = self.tn.read_eager()
#        if len(input)>0:
#            self.buffer.extend(input)
#            print "yay"
#        self.tn.write("\n")
#        print "woo"

    def getBytes(self,size):
        while True:
            try:
                v=self.s.recv(size)
                return v
            except socket.timeout,e:
                print "poll"
                self.s.send(self.pollString)
                print "poll"
                self.s.send(self.pollString)
            
            
    def read(self):
        amountGot=0
        while self.sync==0:
            self.sync=ord(self.s.recv(1)[0])&0x80
            print "resync"
        buffsize=0
        retVal=""
        while buffsize<14:
            buff=self.getBytes(14-buffsize)
            buffsize+=len(buff)
            retVal+=buff
        if len(retVal)==14:
            self.sync=ord(retVal[-1])&0x80
            for c in range(0,len(retVal)):
                self.data[c]=ord(retVal[c])
                if self.saveTo:self.saveTo.write(v)
        
#            if amountGot<self.packetSize:
#                self.getMoreData()
 #       print "Got a whole buffer",self.data[-1],amountGot

#            if len(input)>0:
#            print "yay"
#            print '[',len(input),']',
#            if len(input)>=self.packetSize:
#                for i in range(self.packetSize):
#                    v = input[i]
#                    self.data[i]= ord(v)
#                    if self.saveTo:self.saveTo.write(v)
#                print self.data[0]
        
#        now = time.clock()
#        dur = now - self.last
#        while dur < 0.0039062:
#            now = time.clock()
#            dur = now - self.last
        #print dur
#        self.last = now
#        if self.serial.inWaiting() > self.packetSize * 100:
            #print "flushing"
#            self.serial.flushInput()
 #       for i in range(self.packetSize):
 #           v = self.tn.read()
 #           self.data[i]= ord(v)
 #           if self.saveTo:self.saveTo.write(v)

#        self.sync = self.data[-1]& 0b10000000
        #if self.saveTo:self.saveTo.write(self.data)
        return self.data

