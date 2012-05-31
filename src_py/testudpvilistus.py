import socket,time

tcpSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "try connect",tcpSock
tcpSock.connect(('169.254.1.1',2000))
print "connected - wait for response"
print tcpSock.recv(8)
time.sleep(0.1)
tcpSock.send("$$$")
time.sleep(0.5)
print tcpSock.recv(1024)
print "Param set"
tcpSock.send("set com time 0\r") # set maximum wait between buffers
tcpSock.send("set com size 140\r") # set buffer size
tcpSock.send("set ip flags 3\r") # turn off TCP retries
tcpSock.send("set ip host 169.254.1.10\r") # turn off TCP retries
tcpSock.send("set ip remote 49990\r") # turn off TCP retries
tcpSock.send("set sys autosleep 0\r") # turn off TCP retries
tcpSock.send("set ip proto 3\r") # turn off TCP retries
tcpSock.send("exit\r") 
tcpSock.send("RING\n")
tcpSock.send("RING\n")
tcpSock.close()

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 49990              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
s.settimeout(500)
count=0
print 'UDP Listening on port ',PORT
while 1:
    count=count+1
    data,address=s.recvfrom(1024)
    print address,len(data),count
print "end"

