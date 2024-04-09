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
    "VV" : ["WW_*","WZ_*","ZZ_*"],
    "ST" : ["SingleTop*","ST*"],
    "TT" : ["TT*"],
    "QCD" : ["QCD*"],
}

signals = {
    2000 : [200,1900],
    4000 : [200,3900],
    4800 : [200,4700]
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

    if era == "2017" : samplegroup_skim["ST"] = ["SingleTop*"]
    elif era == "2018" : samplegroup_skim["ST"] = ["ST*"]

    hasSkim = skim is not ''

    if not flag == '' : 
        flagstr = f"{flag}__"
        outdir = f"{outdir}__{flag}"
    else : flagstr = flag
        
    os.system(f"mkdir -p ../RootFiles/{outdir}/{era}/DATA")
    os.system(f"mkdir -p ../RootFiles/{outdir}/{era}/Signals")

    hadddir = f"{GetSKOutDir(analyzername,era)}/{flagstr}"

    basename = analyzername
    if hasSkim : 
        analyzername = basename + "_SkimTree_" + skim
        samplegroup = samplegroup_skim
    else : samplegroup = samplegroup_noskim

    #Signals
    for mwr in signals :
        for mn in signals[mwr] :
            os.system(f"cp {hadddir}/{basename}_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root ../RootFiles/{outdir}/{era}/Signals/{basename}_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
    if onlysignals : return
    
    #Data
    os.system(f"hadd ../RootFiles/{outdir}/{era}/DATA/{basename}_DATA.root {GetSKOutDir(basename,era)}/{flagstr}/DATA/{analyzername}_Tau*")
    # Prompt HADD
    for sample in samplegroup :
        if len(samplegroup[sample]) > 0 :
            haddstr = ""
            for name in samplegroup[sample] :
                haddstr += f"{hadddir}/{analyzername}_{name}.root "
            os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_{sample}.root {haddstr}")

        else : 
            os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_{sample}.root {hadddir}/{analyzername}_{sample}*Tau*")

    for V in ["W","DY"] :
        if not hasSkim : os.system(f"cp {hadddir}/{analyzername}_{V}Jets_MG_TauHLT.root ../RootFiles/{outdir}/{era}")
        else : os.system(f"cp {hadddir}/{analyzername}_{V}Jets_MG.root ../RootFiles/{outdir}/{era}/{basename}_{V}Jets_MG.root")

    # Boson Hadd
    os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_Boson.root ../RootFiles/{outdir}/{era}/{basename}_VVV.root ../RootFiles/{outdir}/{era}/{basename}_VV.root ../RootFiles/{outdir}/{era}/{basename}_DYJets_MG.root ../RootFiles/{outdir}/{era}/{basename}_WJets_MG.root")

    # Data Driven Tau Fake
    os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_DataDrivenTau.root {GetSKOutDir(basename,era)}/TauFake__/DATA/{analyzername}_Tau*")

    # Data Driven ResEl-Tau Fake
    os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_DataDrivenElTau.root {GetSKOutDir(basename,era)}/ResolvedElectronChannelFake__/DATA/{analyzername}_Tau*")

    # Lepton MC Fake
    os.system(f"hadd ../RootFiles/{outdir}/{era}/{basename}_MCLeptonFake.root ../RootFiles/{outdir}/{era}/{basename}_Boson.root ../RootFiles/{outdir}/{era}/{basename}_QCD.root ../RootFiles/{outdir}/{era}/{basename}_TT.root ../RootFiles/{outdir}/{era}/{basename}_ST.root ")

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