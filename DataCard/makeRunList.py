from utils import *
import argparse

input_path = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Workspaces"
parser = argparse.ArgumentParser(description='')
parser.add_argument('-e', dest='l_era', nargs="+")
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
args = parser.parse_args()

with open("RunList_"+args.tag+".txt",'w') as f:
    for era in args.l_era :
        for mwr in d_mass :
            for mn in d_mass[mwr]:
                card = f"{input_path}/{args.tag}/{era}/card_WR{mwr}_N{mn}.root\n"
                f.write(card)
