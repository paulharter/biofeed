
BIOFEED_SRC = r"D:\work\My Dropbox\clever_plugs\biofeed\code\src_py"
#VIZ_SRC = r"D:\work\cleverplugs\company\trunk\psychoViz\code\src"

DST = r"D:\work\My Dropbox\shared\biofeed_shared\psychoFIZZ\biofeed"

import os
import shutil



for filename in os.listdir(BIOFEED_SRC):
    if filename.endswith("py"):shutil.copy(os.path.join(BIOFEED_SRC, filename), os.path.join(DST, filename))

#for filename in os.listdir(VIZ_SRC):
    #if filename.endswith("py"):shutil.copy(os.path.join(VIZ_SRC, filename), os.path.join(DST, filename))
    
    
shutil.copy(os.path.join(BIOFEED_SRC, "filters.dll"), os.path.join(DST, "filters.dll"))


print "done"
