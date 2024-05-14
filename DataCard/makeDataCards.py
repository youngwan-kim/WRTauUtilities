import os
from utils import *
'''
d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}'''

d_lumi = {
    "2016" : 0.012,
    "2016preVFP" : 0.012,
    "2016postVFP" : 0.012,
    "2017" : 0.023,
    "2018" : 0.025,
    "Run2" : 0.016
}

for era in ["2016","Run2"] :
    os.system(f"mkdir -p Cards/{era}")
    for mwr in d_mass :
        for mn in d_mass[mwr] :
            os.system(f"cp LRSMSkeleton.txt Cards/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##ERA##/{era}/g' Cards/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##lumi##/{d_lumi[era]}/g' Cards/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##mwr##/{mwr}/g' Cards/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##mn##/{mn}/g' Cards/{era}/card_WR{mwr}_N{mn}.txt")