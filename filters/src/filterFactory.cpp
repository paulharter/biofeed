/*
Biofeed - An Open Source Python Physiological Monitoring project
Author: Paul Harter
Contact: paul@cleverplugs.com
Copyright: Clever Plugs Ltd 2009
Licence: Python License - http://www.python.org/psf/license/
*/




#include "filterFactory.h"


int CFilterFactory::makeFilter(filterType type)
{
	CFilter* pFilter = 0;
	if(type == FT_TEST)		pFilter = (CFilter*)new CFilter_test();
	if(type == FT_AVERAGE)	pFilter = (CFilter*)new CFilter_average();
	if(type == FT_NULL)		pFilter = (CFilter*)new CFilter_null();
	if(type == FT_EMG)		pFilter = (CFilter*)new CFilter_EMG();
	if(type == FT_ECG)		pFilter = (CFilter*)new CFilter_ECG();
	if(type == FT_GSR)		pFilter = (CFilter*)new CFilter_GSR();
	if(type == FT_BPM)		pFilter = (CFilter*)new CFilter_bpm();
	if(type == FT_PUL)		pFilter = (CFilter*)new CFilter_pulse();
	if(type == FT_NOISE)	pFilter = (CFilter*)new CFilter_noise();
	filters.push_back(pFilter);
	return filters.size() - 1;
}
void CFilterFactory::clearAllFilters()
{


}



double CFilter_average::process(double input)
{ 
//printf("average in %f\n", input);
	xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5];
	xv[5] = input;
	return (xv[0] + xv[1] + xv[2] + xv[3] + xv[4] + xv[5]) / 6.0;
}



/*
EMG
1. Butterworth Bandpass
2. blank
3. 4
4. 256
5. 30, 128
6. blank
7. blank
8. blank
*/



double CFilter_EMG::process(double input)
{
	double result = bandpass(fabs(input - 512.0));
	if(result < 0.0)result = 0.0;
	return result;
}

double CFilter_EMG::bandpass(double input)
{ 
	xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; 
	xv[8] = input/2.783712976;
	yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; 
	yv[8] =   (xv[0] + xv[8]) - 4 * (xv[2] + xv[6]) + 6 * xv[4]
				 + ( -0.1291302835 * yv[0]) + (  0.2373236445 * yv[1])
				 + (  0.5188044618 * yv[2]) + ( -1.0922924416 * yv[3])
				 + ( -0.9388583822 * yv[4]) + (  1.6650807823 * yv[5])
				 + (  0.5116173874 * yv[6]) + ( -1.8476766755 * yv[7]);
	return yv[8];
}



/*
ECG (2 filters)
1. Butterworth Bandstop
2. blank
3. 3
4. 256
5. 55, 65
6. blank
7. blank
8. blank
*/

/*
1. Butterworth Lowpass
2. blank
3. 10
4. 256
5. 80, blank
6. blank
7. blank
8. blank
*/


double CFilter_ECG::process(double input)
{
	return lowpass(bandstop(input));
}

double CFilter_ECG::bandstop(double input)
{
	xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; 
    xv[6] = input/1.278977374e+00;
    yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; 
    yv[6] =   (xv[0] + xv[6]) -   0.5925591627 * (xv[1] + xv[5]) + 3.1170421204 * (xv[2] + xv[4])
                 -   1.1928243676 * xv[3]
                 + ( -0.6113258325 * yv[0]) + (  0.3918143538 * yv[1])
                 + ( -2.2173542717 * yv[2]) + (  0.9232418481 * yv[3])
                 + ( -2.6093417154 * yv[4]) + (  0.5441969336 * yv[5]);
    return yv[6];

}

