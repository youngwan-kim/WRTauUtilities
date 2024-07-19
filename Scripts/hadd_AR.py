#!/usr/bin/python3
import os,argparse,glob
from itertools import product
from datetime import datetime

samplegroup = {}

samplegroup_noskim = {
    "VVV" : ["WWW_TauHLT","WWZ_TauHLT","WZZ_TauHLT","ZZZ_TauHLT"],
    "VV" : ["WW_TauHLT","WZ_TauHLT","ZZ_TauHLT"],
    "ST" : [],
    "TT" : [],
}


samplegroup_skim = {
    "VVV" : ["WWW*","WWZ*","WZZ*","ZZZ*"],
    "VV" : ["WW_*","WZ_*","ZZ_*"],
    "ST" : ["SingleTop*","ST*"],
    "TT" : ["TT*"],
}

signals = {
    2000 : [200,1900],
    4000 : [200,3900],
    4800 : [200,4700]
}

signals = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [100,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

l_lep = ['NonpromptLepton','PromptLepton']
l_tau = ['NonpromptTau','PromptTau']

combinations = product(l_lep, l_tau)
nonprompts = [f"{A}__{B}__" for A, B in combinations if not (A == 'PromptLepton' and B == 'PromptTau')]

def GetTMPDir() :
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def GetSKOutDir(analyzername,era) : 
    return f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/{analyzername}/{era}"

def HADDnGet(analyzername,era,flag,outdir,skim,onlysignals) :

    if era == "2017" or "2016" in era : samplegroup_skim["ST"] = ["SingleTop*"]
    elif era == "2018" : samplegroup_skim["ST"] = ["ST*"]

    hasSkim = skim is not ''

    if not flag == '' : 
        flagstr = f"{flag}__"
        outdir = f"{outdir}__{flag}"
    else : flagstr = flag
        
    os.system(f"mkdir -p ../RootFiles/{outdir}/{era}/DATA")
    os.system(f"mkdir -p ../RootFiles/{outdir}/{era}/Signals")
    os.system(f"mkdir -p ../RootFiles/{outdir}/{era}/AR/DATA")

    hadddir = f"{GetSKOutDir(analyzername,era)}/{flagstr}"

    basename = analyzername
    if hasSkim : 
        analyzername = basename + "_SkimTree_" + skim
        samplegroup = samplegroup_skim
    else : samplegroup = samplegroup_noskim

    #Data
    os.system(f"hadd ../RootFiles/{outdir}/{era}/AR/DATA/{basename}_DATA.root {GetSKOutDir(basename,era)}/RunApplicationRegion__/DATA/{analyzername}_Tau*")
    # Prompt HADD
    for sample in samplegroup :
        if len(samplegroup[sample]) > 0 :
            haddstr = ""
            haddstr_AR = ""
            for name in samplegroup[sample] :
                haddstr_AR += f"{hadddir}/RunApplicationRegion__/{analyzername}_{name}.root " 
            os.system(f"hadd ../RootFiles/{outdir}/{era}/AR/{basename}_{sample}.root {haddstr_AR}")

        else : 
            os.system(f"hadd ../RootFiles/{outdir}/{era}/AR/{basename}_{sample}.root {hadddir}/RunApplicationRegion__/{analyzername}_{sample}*Tau*")


    os.system(f"hadd ../RootFiles/{outdir}/{era}/AR/{basename}_Prompt.root ../RootFiles/{outdir}/{era}/AR/{basename}_*.root ")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hadd output files from WRTauAnalyzer')
    parser.add_argument('--flag'  , type=str , help='Additional flag used' , default = '' ) 
    parser.add_argument('--outdir', type=str , help='Output dir'           , default = GetTMPDir() )
    parser.add_argument('--era'   , type=str , help='Era')
    parser.add_argument('--skim'  , type=str , help='Skim name i.e Name if SkimTree_Name' , default = '' )
    parser.add_argument('--analyzername', type=str , help='Analyzer name'  , default = 'WRTau_Analyzer' )
    parser.add_argument('--onlysignals',action='store_true', help='Move only signals' )
    args = parser.parse_args()

    HADDnGet(args.analyzername,args.era,args.flag,args.outdir,args.skim,args.onlysignals)
