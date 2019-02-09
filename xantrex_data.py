#!/usr/bin/python

import serial
import os
from datetime import datetime, date, time

# dir_path = os.path.dirname(os.path.abspath(__file__))
# dir_path = os.path.abspath("~/solardata")
dir_path = os.path.abspath("/home/pi/solardata/")
print(("dir_path = ", dir_path))

#Save Date and Time into variables
date_now = datetime.now().strftime("%Y-%m-%d")
time_now = datetime.now().strftime("%H:%M:%S")

#Create serial connection
s = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)

#List of commands to send to the inverter
queries = (
  "IDN",      # inverter ID must come first
  "IIN",
  "KWHTODAY",
  "KWHLIFE",
  "PIN",
  "POUT",
  "TIME",
  "MEASTEMP",
  "DERATELIMIT",
  "TEMPLIMIT",
  "VIN",
  "VOUT",
)

# function that extracts temp in degrees celsius from MEASTEMP
def extract_between(text, sub1, sub2, nth=1):
	if sub2 not in text.split(sub1, nth)[-1]:
		return None
	return text.split(sub1, nth)[-1].split(sub2, nth)[0]

# utility function that reads a socket until a \r
def myreadline(s):
  res = ""
  while 1:
    c = s.read()
    # convert byte to UTF8
    u = c.decode()
    if (u == '\r'): return res
    res += u

for query in queries:
  # encode to bytes before sending over serial
  s.write(str.encode(query + "?\r"))
  response = myreadline(s)
  exec('%s=response' % query)
      
#Modify some of the returned values to get what we want to upload.
MEASTEMP = extract_between(MEASTEMP,':',' ')
KWHTODAY = '{0:g}'.format(float(KWHTODAY)*1000)

daily_file = open(os.path.join(dir_path, "CumbalumXantrex_" + date_now + ".tsv"),"a+")

daily_file.write(date_now + '\t')
daily_file.write(time_now + '\t')
daily_file.write(VIN  + '\t')
daily_file.write(IIN      + '\t')
daily_file.write(PIN  + '\t')
daily_file.write(VOUT + '\t')
daily_file.write(POUT + '\t')
daily_file.write(KWHTODAY + '\t')
daily_file.write(KWHLIFE  + '\t')
daily_file.write(TIME + '\t')
daily_file.write(MEASTEMP +    '\t')
daily_file.write(DERATELIMIT + '\t')
daily_file.write(TEMPLIMIT +   '\n')



daily_file.close()

# #Get Inverter Efficiency
# try:
#   EFFICIENCY = (int(POUT) / int(PIN))*100
#   EFFICIENCY = int(EFFICIENCY)

# except ZeroDivisionError:
#   EFFICIENCY = int(0)

# Write Max Power to log file, only if date or Power value is higher
file = open(os.path.join(dir_path, "MaxPower.txt"),"r")
line = file.readline()
line_split = line.split(",")
power = line_split[0]
aDate = line_split[1]
aTime = line_split[2]
file.close

if int(POUT) > int(power) or date_now > aDate:
	file = open(os.path.join(dir_path, "MaxPower.txt"),"w")
	file.write(POUT + "," + date_now + "," + time_now)

file.close