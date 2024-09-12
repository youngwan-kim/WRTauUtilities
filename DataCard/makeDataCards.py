import os, argparse
from utils import *
'''
d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}'''

d_lumi = {
    "2016" : 1.012,
    "2016preVFP" : 1.012,
    "2016postVFP" : 1.012,
    "2017" : 1.023,
    "2018" : 1.025,
    "Run2" : 1.016
}

parser = argparse.ArgumentParser(description='')
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
parser.add_argument('--no-scaleSignals', action='store_true')
args = parser.parse_args()

noscaling = args.no_scaleSignals
if noscaling :
    args.tag += "_noScale"

d_mass_ = d_mass

for era in ["2018"] :
    if era == "2018" : d_mass_ = d_mass_2018
    os.system(f"mkdir -p Cards/{args.tag}/{era}")
    for mwr in d_mass_ :
        for mn in d_mass_[mwr] :
            #PDFUnc = GetPDFUnc(mwr,mn,args.tag,era)
            #if PDFUnc != "-"  : PDFUnc = PDFUnc/100.+1.0
            #print(mwr,mn,PDFUnc)
            os.system(f"cp cardTemplate.txt Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##TAG##/{args.tag}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##ERA##/{era}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##lumi##/{d_lumi[era]}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##mwr##/{mwr}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            os.system(f"sed -i 's/##mn##/{mn}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            #os.system(f"sed -i 's/##PDF##/{PDFUnc}/g' Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt")
            print(f"{mwr},{mn} done ")