import biofeed
import time
from biofeedSource import *
from dummySerials import SineWaveDummySerialDataSource

port = 80
bio = biofeed.Biofeed()
wiffy = WifiTCPDataSource(port, 8)
#dummy = SineWaveDummySerialDataSource(port, 8)
bio.addDsu(port, 8, wiffy)

ch1 = bio.addChannel("heart", port, 0, [], 100, 1)

bio.start()

for i in range(100):
    time.sleep(0.1)
    print ch1.lastValue
    
bio.stop()

