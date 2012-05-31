import biofeed
import time
from dummySerials import SineWaveDummySerialDataSource

port = 40
bio = biofeed.Biofeed()
dummy = SineWaveDummySerialDataSource(port, 8)
bio.addDsu(port, 8, dummy)

ch1 = bio.addChannel("heart", port, 0, [], 100, 1)

bio.start()

for i in range(100):
    time.sleep(0.1)
    print ch1.lastValue
    
bio.stop()

