from ROOT import *
import os
import array
from .tools import getLumiSyst

'''
brute force systematic unc. calculator for prefit plots
'''
 
def GetSystList(stamp,samplename,era) :
    systDir  = f"{os.getenv('WRTau_Output')}/{stamp}/{era}/RunSyst"
    systFile = TFile(f"{systDir}/WRTau_Analyzer_{samplename}.root")
    
    systList = []

    for key in systFile.GetListOfKeys():
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            systName = obj.GetName()
            if systName != "Central" : systList.append(systName)

    out = []

    for syst in systList :
        if "Up" in syst     : out.append(syst.replace("Up",""))
        elif "Down" in syst : out.append(syst.replace("Down",""))

    out = list(set(out))

    systFile.Close()
    return out

def GetSystError(stamp,samplename,era,varKey,VarDic,binN) :
    systDir  = f"{os.getenv('WRTau_Output')}/{stamp}/{era}/RunSyst"
    systFile = TFile(f"{systDir}/WRTau_Analyzer_{samplename}.root")
    systList = GetSystList(stamp,samplename,era)

    systDict = {key : [] for key in systList}

    for syst in systList :

        h_central_ = systFile.Get(f"Central/__PromptTau__PromptLepton/{varKey}")
        gROOT.cd()
        if len(VarDic[varKey]) == 8 :
            h_central = h_central_.Clone(f"{syst}Central").Rebin(len(VarDic[varKey][6])-1,f"{syst}Central",array.array('d',VarDic[varKey][6]))
        else :
            h_central = h_central_.Clone(f"{syst}Central").Rebin(VarDic[varKey][1])

        nCentral = h_central.GetBinContent(binN)

        if nCentral == 0 : 
            systDict[syst] = [0.,0.,0.]
            continue
        else :
            h_up_ = systFile.Get(f"{syst}Up/__PromptTau__PromptLepton/{varKey}")
            gROOT.cd()
            h_down_ = systFile.Get(f"{syst}Down/__PromptTau__PromptLepton/{varKey}")
            gROOT.cd()
            if len(VarDic[varKey]) == 8 :
                h_up = h_up_.Clone(f"{syst}Up").Rebin(len(VarDic[varKey][6])-1,f"{syst}Up",array.array('d',VarDic[varKey][6]))
                h_central = h_central_.Clone(f"{syst}Central").Rebin(len(VarDic[varKey][6])-1,f"{syst}Central",array.array('d',VarDic[varKey][6]))
                h_down = h_down_.Clone(f"{syst}Down").Rebin(len(VarDic[varKey][6])-1,f"{syst}Down",array.array('d',VarDic[varKey][6]))
            else :
                h_up = h_up_.Clone(f"{syst}Up").Rebin(VarDic[varKey][1])
                h_central = h_central_.Clone(f"{syst}Central").Rebin(VarDic[varKey][1])
                h_down = h_down_.Clone(f"{syst}Down").Rebin(VarDic[varKey][1])

            nUp = h_up.GetBinContent(binN)
            nDown = h_down.GetBinContent(binN)

            systDict[syst] = [max((nUp-nCentral),(nCentral-nDown)),max((nUp-nCentral)/nCentral,(nCentral-nDown)/nCentral),nCentral]

        for h in [h_up,h_central,h_down] : del h
    
    for syst_global in d_global :
        d_global["Luminosity"] = getLumiSyst(era)-1.0
        n_ = systDict[systList[0]][2]
        if n_ == 0 : systDict[syst_global] = [0.,0.,0.]
        else :
            systDict[syst_global] = [n_*d_global[syst_global],d_global[syst_global],n_]
    systFile.Close()
    return systDict

d_global = {
    "Luminosity" : 0. ,
}

def GetTotalSystError(stamp,samplename,era,varKey,VarDic,binN) :
    systDict = GetSystError(stamp,samplename,era,varKey,VarDic,binN)
    unc = 0
    print(f"{varKey} Bin #{binN} Syst. Unc. Summary ")
    for syst in systDict :
        unc += systDict[syst][0]**2
        print(f"\t {syst} : {systDict[syst][2]} +/- {abs(systDict[syst][0])} ({abs(systDict[syst][1])*100}%)")
    print(f"\t\t Total Syst. Unc. = {systDict[syst][2]} +/- {sqrt(unc)} ({sqrt(unc)/systDict[syst][2]*100}%)")
    del systDict
    return sqrt(unc)