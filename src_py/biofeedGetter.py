"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""


from biofeedProcessor import BioThreadedDataProcessor


class BioDataGetter(BioThreadedDataProcessor):
    """reads the data from the source"""
    """passes on a tuple of the channels' data"""
    
    def __init__(self, src, dst, noise=None):
        self.channels = src.channels
        super(BioDataGetter, self).__init__(src, dst)
        self.noise = noise
        

    def _getData(self):
        return self.src.read()
    
    def _putData(self, data):
        self.dst.put((self.src.comport, tuple(data[2])))
        

    
    def _transformData(self, dataIn):
        #print dataIn
        #print "d ", dataIn[2]
        #print "dataLength", len(dataIn)
        #print "channels", self.channels
        header = dataIn[0] & 0b01111110 >> 1
        if len(dataIn) == (3*(self.channels / 2))+2:
            aux =  dataIn[0] << 7 + dataIn[1] & 0b01111111
            offset=1
        else:
            aux=0
            offset=0
        ch = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(self.channels/2):
            j = 2*i
            k = 3*i
            ch[0+j] = (dataIn[1+k+offset] & 0b01111111) + ((dataIn[3+k+offset] & 0b01110000) << 3)
            ch[1+j] = (dataIn[2+k+offset] & 0b01111111) + ((dataIn[3+k+offset] & 0b00000111) << 7)
#        sync = dataIn[self.channels/2+1] & 0b10000000
        return header, aux, tuple(ch)

    
    
    
    
    
##NOTES
    
#import ctypes

#        link = ctypes.cdll.sugarlink
        #dllpath = os.path.join(os.path.dirname(__file__), "sugarlink.dll")
        #link = ctypes.cdll.loadLibrary(dllpath)
#        self.getItemBell = link.getItemBell
    
    
    ## keep this in case we need to process each incomming byte one at a time!
#    def _read(source, cb, control):
#        waitForSync()
#        print "reading from serial port"
#        start = time.clock()
#        while time.clock() < start + 5:
#            print "."
#            x = ord(source.read())
#            header = (x & 0b01111110)>>1
#            aux =  ((x & 0b00000001) << 7) + ord(source.read()) & 0b01111111
#            data = [0, 0, 0, 0, 0, 0, 0, 0]
#            for i in range(4):
#                data[0+i] = ord(source.read()) & 0b01111111
#                data[1+i] = ord(source.read()) & 0b01111111
#                x = ord(source.read())
#                data[0+i] += (x & 0b01110000) << 3
#                data[1+i] += (x & 0b00000111) << 7
#                sync = x & 0b10000000
#            cb(header, aux, tuple(data))
#            if sync == 0:waitForSync()
    
    