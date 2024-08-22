import os, argparse 
from utils import *

input_path = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Workspaces"
parser = argparse.ArgumentParser(description='')
parser.add_argument('-e', dest='l_era', nargs="+")
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
args = parser.parse_args()


for era in args.l_era :
    for mwr in d_mass :
        for mn in d_mass[mwr]:
            os.system(f"mkdir -p FitDiagnostics/{args.tag}/{era}/WR{mwr}_N{mn}/")
            os.chdir(f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/FitDiagnostics/{args.tag}/{era}/WR{mwr}_N{mn}/")
            os.system(f"combine -M FitDiagnostics {input_path}/{args.tag}/{era}/card_WR{mwr}_N{mn}.root  --saveShapes --saveWithUncertainties --plots")
            os.chdir("/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/")