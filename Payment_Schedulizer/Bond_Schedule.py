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

#######################################
###     CodeBlock: Pass Parameters
#######################################
### Read passed arguements from the command line
parser = ArgumentParser(
    description='develop schedule of payments and relevant metrics for a bond over its life time until maturity',
    epilog="Example:\r python3 ./Bond_Schedule.py -v 100 0 -c 0.06 -s "fullyAmoritized" -n 12 -y 15")
parser.add_argument("-v", "--Value_Array", dest="vArray", help="Value array representing initial and final values, space delimited format: PV FV", nargs="+", default=[100,0], metavar="min max", type=float)
parser.add_argument("-c", "--couponRate", dest="cRate", help="Annualized effective interest/coupon rate stated as a decimal", default=0.03, metavar="interest", type=float)
parser.add_argument("-s", "--ScheduleType", dest="schType", help="Type of Schedule terms of the bond. Values accepted are = [sinkingFund, fullyAmoritized, bullet]",  default='bullet', metavar="ScheduleType", type=str)
# parser.add_argument("-p", "--paymentAmount", dest="payment", help="If there is a set value for the payment then this value should be defined as the set payment", metavar="Payment", type=int)
parser.add_argument("-n", "--numberPeriods", dest="nper", help="number of payment periods per year",  default=1, metavar="nper", type=int)
parser.add_argument("-y", "--yearsToMaturity", dest="years", help="number of years until maturity",  default=15, metavar="years", type=int)
### Parse the parameters
args = parser.parse_args()
valueBound=args.vArray
scheduleType=args.schType
ppy=args.nper
total_Periods = args.years * ppy
effective_periodRate=args.cRate/ppy


### Check if initial conditions are met
if scheduleType not in Accepted_ScheduleTypes:
    print("Unsupported schedule type.\nuse -h option for help calling this script")
    exit()

### Set up initial arrays of empty Values
t_array = np.linspace(1,total_Periods,total_Periods)            # array of time periods
p_array = np.linspace(1,total_Periods,total_Periods)            # array of total payments made to bond servicer
paidArray_Interest  = np.repeat(0,total_Periods)                # array of interest per period
paidArray_Principle = np.repeat(0,total_Periods)                # array of principle paid per period
Balance_Principle   =  np.repeat(valueBound[0],total_Periods)               # array of principle balance

### Set up initial arrays of empty Values
t_array = np.linspace(1,total_Periods,total_Periods)            # array of time periods
p_array = [0] * total_Periods
paidArray_Interest  = [0] * total_Periods               # array of interest per period
paidArray_Principle = [0] * total_Periods               # array of principle paid per period
Balance_Principle   = [valueBound[0]] * total_Periods               # array of principle balance



#######################################
###     Financial Calculations - Schedule Building
#######################################
if scheduleType in ['fullyAmoritized']:
    # all payments are equal level. predefined by maturity and coupone rate
    amoritizing_payment = -1 * np.pmt (effective_periodRate,total_Periods, valueBound[0], valueBound[1])
    p_array = [round(amoritizing_payment,Accepted_precision)] *  total_Periods

    ### Period calculations, iterate over whole maturity of bond
    for i in range(len(t_array)-1):
        paidArray_Interest[i] = round(Balance_Principle[i] * effective_periodRate, Accepted_precision)
        paidArray_Principle[i] = round( p_array[i] - paidArray_Interest[i], Accepted_precision)
        Balance_Principle[i+1] = round( Balance_Principle[i] - paidArray_Principle[i], Accepted_precision)
    ### Final Period calcualtion
    paidArray_Interest[i+1] = round(Balance_Principle[i+1] * effective_periodRate, Accepted_precision)
    paidArray_Principle[i+1] = p_array[i+1] - paidArray_Interest[i]

elif scheduleType in ['bullet']:
    # Principle paid each period is 0, principle balance is left static as Present Value at start of loan
    paidArray_Principle = [0] * total_Periods

    ### Period calculations, iterate over whole maturity of bond
    for i in range(len(t_array)-1):
        paidArray_Interest[i] = round(Balance_Principle[i] * effective_periodRate, Accepted_precision)
    ### Final Period calcualtion
    paidArray_Interest[i+1] = round(Balance_Principle[i+1] * effective_periodRate, Accepted_precision)
    p_array = paidArray_Interest
    #add final bullet payment to payment array
    p_array[i+1] = paidArray_Interest[i+1] + Balance_Principle[i+1]
elif args.payment is None and scheduleType is ['sinkingFund']:
    print("Sinking fund schedule type requires a predetermined payment amount. Use -h for help calling script")
    exit()



#######################################
###     Financial Analysis
#######################################

#Creates two subplots and unpacks the output array immediately
f, (fig1, fig2) = plt.subplots(1, 2, sharey=True)
fig1.stem(t_array, p_array,'b', markerfmt='b-',label='Total PMT')
fig1.stem(t_array, paidArray_Principle,'g', markerfmt='g-', label='Principle PMT')
fig1.set_title('Payments made each Period')
fig1.set_xlabel('Periods in bond term')
fig1.set_ylabel('$ Dollars')
fig1.legend(loc='upper left', fancybox=True, shadow=True)
fig1.grid(which='both', axis='both', color='r', linestyle=':', linewidth=0.5)

fig2.plot(t_array,paidArray_Principle,'g-', label='Principle Schedule')
fig2.plot(t_array,paidArray_Interest,'b-', label='Interest Schedule')
fig2.set_title('Payments by Type')
fig2.set_xlabel('Periods in bond term')
fig2.legend(loc='upper center', fancybox=True, shadow=True)
fig2.grid(which='both', axis='both', color='r', linestyle=':', linewidth=0.5)
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
