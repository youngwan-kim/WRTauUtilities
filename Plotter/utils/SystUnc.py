from ROOT import *
import os
import array
from .tools import getLumiSyst
import tracemalloc

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
            systList.append(systName)

    out = []
    for syst in systList :
        syst_str = ""
        if "Up" in syst         : syst_str = syst.replace("Up","")
        elif "Down" in syst     : syst_str = syst.replace("Down","")
        elif syst == "Central"  : syst_str = syst
        out.append(syst_str)

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

        del h_central_
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
                h_down = h_down_.Clone(f"{syst}Down").Rebin(len(VarDic[varKey][6])-1,f"{syst}Down",array.array('d',VarDic[varKey][6]))
            else :
                h_up = h_up_.Clone(f"{syst}Up").Rebin(VarDic[varKey][1])
                h_down = h_down_.Clone(f"{syst}Down").Rebin(VarDic[varKey][1])
                
            for h in [h_up_,h_down_] : del h

            nUp = h_up.GetBinContent(binN)
            nDown = h_down.GetBinContent(binN)

            systDict[syst] = [max((nUp-nCentral),(nCentral-nDown)),max((nUp-nCentral)/nCentral,(nCentral-nDown)/nCentral),nCentral]

        for h in [h_up,h_central,h_down] : del h
    

    systFile.Close()
    return systDict


def GetTotalSystError(stamp,samplename,era,varKey,VarDic) :
    systDict = GetSystError(stamp,samplename,era,varKey,VarDic)
    l = []
    for binN in range(1,len(systDict["Central"])+1) :
        unc = 0.
        unc_r = 0.
        print(f"[{samplename}] {varKey} Bin #{binN} Syst. Unc. Summary ")
        nCentral = systDict["Central"][binN-1]
        for syst in systDict :
            if syst != "Central" :
                #print(systDict[syst])
                err = systDict[syst][0][binN-1] 
                err_r = systDict[syst][1][binN-1] 
                unc += err**2
                print(f"\t {syst} : {nCentral} +/- {err} ({err_r*100}%)")
        if nCentral == 0 : unc_r = 0.
        else : unc_r = sqrt(unc) / nCentral
        print(f"\t\t Total Syst. Unc. = {nCentral} +/- {sqrt(unc)} ({unc_r}%)")
        l.append(sqrt(unc))
    del systDict
    return l



def GetSystError(stamp,samplename,era,varKey,VarDic) :
    systDir  = f"{os.getenv('WRTau_Output')}/{stamp}/{era}/RunSyst"
    systFile = TFile(f"{systDir}/WRTau_Analyzer_{samplename}.root")
    systList = GetSystList(stamp,samplename,era)

    systDict = {key : [] for key in systList}

    for syst in systList :

        l_err , l_central, l_r = [] , [], []

        h_central_ = systFile.Get(f"Central/__PromptTau__PromptLepton/{varKey}")
        gROOT.cd()

        if len(VarDic[varKey]) == 8 :
            h_central = h_central_.Clone(f"{syst}Central").Rebin(len(VarDic[varKey][6])-1,f"{syst}Central",array.array('d',VarDic[varKey][6]))
        else :
            h_central = h_central_.Clone(f"{syst}Central").Rebin(VarDic[varKey][1])

        if syst == "Central" :
            for i in range(1,h_central.GetNbinsX()+1) :
                l_central.append(h_central.GetBinContent(i))
            systDict[syst] = l_central
            continue 
        else :
            h_up_ = systFile.Get(f"{syst}Up/__PromptTau__PromptLepton/{varKey}")
            gROOT.cd()

            h_down_ = systFile.Get(f"{syst}Down/__PromptTau__PromptLepton/{varKey}")
            gROOT.cd()

            if len(VarDic[varKey]) == 8 :
                h_up = h_up_.Clone(f"{syst}Up").Rebin(len(VarDic[varKey][6])-1,f"{syst}Up",array.array('d',VarDic[varKey][6]))
                h_down = h_down_.Clone(f"{syst}Down").Rebin(len(VarDic[varKey][6])-1,f"{syst}Down",array.array('d',VarDic[varKey][6]))
            else :
                h_up = h_up_.Clone(f"{syst}Up").Rebin(VarDic[varKey][1])
                h_down = h_down_.Clone(f"{syst}Down").Rebin(VarDic[varKey][1])

            del h_central_ ; del h_up_ ; del h_down_

            h_plus = h_up - h_central
            h_minus = h_central - h_down

            for i in range(1,h_central.GetNbinsX()+1) :
                v = 0. ; v_r = 0.
                l_central.append(h_central.GetBinContent(i))
                if h_central.GetBinContent(i) != 0 : 
                    v = max(abs(h_plus.GetBinContent(i)),abs(h_minus.GetBinContent(i)))
                    #print(syst,samplename,i,h_plus.GetBinContent(i),h_minus.GetBinContent(i))
                    v_r = v/h_central.GetBinContent(i)
                else : v , v_r = 0., 0.
                l_err.append(v)
                l_r.append(v_r)

            systDict[syst] = [l_err,l_r]

        
        for h in [h_up,h_central,h_down] : del h
    
    lumi = [getLumiSyst(era)-1. for _ in range(len(systDict["Central"]))]
    #print(systDict["Central"])
    lumierr = [getLumiSyst(era) * n for n in systDict["Central"]]
    systDict["Luminosity"] = [lumierr,lumi]
    
    systFile.Close()
    return systDict
