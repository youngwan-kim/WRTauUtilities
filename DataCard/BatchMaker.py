# Place it at CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter
# python create-batch.py -l RunList1.txt [RunList2.txt] --Asymptotic[--Full][--Q*]
# RunList.txt contains paths of results from text2workspace.py e.g. /data6/Users/jihkim/CombineTool/CMSSW_10_2_13/src/DataCardsShape/HNL_SignalRegionPlotter/Workspace/card_2017_MuMu_M500_HNL_UL.root

import os, sys
import commands as cmd
import argparse
import datetime

parser = argparse.ArgumentParser(description='option')
parser.add_argument('-l', dest='RunLists', nargs='+') # take args as a list, return error when there is no arg
parser.add_argument('--Full', action='store_true')
parser.add_argument('-t', dest='Ntoy', default='1000', help='N of toys when running full CLs')
parser.add_argument('--Asymptotic', action='store_true')
args = parser.parse_args()

pwd = os.getcwd()
CMSSW_BASE = os.environ['CMSSW_BASE']
SCRAM_ARCH = os.environ['SCRAM_ARCH']

failure, result = cmd.getstatusoutput('combine --help')
if failure:
    print "[!!ERROR!!] cannot run combine."
    print "Please set proper cmsenv first."
    print "Exiting ..."
    sys.exit(1)

for RunList in args.RunLists:
    cards = open(RunList).readlines()
    NCARD = len(cards)
    WP = RunList.split('.')[-2].replace('RunList_','')


    os.system('mkdir -p Batch/'+WP)
    with open('Batch/submit_skeleton.sh','w') as skel:
        skel.write("universe = vanilla\n")
        skel.write("getenv   = True\n")
        skel.write("should_transfer_files = YES\n")
        skel.write("when_to_transfer_output = ON_EXIT\n")
        skel.write("request_memory = 24000\n")
  
    for i in range(0,NCARD):
  
        card = cards[i].strip('\n')
        era = card.split('/')[-2]
        os.system('mkdir -p Batch/'+WP+'/'+era)
        if '#' in card: continue
        shortcard = card.split('/')[-1].replace(".root","").replace("card_","")
  
        os.system('mkdir -p Batch/'+WP+"/"+era+'/Asymptotic/'+shortcard+'/output/')
        os.system('cp Batch/submit_skeleton.sh Batch/'+WP+"/"+era+'/Asymptotic/'+shortcard+'/submit.sh')

        if args.Asymptotic:
            with open("Batch/"+WP+"/"+era+"/Asymptotic/"+shortcard+"/run_Asymptotic.sh",'w') as runfile:
                runfile.write("#!/bin/bash\n")
                runfile.write("combine -M AsymptoticLimits "+card+" --run blind\n")
            with open("Batch/"+WP+"/"+era+"/Asymptotic/"+shortcard+"/submit.sh",'a') as submitfile:
                submitfile.write("executable = run_Asymptotic.sh\n")
                submitfile.write("log = "+shortcard+"_Asymptotic.log\n")
                submitfile.write("output = "+shortcard+"_Asymptotic.out\n")
                submitfile.write("error = "+shortcard+"_Asymptotic.err\n")
                submitfile.write("transfer_output_files = higgsCombineTest.AsymptoticLimits.mH120.root\n")
                submitfile.write("transfer_output_remaps = \"higgsCombineTest.AsymptoticLimits.mH120.root = output/"+shortcard+"_Asymptotic.root\"\n")
                submitfile.write("queue\n")
            os.chdir('Batch/'+WP+"/"+era+'/Asymptotic/'+shortcard)
            os.system('chmod +x run_Asymptotic.sh')
            os.system('condor_submit submit.sh -batch-name '+shortcard+'_'+WP+'_Asymptotic'+'_'+era)
            os.chdir(pwd)