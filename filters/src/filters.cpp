/*
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
*/



#ifdef WIN32
#define EXPORTED_FROM_CPP extern "C" __declspec(dllexport)
#else
#define EXPORTED_FROM_CPP extern "C" __attribute__((visibility("default")))
#endif

#include "filterFactory.h"

static CFilterFactory factory;


EXPORTED_FROM_CPP int test(int input)
{
   	
	int result = 67;

	return result;
}


EXPORTED_FROM_CPP int makeFilter(int input)
{
   	return factory.makeFilter((filterType)input);
}


EXPORTED_FROM_CPP int process(int id, double input, double* output)
{
	*output = factory.process(id, input);
	return 55;
}


