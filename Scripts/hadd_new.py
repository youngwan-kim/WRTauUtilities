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
    "QCD" : [],
}


samplegroup_skim = {
    "VVV" : ["WWW","WWZ","WZZ","ZZZ"],
    "VV" : ["WW_pythia","WZ_pythia","ZZ_pythia"],
    "ST" : ["SingleTop*"],
    "TT" : ["TT*"],
    "QCD" : ["QCD*"],
}

l_lep = ['NonpromptLepton','PromptLepton']
l_tau = ['NonpromptTau','PromptTau']

combinations = product(l_lep, l_tau)
nonprompts = [f"{A}__{B}__" for A, B in combinations if not (A == 'PromptLepton' and B == 'PromptTau')]

def GetTMPDir() :
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def GetSKOutDir(analyzername,era) : 
    return f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/{analyzername}/{era}"

def HADDnGet(analyzername,era,flag,outdir,skim) :
    
    hasSkim = skim is not ''

    if not flag == '' : 
        flagstr = f"{flag}__"
        outdir = f"{outdir}__{flag}"
    else : flagstr = flag
        

    os.system(f"mkdir -p ../RootFiles/{outdir}/DATA")

    hadddir = f"{GetSKOutDir(analyzername,era)}/{flagstr}"
    # Data
    basename = analyzername
    if hasSkim : 
        analyzername = basename + "_SkimTree_" + skim
        samplegroup = samplegroup_skim
    else : samplegroup = samplegroup_noskim
    os.system(f"hadd ../RootFiles/{outdir}/DATA/{basename}_DATA.root {GetSKOutDir(basename,era)}/{flagstr}/DATA/{analyzername}_Tau*")

    # Prompt HADD
    for sample in samplegroup :
        if len(samplegroup[sample]) > 0 :
            haddstr = ""
            for name in samplegroup[sample] :
                haddstr += f"{hadddir}/{analyzername}_{name}.root "
            os.system(f"hadd ../RootFiles/{outdir}/{basename}_{sample}.root {haddstr}")

        else : 
            os.system(f"hadd ../RootFiles/{outdir}/{basename}_{sample}.root {hadddir}/{analyzername}_{sample}*Tau*")

    for V in ["W","DY"] :
        if not hasSkim : os.system(f"cp {hadddir}/{analyzername}_{V}Jets_MG_TauHLT.root ../RootFiles/{outdir}")
        else : os.system(f"cp {hadddir}/{analyzername}_{V}Jets_MG.root ../RootFiles/{outdir}/{basename}_{V}Jets_MG.root")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hadd output files from WRTauAnalyzer')
    parser.add_argument('--flag'  , type=str , help='Additional flag used' , default = '' ) 
    parser.add_argument('--outdir', type=str , help='Output dir'           , default = GetTMPDir() )
    parser.add_argument('--era'   , type=int , help='Era, if 0 full era combination')
    parser.add_argument('--skim'  , type=str , help='Skim name i.e Name if SkimTree_Name' , default = '' )
    parser.add_argument('--analyzername', type=str , help='Analyzer name'  , default = 'WRTau_Analyzer' )
    args = parser.parse_args()

    HADDnGet(args.analyzername,args.era,args.flag,args.outdir,args.skim)