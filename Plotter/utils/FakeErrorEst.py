from ROOT import *
import os
import array

def GetFakeFitErr(stamp,era,varKey,VarDic,binN) :
    fakeDir = f"{os.getenv('WRTau_Output')}/{stamp}/{era}"
    fakeFile = TFile(f"{fakeDir}/WRTau_Analyzer_Fakes.root")
    h_up_ = fakeFile.Get(f"Central_TauFRErrUp/{varKey}")
    gROOT.cd()
    h_central_ = fakeFile.Get(f"Central/{varKey}")
    gROOT.cd()
    h_down_ = fakeFile.Get(f"Central_TauFRErrDown/{varKey}")
    #print(h_up_,h_central_,h_down_)
    #print(len(VarDic[varKey]))
    gROOT.cd()
    if len(VarDic[varKey]) == 8 :
        h_up = h_up_.Clone("Up").Rebin(len(VarDic[varKey][6])-1,"Up",array.array('d',VarDic[varKey][6]))
        h_central = h_central_.Clone("Central").Rebin(len(VarDic[varKey][6])-1,"Central",array.array('d',VarDic[varKey][6]))
        h_down = h_down_.Clone("Down").Rebin(len(VarDic[varKey][6])-1,"Down",array.array('d',VarDic[varKey][6]))
    else :
        h_up = h_up_.Clone("Up").Rebin(VarDic[varKey][1])
        h_central = h_central_.Clone("Central").Rebin(VarDic[varKey][1])
        h_down = h_down_.Clone("Down").Rebin(VarDic[varKey][1])
    nUp = h_up.GetBinContent(binN)
    nCentral = h_central.GetBinContent(binN)
    nDown = h_down.GetBinContent(binN)
    return max(nUp-nCentral,nCentral-nDown)