double CFilter_ECG::lowpass(double input)
{
	xv2[0] = xv2[1]; xv2[1] = xv2[2]; xv2[2] = xv2[3]; xv2[3] = xv2[4]; xv2[4] = xv2[5]; xv2[5] = xv2[6]; xv2[6] = xv2[7]; xv2[7] = xv2[8]; xv2[8] = xv2[9]; xv2[9] = xv2[10]; 
    xv2[10] = input/5.930023404e+01;
    yv2[0] = yv2[1]; yv2[1] = yv2[2]; yv2[2] = yv2[3]; yv2[3] = yv2[4]; yv2[4] = yv2[5]; yv2[5] = yv2[6]; yv2[6] = yv2[7]; yv2[7] = yv2[8]; yv2[8] = yv2[9]; yv2[9] = yv2[10]; 
    yv2[10] =   (xv2[0] + xv2[10]) + 10 * (xv2[1] + xv2[9]) + 45 * (xv2[2] + xv2[8])
                 + 120 * (xv2[3] + xv2[7]) + 210 * (xv2[4] + xv2[6]) + 252 * xv2[5]
                 + ( -0.0002844617 * yv2[0]) + ( -0.0049771031 * yv2[1])
                 + ( -0.0405221084 * yv2[2]) + ( -0.2022430888 * yv2[3])
                 + ( -0.6925140485 * yv2[4]) + ( -1.6989861021 * yv2[5])
                 + ( -3.0871002799 * yv2[6]) + ( -4.0838144887 * yv2[7])
                 + ( -3.9667670135 * yv2[8]) + ( -2.4908513158 * yv2[9]);
    return yv2[10];
}




double CFilter_bpm::process(double input)
{
		//too crude doesn't really work at all!
		xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6];
		xv[6] = input;

		if (xv[0] < xv[1] && xv[1] <= xv[2] && xv[2] <= xv[3] && xv[3] >= xv[4] && xv[4] >= xv[5] && xv[5] > xv[6]
			&& xv[3] > lastMax * 0.7)
		{
			lastMax = xv[3];
			intervals[0] = intervals[1];
			intervals[1] = intervals[2];
			intervals[2] = sinceLast + 1;
			sinceLast = 0;
		}
		else
		{
			sinceLast++;
		}

		return (intervals[0] + intervals[1] + intervals[2])/3.0;
}


double CFilter_pulse::process(double input)
{
		//normalises the top half of the signal to 0-1 for controlling flashing pulse indicator

		xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6];
		xv[6] = input;

		if (xv[0] < xv[1] && xv[1] <= xv[2] && xv[2] <= xv[3] && xv[3] >= xv[4] && xv[4] >= xv[5] && xv[5] > xv[6]
			&& xv[3] > max * 0.7)
		{
			max = xv[3];
		}

		if (xv[0] > xv[1] && xv[1] >= xv[2] && xv[2] >= xv[3] && xv[3] <= xv[4] && xv[4] <= xv[5] && xv[5] < xv[6]
			&& xv[3] < min * 1.2)
		{
			min = xv[3];
		}

		double v = (((input - min)/(max-min)) - 0.5) * 2.0;
		
		return v < 0 ? 0 : v;
}









/*
GSR
1. Bessel Lowpass
2. blank
3. 5
4. 256
5. 3, blank
6. blank
7. blank
8. blank
*/


double CFilter_GSR::process(double input)
{
	//printf("gsr input %f\n", input);
	double filtered = chasingThreshold(lowpass(input));
	//printf("gsr filtered %f\n", filtered);
	return filtered;

}
double CFilter_GSR::chasingThreshold(double input)
{
	int i;
	double sum1 = 0;
	double sum2 = 0;

	for(i = 0; i < 20; i++)
	{
		av[i] = av[i+1];
		sum1 += av[i];
	}

	for(i = 20; i < 39; i++)
	{
		av[i] = av[i+1];
		sum2 += av[i];
	}

	sum2 += input;
	av[39] = input;

	double result = sum2 - sum1;
	if(result < 0.0) return 0.0;

	return result;
}

double CFilter_GSR::lowpass(double input)
{
	xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; 
    xv[5] = input/1.648922999e+06;
    yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; 
    yv[5] =   (xv[0] + xv[5]) + 5 * (xv[1] + xv[4]) + 10 * (xv[2] + xv[3])
                 + (  0.6344519043 * yv[0]) + ( -3.4650204658 * yv[1])
                 + (  7.5796043901 * yv[2]) + ( -8.3013446171 * yv[3])
                 + (  4.5522893820 * yv[4]);
    return yv[5];
}



double CFilter_noise::process(double input)
{
	//clips the top and bottom of the signal to catch some types of noise
	double out = input;
	if(input > 980.0 || input < 50)out = last;
	last = out;
	return out;

}
