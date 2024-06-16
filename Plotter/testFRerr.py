import os
from utils import *
from math import sqrt
from ROOT import *
import array

VarDic = {
    "BoostedSignalRegionMETInvert_MuTau/Tauh_pT"  : [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,800.,[0,190,210,230,250,270,320,800],True],
    "BoostedSignalRegionMETInvert_MuTau/Tauh_eta" : [True,4,"Leading Hadronic Tau #eta (GeV)","Tauh_Eta",-3.,3.,[-3.,-2.4,-1.6,-1.0,-0.6,-0.3,0.,0.3,0.6,1.0,1.6,2.4,3.0],False],
}

fakeDir = f"{os.getenv('WRTau_Output')}/240521/2017"
fakeFile = TFile(f"{fakeDir}/WRTau_Analyzer_Fakes.root")
h_ = fakeFile.Get(f"Central_TauFRErrUp/BoostedSignalRegionMETInvert_MuTau/Tauh_pT")
h = h_.Clone("test").Rebin(len(VarDic["BoostedSignalRegionMETInvert_MuTau/Tauh_pT"][6])-1,"Up",array.array('d',VarDic["BoostedSignalRegionMETInvert_MuTau/Tauh_pT"][6]))

print(GetFakeFitErr("240521","2017","BoostedSignalRegionMETInvert_MuTau/Tauh_pT",VarDic,2))
for i in range(1,h.GetNbinsX()+1) :
    err0 = h.GetBinError(i)
    err1 = GetFakeFitErr("240521","2017","BoostedSignalRegionMETInvert_MuTau/Tauh_pT",VarDic,i)
    err = sqrt(err0**2 + err1**2)
    print(f"Original stat error for bin {i} = {err0}")
    print(f"Fit error for bin {i} = {err1}")
    print(f"New error for bin {i} = {err}")
