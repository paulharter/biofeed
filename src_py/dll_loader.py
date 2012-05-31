import ctypes
import os
import platform


#enables ctypes to find dlls
dllpath =  os.path.dirname(__file__)

IS_MAC = bool(platform.mac_ver()[0])
IS_WINDOWS = bool(platform.win32_ver()[0])
_LIBS_CACHE = {}
    
def getLib(libname):
    lib = _LIBS_CACHE.get(libname)
    if lib: return lib

    if IS_WINDOWS:
        #TODO: #FROZEN DLL move to configuration
        libpath =  os.path.join(dllpath, "%s.dll" % libname) 
    elif IS_MAC:
        #TODO: #FROZEN DLL
        libpath =  os.path.join(dllpath, "%s.dylib" % libname) 
    else:
        raise Exception, "Unknown platform in dll_loader"

    lib = ctypes.CDLL(libpath)
    _LIBS_CACHE[libname] = lib
    return lib


def closeLib(lib):
    del lib
    lib = 1
    x = lib

