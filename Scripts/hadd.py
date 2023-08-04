import os,argparse,datetime,glob
from itertools import product

samplegroup = {
    "VVV" : ["WWW_TauHLT","WWZ_TauHLT","WZZ_TauHLT","ZZZ_TauHLT"],
    "VV" : ["WW_TauHLT","WZ_TauHLT","ZZ_TauHLT"],
    "ST" : [],
    "TT" : [],
    "QCD" : [],
}

l_lep = ['NonpromptLepton','PromptLepton']
l_tau = ['NonpromptTau','PromptTau']

combinations = product(l_lep, l_tau)
nonprompts = [f"{A}__{B}__" for A, B in combinations if not (A == 'PromptLepton' and B == 'PromptTau')]

def GetTMPDir() :
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def GetSKOutDir(analyzername,era) : 
    return f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/{analyzername}/{era}"

def HADDnGet(analyzername,era,flag,outdir)
    os.system(f"mkdir -p ../RootFiles/{outdir}/DATA")
    if not flag == '' : flagstr = f"{flag}__"
    else : flagstr = flag

    hadddir = f"{GetSKOutDir(analyzername,era)}/{flagstr}PromptLepton__PromptTau__"
    # Data
    os.system(f"hadd {outdir}/{analyzername}_DATA.root {hadddir}/DATA/{analyzername}_Tau*")

    # Prompt HADD
    for sample in samplegroup :
        if len(samplegroup[sample]) > 0 :
            haddstr = ""
            for name in samplegroup[sample] :
                haddstr += f"{hadddir}/{analyzername}_{name}.root "
            os.system(f"hadd ../RootFiles/{outdir}/{analyzername}_{sample}.root {haddstr}")

        else : 
            os.system(f"hadd ../RootFiles/{outdir}/{analyzername}_{sample}.root {hadddir}/{analyzername}_{sample}*Tau*")

    # Nonprompt HADD
    fullnonprompt = ""
    for np in nonprompts :
        hadddir = f"{GetSKOutDir(analyzername,era)}/{flagstr}{np}"
        allfiles = glob.glob(f"{hadddir}/*.root")
        bkgonly = [file for file in allfiles if "WRtoTauNtoTau" not in file]
        haddstr = ""
        for bkgf in bkgonly : haddstr += f"{hadddir}/{bkgf} "
        os.system(f"hadd ../RootFiles/{outdir}/{analyzername}_{np}.root {haddstr}")
        fullnonprompt += f"../RootFiles/{outdir}/{analyzername}_{np}.root "

    os.system(f"hadd ../RootFiles/{outdir}/{analyzername}_Nonprompt.root {fullnonprompt}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hadd output files from WRTauAnalyzer')
    parser.add_argument('--flag', type=str, required=True, help='Additional flag used',default=GetTMPDir())
    parser.add_argument('--outdir', type=str, required=True, help='Output dir')
    parser.add_argument('--era', type=int, required=True, help='Era, if 0 full era combination')
    parser.add_argument('--analyzername', type=str, required=True, help='Output dir')
    parser.add_argument('--fakemode', type=int, required=True, help='Fake division mode , 0 : Combine all / 1 : Division per fake source / 2 : Get Both',default=2)
    args = parser.parse_args()

    HADDnGet(args.analyzername,args.flag,args.outdir)