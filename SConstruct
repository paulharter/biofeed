print "starting scons build"
import os
import platform


class PlatformBuildConstants_common(object):
    
    def __init__(self, debug=False):
        self.CPPDEFINES =['_DEBUG']if debug else['NDEBUG', 'NOASSERT']
        self.VS_PATH = os.path.join("#build", "vs")	
        self.PATH = ""
        self.CPPPATH = []
        self.LIBPATH = []
        self.TEMP = ""


class PlatformBuildConstants_win32(PlatformBuildConstants_common):
    
    def __init__(self, debug=False):
        super(PlatformBuildConstants_win32, self).__init__(debug) 
        
        VC_PATH = os.environ['VC_PATH']
        SDK_PATH = os.environ['WIN_SDK_PATH']

        VC_BIN = os.path.join(VC_PATH, r'VC\bin')
        VC_IDE = os.path.join(VC_PATH, r'Common7\IDE')
        
        self.PATH = "%s;%s" % (VC_BIN, VC_IDE)
        VC_INCLUDE = os.path.join(VC_PATH, r'VC\include')
        VC_LIB = os.path.join(VC_PATH, r'VC\lib')
        
		#Runtime - Multi-threaded Debug DLL (/MDd)
		#Optimization - Disabled (/Od)
		#Program Database for Edit & Continue (/ZI)
		#Warnings - Level 3 (/W3)
		#Minimal rebuild - Yes (/Gm)
		#Runtime Checks  - Both (/RTC1, equiv. to /RTCsu)
		#Compile as C++ Code (/TP)
		#Runtime - Multi-threaded DLL (/MD)
		#Optimization - Maximize Speed (/O2)
		#Debug info - C7 Compatible (/Z7)
		#Function level linking - Yes (/Gy)
		#calling convention __cdecl (/Gd)        
        
        self.CCFLAGS = ' /nologo /Gd /W3 /TP /MD /EHsc'
        if debug:
            self.CCFLAGS += ' /MDd /Od /ZI /Gm /RTC1'
        else:
            self.CCFLAGS += ' /MD /O2 /Z7 /Gy /GL /Zp1'
        self.LINKFLAGS = ' /NOLOGO /DLL  /LTCG '
        self.CPPDEFINES = self.CPPDEFINES + ['WIN32']
        self.PLATFORM_DIR_NAME = "msw"
        
        self.BUILD_PATH = os.path.join("#filters", "build", "scons", "builds", self.PLATFORM_DIR_NAME)
        self.CPPPATH.append(VC_INCLUDE)
        self.CPPPATH.append(os.path.join(SDK_PATH, "Include"))
        self.LIBPATH = [VC_LIB, os.path.join(SDK_PATH, "lib")]
        self.TEMP = os.environ['TMP']
        


class PlatformBuildConstants_osx(PlatformBuildConstants_common):

    def __init__(self, debug=False):

        super(PlatformBuildConstants_osx, self).__init__(debug)
		
		#32-bit & 64-bit intel?
        if debug:
            #self.CCFLAGS = ' -O0 -g -arch i386 -arch x86_64'
            self.CCFLAGS = ' -O0 -g -arch i386'
            #self.CCFLAGS = ' -O0 -g -arch i386 -isysroot /Developer/SDKs/MacOSX10.5.sdk -mmacosx-version-min=10.5'
        else:
            #self.CCFLAGS = ' -O2 -arch i386 -arch x86_64 '
            self.CCFLAGS = ' -O2 -arch i386'
            #self.CCFLAGS = ' -O2 -arch i386 -isysroot /Developer/SDKs/MacOSX10.5.sdk -mmacosx-version-min=10.5'

        #self.LINKFLAGS = ' -Wl,-undefined -Wl,warning -Wl,-flat_namespace -arch i386 -arch x86_64'
        self.LINKFLAGS = ' -Wl,-undefined -Wl,warning -Wl,-flat_namespace -arch i386'
        #self.LINKFLAGS = ' -Wl,-undefined -Wl,warning -Wl,-flat_namespace -arch i386 -isysroot /Developer/SDKs/MacOSX10.5.sdk -mmacosx-version-min=10.5'
        
        
        self.CPPDEFINES = self.CPPDEFINES + ['UNIX', 'DARWIN']
        self.PLATFORM_DIR_NAME = "osx"

        self.BUILD_PATH = os.path.join("#filters", "build", "scons", "builds", self.PLATFORM_DIR_NAME)

def getPlatformSpecificConstants(debug=False):
    thisPlatform = platform.system()
    if thisPlatform == 'Windows':
        return PlatformBuildConstants_win32(debug)
    elif thisPlatform == 'Darwin':
        return PlatformBuildConstants_osx(debug)  
    else:
        raise Exception, "Unknown %s platform in SConstruct" % thisPlatform


class Env(Environment):

    def init(self):
        self.platformConstants = getPlatformSpecificConstants()
        self['SHLIBPREFIX'] = ""
        self.Append(CPPDEFINES=self.platformConstants.CPPDEFINES)
        self.Append(LINKFLAGS=self.platformConstants.LINKFLAGS)
        if self.platformConstants.PATH:
        	self["ENV"]={'PATH': self.platformConstants.PATH, 'TMP': self.platformConstants.TEMP }
        #self.Append(CFLAGS=self.platformConstants.LINKFLAGS)
        #self.Append(SHLLDFLAGS=self.platformConstants.LINKFLAGS)
        self.Append(CCFLAGS=self.platformConstants.CCFLAGS)
        

env = Env()
env.init()
env.Export('env')
env.SConscript(dirs=[os.path.join("filters", "src")])







