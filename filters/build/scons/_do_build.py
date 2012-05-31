import sys
import os
import shutil
import platform
import subprocess

try:
    from build_config_local import *
except:
    from build_config_default import *

SCONS_CMD_OSX = "/usr/local/bin/scons"
SCONS_CMD_MSW = "C:\\Python26\\Scripts\\scons.bat"

BUILT_DIR_NAME_OSX = "osx"
BUILT_DIR_NAME_MSW = "msw"

LIB_EXT_OSX = [".dylib"]
LIB_EXT_MSW = [".dll", ".manifest"]

##PLATFORM
thisPlatform = platform.system()
if thisPlatform == 'Windows':
    SCONS_CMD = SCONS_CMD_MSW
    BUILT_DIR_NAME = BUILT_DIR_NAME_MSW
    LIB_EXTS = LIB_EXT_MSW 
    os.environ['VC_PATH'] = VISUAL_STUDIO_PATH
    os.environ['WIN_SDK_PATH'] = WINDOWS_SDK_PATH
    
elif thisPlatform == 'Darwin':
    SCONS_CMD = SCONS_CMD_OSX
    BUILT_DIR_NAME = BUILT_DIR_NAME_OSX
    LIB_EXTS = LIB_EXT_OSX
else:
    raise Exception, "Unknown %s platform in _do_build" % thisPlatform


def buildDlls():
    thispath = os.path.dirname(__file__)
    build_home =  os.path.join(thispath, "..", "..", "..")
    os.chdir(build_home)
    p = subprocess.Popen(SCONS_CMD)
    p.wait()
    
    builds_dir =  os.path.join(thispath, "builds", BUILT_DIR_NAME)
    dlls_dir =  os.path.join(thispath, "..", "..", "..", "src_py")
    for filename in os.listdir(builds_dir):
        if os.path.splitext(filename)[1] in LIB_EXTS:
            src = os.path.join(builds_dir, filename)
            dst = os.path.join(dlls_dir, filename)
            shutil.copy(src, dst)
