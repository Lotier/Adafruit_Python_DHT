#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
#import Adafruit_DHT
import getopt

#defaults
scale="c"
feels=False
pin=4
sensor='11' 

def usage():
	print('usage: sudo ./Adafruit_DHT.py -t/--type=[11|22|2302] -p/--pin=GPIOpin# -s/--scale=[f|c] -f/--feels')
	print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
	
def checkSensor(type):
	global sensor
	if type in sensor_args:
		sensor = type
	else:
		print str("Unknown sensor type | {0}".format(a))
		usage()
		sys.exit(2)

# Parse command line parameters.
sensor_args = { '11': 'Adafruit_DHT.DHT11',
                '22': 'Adafruit_DHT.DHT22',
                '2302': 'Adafruit_DHT.AM2302' }              

try:
    opts, args = getopt.getopt(sys.argv[1:], "hft:p:s:", ["help", "feels", "type=", "pin=", "scale="])
except getopt.GetoptError as err:
	# print help information and exit:
    print str(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
   
for o, a in opts:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-t","--type"):
		checkSensor(a)
	elif o in ("-p","--pin"):
		pin = a
	elif o in ("-s","--scale"):
		if a in ("f", "c"):
			scale = a
		else:
			print str("Unknown scale type | {0}".format(a))
			usage()
			sys.exit(2)
	elif o in ("-f","--feels"):
		feels=True
		
if len(args) == 2:
	checkSensor(args[0])
	pin = args[1]

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, readingTemperature = 35, 92#= Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
if scale == "f":
	outputTemperature = readingTemperature * 9/5.0 + 32
else:
	outputTemperature = readingTemperature

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and readingTemperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(outputTemperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
    
if feels:
	#formula is for fahrenheit
	fahrenheit = readingTemperature * 9/5.0 + 32

	fahrenheitSquared = pow(fahrenheit, 2)
	fahrenheitCubed = pow(fahrenheit, 3)
	humiditySquared = pow(humidity, 2)
	humidityCubed = pow(humidity, 3)

	# Coefficients for the calculations
	constGroup1 = [ -42.379,       2.04901523,  10.14333127, 
                     -0.22475541, -6.83783e-03, -5.481717e-02, 
                      1.22874e-03, 8.5282e-04,  -1.99e-06]
	constGroup2 = [ 0.363445176,  0.988622465,  4.777114035, 
                   -0.114037667, -8.50208e-04, -2.0716198e-02, 
	                6.87678e-04,  2.74954e-04,  0]
	constGroup3 = [ 16.923,        0.185212,    5.37941,     -0.100254, 
                     9.41695e-03,  7.28898e-03, 3.45372e-04, -8.14971e-04, 
                     1.02102e-05, -3.8646e-05,  2.91583e-05,  1.42721e-06, 
                     1.97483e-07, -2.18429e-08, 8.43296e-10, -4.81975e-11]

	# Calculating heat-indexes with 3 different formula
	formula1 = constGroup1[0] + (constGroup1[1] * fahrenheit) + (constGroup1[2] * humidity) + (constGroup1[3] * fahrenheit * humidity) + (constGroup1[4] * fahrenheitSquared) + (constGroup1[5] * humiditySquared) + (constGroup1[6] * fahrenheitSquared * humidity) + (constGroup1[7] * fahrenheit * humiditySquared) + (constGroup1[8] * fahrenheitSquared * humiditySquared)
	formula2 = constGroup2[0] + (constGroup2[1] * fahrenheit) + (constGroup2[2] * humidity) + (constGroup2[3] * fahrenheit * humidity) + (constGroup2[4] * fahrenheitSquared) + (constGroup2[5] * humiditySquared) + (constGroup2[6] * fahrenheitSquared * humidity) + (constGroup2[7] * fahrenheit * humiditySquared) + (constGroup2[8] * fahrenheitSquared * humiditySquared)
	formula3 = constGroup3[0] + (constGroup3[1] * fahrenheit) + (constGroup3[2] * humidity) + (constGroup3[3] * fahrenheit * humidity) + (constGroup3[4] * fahrenheitSquared) + (constGroup3[5] * humiditySquared) + (constGroup3[6] * fahrenheitSquared * humidity) + (constGroup3[7] * fahrenheit * humiditySquared) + (constGroup3[8] * fahrenheitSquared * humiditySquared) + (constGroup3[9] * fahrenheitCubed) + (constGroup3[10] * humidityCubed) + (constGroup3[11] * fahrenheitCubed * humidity) + (constGroup3[12] * fahrenheit * humidityCubed) + (constGroup3[13] * fahrenheitCubed * humiditySquared) + (constGroup3[14] * fahrenheitSquared * humidityCubed) + (constGroup3[15] * fahrenheitCubed * humidityCubed)

	if scale == "c":
		formula1 = (formula1 - 32) * 5/9
		formula2 = (formula2 - 32) * 5/9
		formula3 = (formula3 - 32) * 5/9
	
	print("The Heat index is:")
	print("\tFormula 1: {0}".format(round(formula1, 1)))
	print("\tFormula 2: {0}".format(round(formula2, 1)))
	print("\tFormula 3: {0}".format(round(formula3, 1)))