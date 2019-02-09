#!/usr/bin/python



#Declare PVOutput URL's, ID and System Key
PVOutputURL = "http://pvoutput.org"
StatusURL = PVOutputURL + "/service/r2/addstatus.jsp"
OutputURL = PVOutputURL + "/service/r2/addoutput.jsp"
APIKey   = "###_insert-your-API-key-here_###"
SystemID = "#####"

#API and System ID can be found on the PVOutput account page - http://pvoutput.org/account.jsp 

# Directory for data log files

import os

DATA_DIR = os.path.abspath("/home/pi/solardata/")
