# Place it at CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter
# python create-batch.py -l RunList1.txt [RunList2.txt] --Asymptotic[--Full][--Q*]
# RunList.txt contains paths of results from text2workspace.py e.g. /data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/Workspace/card_2017_MuMu_M500_HNL_UL.root

import os, sys
#import commands as cmd
import argparse
import datetime
from utils import *

parser = argparse.ArgumentParser(description='option')
parser.add_argument('-t', dest='tag', default='240903')
args = parser.parse_args()

pwd = os.getcwd()
CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']

WP = args.tag

#failure, result = cmd.getstatusoutput('combine --help')
#if failure:
#    print("[!!ERROR!!] cannot run combine.")
#    print("Please set proper cmsenv first.")
#    print("Exiting ...")
#    sys.exit(1)

for era in ["2018"] :
    d_mass_ = d_mass 
    if era == "2018" : d_mass_ = d_mass_2018
    os.system(f"mkdir -p Workspaces/{args.tag}/{era}")
    with open('Workspaces/submit_skeleton.sh','w') as skel:
        skel.write("universe = vanilla\n")
        skel.write("getenv   = True\n")
        skel.write("should_transfer_files = YES\n")
        skel.write("when_to_transfer_output = ON_EXIT\n")
        skel.write("request_memory = 24000\n")
    for mwr in d_mass_ :
        for mn in d_mass_[mwr] :
            shortcard = "WR"+str(mwr)+"_N"+str(mn)
            os.system('cp Workspaces/submit_skeleton.sh Workspaces/'+WP+"/"+era+'/submit_'+shortcard+'.sh')
            with open("Workspaces/"+WP+"/"+era+"/run_"+shortcard+".sh",'w') as runfile:
                runfile.write("#!/bin/bash\n")
                runfile.write(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel /data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt -o card_WR{mwr}_N{mn}.root \n")
            with open("Workspaces/"+WP+"/"+era+"/submit_"+shortcard+".sh",'a') as submitfile:
                submitfile.write("executable = run_"+shortcard+".sh\n")
                submitfile.write("log = card_"+shortcard+".log\n")
                submitfile.write("output = card_"+shortcard+".out\n")
                submitfile.write("error = card_"+shortcard+".err\n")
                submitfile.write("transfer_output_files = card_"+shortcard+".root\n")
                #submitfile.write("transfer_output_remaps = \"card_"+shortcard+".root = card_"+shortcard+".root\"\n")
                submitfile.write("queue\n")
            os.chdir('Workspaces/'+WP+"/"+era)
            os.system('chmod +x run_'+shortcard+'.sh')
            os.system('condor_submit submit_'+shortcard+'.sh -batch-name '+shortcard+'_'+WP+'_WorkspaceMaker'+'_'+era)
            os.chdir(pwd)

