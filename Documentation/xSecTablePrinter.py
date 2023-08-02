import os
from math import ceil,log10


with open("../data/xsec.csv") as xsec :
    for line in xsec :
        mWR = float(line.split(",")[0])
        mN = float(line.split(",")[1])
        xsec = float(line.split(",")[2])
        xsec_power = int(ceil(log10(xsec)))
        
        xsec_powerprint = "{"+str(xsec_power)+"}"

        xsec_power_printv = [f"\\times10^{xsec_powerprint}",""][xsec_power  0]
        xsec_div = xsec/pow(10.,xsec_power)
        k_factor = 1.
        print(f"WRTau\_WR{int(mWR)}\_N{int(mN)} & ${xsec_div:.2f}{xsec_power_printv}$ & {k_factor} \\\\")

