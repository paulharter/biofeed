/*
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
*/



#ifndef FILTERFACTORY_H
#define FILTERFACTORY_H


#include  <stddef.h>
#include <vector>
#include <stdlib.h>
#include <math.h>
using namespace std;


enum filterType{FT_TEST = 0, 
				FT_NULL = 1, 
				FT_AVERAGE = 2, 
				FT_EMG = 3, 
				FT_ECG = 4,
				FT_GSR = 5,
				FT_BPM = 6,
				FT_PUL = 7,
				FT_NOISE = 8};


class CFilter
{
public:
	CFilter(){}
	~CFilter(){}

	virtual double process(double input){return 16.0;}

};


class CFilter_test:CFilter
{
public:
	CFilter_test(){}
	~CFilter_test(){}
	
	double process(double input){return 44.6;}
};


class CFilter_null:CFilter
{
public:
	CFilter_null(){}
	~CFilter_null(){}

	double process(double input){return input;}
};


class CFilter_average:CFilter
{
public:
	CFilter_average(){}
	~CFilter_average(){}

	double process(double input);

	private:
		double xv[6];
};


class CFilter_EMG:CFilter
{
public:
	CFilter_EMG()
	{
	int i;
		for(i=0; i < 9; i++)
		{
			xv[i] = 512.0;
			yv[i] = 512.0;
		}


	}
	~CFilter_EMG(){}

	double process(double input);
	double bandpass(double input);

	private:
		double xv[9];
		double yv[9];

};

class CFilter_ECG:CFilter
{
public:
	CFilter_ECG()
	{
		int i;
		for(i=0; i < 7; i++)
		{
			xv[i] = 512.0;
			yv[i] = 512.0;
		}

		for(i=0; i < 11; i++)
		{
			xv2[i] = 512.0;
			yv2[i] = 512.0;
		}
	}
	~CFilter_ECG(){}

	double process(double input);

	private:
		double bandstop(double input);
		double lowpass(double input);
		double xv[7];
		double yv[7];
		double xv2[11];
		double yv2[11];
};

class CFilter_GSR:CFilter
{
public:
	CFilter_GSR(){}
	~CFilter_GSR(){}

	double process(double input);
	double lowpass(double input);
	double chasingThreshold(double input);

	private:
		double xv[6];
		double yv[6];
		double av[40];
};

class CFilter_bpm:CFilter
{
public:
	CFilter_bpm(){lastMax = 0.0;}
	~CFilter_bpm(){}

	double process(double input);

	private:
		double xv[7];
		int intervals[3];
		int sinceLast;
		double lastMax;
};

class CFilter_pulse:CFilter
{
public:
	CFilter_pulse(){max = 0.0; min = 0.0;}
	~CFilter_pulse(){}

	double process(double input);

	private:
		double xv[7];
		double max;
		double min;
};

class CFilter_noise:CFilter
{
public:
	CFilter_noise(){last = 0.0;}
	~CFilter_noise(){}

	double process(double input);

	private:
		double last;
};

class CFilterFactory
{
public:
	CFilterFactory(){}
	~CFilterFactory(){}

	int makeFilter(filterType type);
	double process(int id, double input){

		return filters[id]->process(input);
	}
	void clearAllFilters();

private:
	std::vector<CFilter*> filters;
};

#endif // FILTERFACTORY_H


