import os,ROOT
from math import sqrt

for LSFCut in [0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85] :
    val = format(LSFCut,".2f").split('.')[1]
    b = 0 ; s = 0
    for bkg in ["QCD","TT","ST","VVV","VV","Nonprompt","DYJets_MG_TauHLT"] :
        f = ROOT.TFile(f"{os.getenv('WRTau_Output')}/LSFOptTest__LSFOpt/WRTau_Analyzer_{bkg}.root")
        h = f.Get(f"WRTau_SignalSingleTauTrg/vJetTight_vElTight_vMuTight/BoostedSignalRegion_LSF0p{val}_MuTau/nLooseLeptons")
        if h == None : b += 0
        else : b += h.Integral()
    for signal in ["WR2000_N100","WR2800_N100","WR3200_N100","WR3600_N100","WR4000_N100","WR4400_N100","WR4800_N200"] :
        fs = ROOT.TFile(f"{os.getenv('WRTau_Output')}/LSFOptTest__LSFOpt/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_{signal}.root")
        hs = fs.Get(f"WRTau_SignalSingleTauTrg/vJetTight_vElTight_vMuTight/BoostedSignalRegion_LSF0p{val}_MuTau/nLooseLeptons")
        if hs != None : s = hs.Integral()
        print(f"{signal},{LSFCut},{b},{s},{s/sqrt(b)}")