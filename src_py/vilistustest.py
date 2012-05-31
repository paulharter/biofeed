import socket
import time

class VilistusTest(object):
    def runTest(self):
        self.pollString="RING\n"
        HOST = '169.254.1.1'
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print "try connect",self.s
        self.s.connect((HOST,2000))
        print "connected - wait for response"
        print self.s.recv(8)
        time.sleep(0.1)
        self.s.send("$$$")
        time.sleep(0.5)
        print self.s.recv(1024)
        print "Param set"
        self.s.send("set com time 10\r") # set maximum wait between buffers
        self.s.send("set com size 140\r") # set buffer size
        self.s.send("set ip flags 3\r") # turn off TCP retries
        print self.s.recv(1024)
        time.sleep(0.5)
#        time.sleep(0.5)
        self.s.send("exit\r")        
        time.sleep(0.5)
#        time.sleep(0.5)
        print "poll"
        self.s.send(self.pollString)
        print "poll"
        self.s.send(self.pollString)
        print "connected okay"
        self.s.settimeout(5.0)
        self.sync=0
        
        totalLen=0
        print "time me"
        while totalLen<256*5*14:
            totalLen+=len(self.s.recv(2000))
        print "5 seconds"
#        for c in range(0,1000):
#            totalLen
#            try:                
#                print len(self.s.recv(2000)),"*",c
#            except socket.timeout,e:
#                print "timeout *"
        resyncNum=0
        for c in range(0,100000):
            try:
#                resyncCount=0
                if self.sync==0:
                    resyncNum=resyncNum+1
#                    print "resync:",
                while self.sync==0:
                    recvByte=ord(self.s.recv(1)[0])
                    self.sync=recvByte&0b10000000
#                    print "%x,"%recvByte,
#                if resyncCount!=0:
#                    print "[%d]"%(resyncCount)
                    
                buffsize=0
                retVal=""
                while buffsize<14:
                    buff=self.s.recv(14-buffsize)
                    buffsize+=len(buff)
                    retVal+=buff
                if len(retVal)==14:
#                    print ".",
                    self.sync=ord(retVal[-1])&0b10000000
#                    print retVal
                    if c%64 == 0:
                        self.curValue=ord(retVal[5])+((ord(retVal[7])&0b01110000)<<3)
                        print "<%d> %x,%x,%d,%d"%(c,ord(retVal[2]),ord(retVal[4]),resyncNum,self.curValue)
                        resyncNum=0
#                    for c in retVal:
#                        print "%x,"%ord(c),
#                    print ""
                else:   
                    print "short"
                    self.sync=0
            except socket.timeout,e:
                print "timeout"
                print "poll"
                self.s.send(self.pollString)
                print "poll"
                self.s.send(self.pollString)
        self.s.close()
            

v=VilistusTest()
v.runTest()