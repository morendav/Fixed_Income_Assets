# Bond_Schedule.py

Script used to calculate the schedule of payments for a fixed income financial instrument with a predetermined interest rate, maturity life term, and present and forecasted final value.

## Prerequisites

A number of python libraries are used in these scripts at different points. Please refer to the .py file for specific modules required by each script.
These are mostly from SciPy and commonly available in standard IDEs used in python development

In no specific order:
  + matplotlib
  + numpy
  + argpars


### Running the script

The schedule builder will accept a number of different bond repayment terms including:
  + Fully Amoritized
  + Bullet
  + Sinking Fund

  > NOTE: the script requires at least the schedule type to passed as parameter s
  > NOTE: the coupon rate must be passed as a decimal equivalent

Example Run:
```
 python3 ./Bond_Schedule.py -v 100 0 -c 0.06 -s "fullyAmoritized" -n 12 -y 15
```

In this example the schedule of payments will be forecast for a monthly compounding bond, over the life of 15 years.
with an annualized effective coupon rate of 6%
- Rd      6% - 7%
- Tc      30% - 40%
- Rdisc   6% - 8%



### Note regarding accuracy of schedule

The schedule builder uses a floating point precision of 3 decimal places to forecast payments. For the sake of visualization this seems to be sufficient.
If increased precision is required the precision can be set by updating the hardcoded value set in the beginning of the script like so:

First 30 lines of the script:
```
#######################################
# Create schedule of payments for a fixed income asset
#
# Options (parameters)
#       -v      Value array of present vs future value, integers
#       -c      Coupon rate percentage stated as an annualized decimal equivalent
#       -s      Schedule type, can be any of the following: (SinkingFund, fullyAmoritized, bullet)
#       -p      Payment amount against bond at the end of each period
#       -n      Number of Periods per year
#       -y      Number of years until maturity
#
# Example:
#       python3 ./Bond_Schedule.py -v 100 0 -c 0.06 -s "fullyAmoritized" -n 12 -y 15
#
#       Providing a schedule of payments for a fullyamoritized bond, with effective monthly compounding rate of 6%, over 15 years.
#           Bond Present Value = 100, Future value = 0
#           rate = 6% annualized rate
#
#######################################
###     CodeBlock: Modules & Init Variables
#######################################
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt


### Predefined varaibles & data sets
Accepted_ScheduleTypes = ["sinkingFund", "fullyAmoritized", "bullet"]
Accepted_precision = 3 #precision of floating decimals, number represents the number of digits after the decimal point
```

The variable set to "Accepted_precision = 3 "  <--- can be updated to reflect higher precision. Higher number = higher precision in calculations.


## Version

### V 1.01
  + parameters set up to take on some default values if not passed when called
  + iterative model to build out forecast
  + subplots of total payments & interest v principle payments over life
