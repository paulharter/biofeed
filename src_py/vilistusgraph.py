import socket
import time
import threading
import sys
import array

class VilistusTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.curValue=0
        self.valueList=array.array("i",[0]*1000)
        self.valueList2=array.array("i",[0]*1000)
        self.valueListLen=0
        self.lock = threading.Lock()
        
    def run(self):
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
#        self.s.send("set com size 994\r") # set buffer size
        self.s.send("set com size 140\r") # set buffer size
#        self.s.send("set ip flags 3\r") # turn off TCP retries
        self.s.send("set ip flags 7\r") #  TCP retries
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
        
#        totalLen=0
#        print "time me"
#        while totalLen<256*5*14:
#            totalLen+=len(self.s.recv(2000))
#        print "5 seconds"
#        for c in range(0,1000):
#            totalLen
#            try:                
#                print len(self.s.recv(2000)),"*",c
#            except socket.timeout,e:
#                print "timeout *"
        resyncNum=0
        c=0
        while True:
            c=c+1
#        for c in range(0,100000):
            try:
#                resyncCount=0
                if self.sync==0:
                    resyncNum=resyncNum+1
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
                    if self.sync!=0:
                        with self.lock:
                            self.curValue=ord(retVal[5])+((ord(retVal[7])&0b01110000)<<3)
                            self.valueList[self.valueListLen]=self.curValue
                            self.valueListLen=self.valueListLen+1
                            if self.valueListLen>999:self.valueListLen=999
                    if c%512 == 0:
                        print "<%d> %x,%x,%d,%d"%(c,ord(retVal[2]),ord(retVal[4]),self.curValue,resyncNum)
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
        
    def getValue(self):
        val=0
        with self.lock:
            val=self.curValue
        return val

    def getValueList(self):
#        print "getvals",self.valueListLen
        #swap lists - quick - can block thread for this
        with self.lock:
            numVals=self.valueListLen
            temp=self.valueList
            self.valueList=self.valueList2
            self.valueList2=temp
            self.valueListLen=0
        val=self.valueList2[0:numVals]
        return val
            


# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    #startup vilistus in thread
    v=VilistusTest()
    v.start()
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
#    logo = pygame.image.load("logo32x32.png")
#    pygame.display.set_icon(logo)
    pygame.display.set_caption("vilistus test")
    
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((640,480))
    
    # define a variable to control the main loop
    running = True
    
    image = pygame.image.load("ball.png")
    screen.fill((255,255,255))
    pygame.display.flip()
    screen.fill((255,255,255))
    
    # main loop
    x=0
    while running:
        time.sleep(0.1)
#        val=v.getValue()
        values = v.getValueList()
        if len(values)==0:
            time.sleep(0.05)
        for val in values[0:64]:
            y = (400.0 * val)/1024.0
            screen.blit(image, (x,y))
            x=x+1
            if x>600:
                x=0
                screen.fill((255,255,255))
        # update the screen to make the changes visible (fullscreen update)
        time.sleep(0.005)
#        y = (400.0 * val)/1024.0
#        screen.blit(image, (x,y))
#        x=x+1
#        if x>600:
#            x=0
        pygame.display.flip()
#        if len(values)>0:print values[0]
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
    
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
    sys.exit(0)
