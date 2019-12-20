"""
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
"""

import Queue
import ctypes
import os
import platform
import dll_loader
from biofeedProcessor import BioThreadedDataProcessor







FILTER_LOOKUP = { "test": 0,
              "null": 1,
              "average": 2,
              "emg": 3,
              "ecg": 4,
              "gsr": 5,
              "bpm": 6,
              "pulse": 7,
              "noise": 8}




#
#enum filterType{FT_TEST = 0, 
#                FT_NULL = 1, 
#                FT_AVERAGE = 2, 
#                FT_EMG = 3, 
#                FT_ECG = 4,
#                FT_GSR = 5};


class BioFilterManager(BioThreadedDataProcessor):
    """does nothing at the moment"""
    """will apply filters to the data and pass it on"""
    
    def __init__(self, dst):
        self.src = Queue.Queue()
        super(BioFilterManager, self).__init__(self.src, dst)
        self.channels = {}
        self.inputs = []


        
    def __str__(self):
        S = []
        for name, channel in self.channels.iteritems():
            S.append("channel: %s : %s\n" % (name, channel))
            
        for input in self.inputs:
            input.getStringOfTree(0, S)
            
        return "".join(S)
            
    def _getData(self):
        ## getting data from a Queue object
        try:
            return self.src.get(True, 3)
        except:
            print "not data in queue"
            #raise Exception, "failed to find data in BioFilterManager queue"
    
    def _putData(self, data):
        # a tuple of numeric values
        # into a realTimeDataExchange
        # this is a dict named by channel with indeterminate contents
        self.dst.put(data)
    
    
    def _transformData(self, dataIn):
        port, array = dataIn
        for input in self.inputs:
            if input.port == port:
                input.evaluate(float(array[input.ch]))
        dataOut = {}
        for name, channel in self.channels.iteritems():
            data = channel.getOutput()
            if not data is None:
                dataOut[name] = data
        ##not even every channel which go some new data will produce new data here
        return dataOut #null transforms for now
    
    
    def addChannel(self, name, port, ch, filterAddress):
        input = self.ensureInput(port, ch, filterAddress)
        filters = self.addFilters(input, filterAddress)
        self.channels[name] = FilterChannel(filters)
        #print self.channels.keys()
    
        
    def ensureInput(self, port, ch, filterAddress):
        input = None
        for inp in self.inputs:
            if port == inp.port and ch == inp.ch:
                input = inp
        if not input:
            input = InputFilter(port, ch)
            self.inputs.append(input)
        return input
        
        
    def addFilters(self, input, filterAddress):
        filters = [input,]
        parent = input
        found = False
        for name in filterAddress:
            parent, found = self.ensureFilter(name, parent)
            filters.append(parent)
        if found:
            raise Exception, "filterAddress already exists"
        return filters
            

    def ensureFilter(self, name, parent):
        filter = parent.getFilterNamed(name)
        found = True
        if not filter:
            filter = BioLinearFilter(name)
            parent.addChild(filter)
            found = False
        return filter, found
        
        
        
#import ctypes

#        link = ctypes.cdll.sugarlink
        #
        #link = ctypes.cdll.loadLibrary(dllpath)
#        self.getItemBell = link.getItemBell      
        


class FilterChannel(object):
    
    def __init__(self, filters):
        self.filters = filters
        
    def __str__(self):
        return "".join([str(filter) for filter in self.filters])
        
    def getOutput(self):
        return self.filters[-1].read()
    
    def getInputPortAndCh(self):
        return self.filters[0].port, self.filters[0].ch


class BioFilter(object):
    
    def __init__(self):
        self.children = {}
        self.output = 0.0
        self.fresh = False
        
    def getStringOfTree(self, depth, S):
        tabs = "".join(depth * ["\t"])
        S.append("%s%s\n" % (tabs, self))
        for name, child in self.children.iteritems():
            child.getStringOfTree(depth + 1, S)

    def addChild(self, child):
        if not child.name in self.children.keys():
            self.children[child.name] = child
        else:
            raise Exception, "this child filter already exists"
        
    def getFilterNamed(self, name):
        return self.children.get(name)
        
    def evaluate(self, value):
        self.output = value
        for name, child in self.children.iteritems():
            child.evaluate(value)
        self.fresh = True
        
    def read(self):
        if self.fresh:
            self.fresh = False
            return self.output
        else:
            return None
        
    
class BioLinearFilter(BioFilter):
    
    #process = ctypes.cdll.filters.process
    
    filterLib = dll_loader.getLib("filters")
    makeFilter = filterLib.makeFilter
    process = filterLib.process
    
    def __init__(self, name):
        super(BioLinearFilter, self).__init__()
        self.name = name
        typeInt = FILTER_LOOKUP[name]
        self.id = self.makeFilter(typeInt)
        print "id", self.id

        
    def __str__(self):
        return " -> %s" % self.name

    def evaluate(self, value):
        input = ctypes.c_double(value)
        output = ctypes.c_double()
        result = self.process(self.id, input, ctypes.byref(output))
        self.output = output.value
        for name, child in self.children.iteritems():
            child.evaluate(self.output)
        self.fresh = True
        
        
class InputFilter(BioFilter):
    
    def __init__(self, port, ch):
        super(InputFilter, self).__init__()
        self.port = port
        self.ch = ch
        
    def __str__(self):
        return "%s %s" % (self.port, self.ch)


class FilterInfo(object):
    
    def __init__(self, name, func, id=None):
        self.name = name
        self.func = func
        self.id = id
