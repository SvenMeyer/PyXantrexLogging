#!/usr/bin/python
import subprocess
import sys
from datetime import datetime

import xantrex_data
from pvoutput_config import StatusURL, OutputURL, APIKey, SystemID
from weather import min_temp, max_temp, forecast_text

# Save Date and Time into variables
date = datetime.now().strftime("%Y%m%d")
time = datetime.now().strftime("%H:%M")

try:
    if sys.argv[1] == "--live":

        AddStatus = (
                    '/usr/bin/curl -d "d=%s" -d "t=%s" -d "v1=%s" -d "v2=%s" -d "v5=%s" -d "v6=%s" -H "X-Pvoutput-Apikey:%s" -H "X-Pvoutput-SystemId:%s" --retry 2 %s' % (
            date, time, xantrex_data.KWHTODAY, xantrex_data.POUT, xantrex_data.MEASTEMP, xantrex_data.VOUT, APIKey,
            SystemID, StatusURL))
        subprocess.call(AddStatus, shell=True)
        print()

    elif sys.argv[1] == "--daily_summary":

        from daily_total import PeakPower, PeakTime

        AddOutput = (
                    'curl -d "d=%s" -d "g=%s" -d "pp=%s" -d "pt=%s" -H "X-Pvoutput-Apikey:%s" -H "X-Pvoutput-SystemId:%s" -d "tm=%s" -d "tx=%s" -d "cm=%s" --retry 2 %s' % (
            date, xantrex_data.KWHTODAY, PeakPower, PeakTime, APIKey, SystemID, min_temp, max_temp,
            "Updated " + time + ", " + forecast_text + ", Min: " + min_temp + "C, Max: " + max_temp + "C", OutputURL))
        subprocess.call(AddOutput, shell=True)
        print()

    else:
        print("Incorrect argument has been entered. The following arguments are accepted:")
        print()
        print("--daily_summary")
        print("--live")
        print()
        print("Please enter an accepted argument for this script to run correctly")

except IndexError:
    print("Script failed. Nothing has been run")
