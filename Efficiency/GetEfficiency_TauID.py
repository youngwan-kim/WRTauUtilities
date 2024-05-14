import os
from ROOT import *
 
d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [200,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

dirname = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/SignalDebug__"

for mWR in d_mass :
    for mN in d_mass[mWR] :
        f = TFile(f"{dirname}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
        h = f.Get(f"Central/nAllTaus")
        h_base = f.Get(f"Central/nBaselineTaus")
        h1 = f.Get(f"Central/nBaseline_L_Taus")
        h2 = f.Get(f"Central/nBaseline_T_Taus")
        h3 = f.Get(f"Central/nBaseline_TL_Taus")
        h4 = f.Get(f"Central/nBaseline_TT_Taus")
        h5 = f.Get(f"Central/nBaseline_TTL_Taus")
        h6 = f.Get(f"Central/nBaseline_TTT_Taus")
        h7 = f.Get(f"Central/nTaus")
        

        nTotal   = h.Integral() 

        n0       = h.Integral() - h.GetBinContent(1)
        nbase    = h_base.Integral() - h_base.GetBinContent(1)
        n1       = h1.Integral() - h1.GetBinContent(1)
        n2       = h2.Integral() - h2.GetBinContent(1)
        n3       = h3.Integral() - h3.GetBinContent(1)
        n4       = h4.Integral() - h4.GetBinContent(1)
        n5       = h5.Integral() - h5.GetBinContent(1)
        n6       = h6.Integral() - h6.GetBinContent(1)
        n7       = h7.Integral() - h7.GetBinContent(1)


        
        #print(f"{mWR},{mN},{effTrigger},{effTauID},{effSafePt},{effLep},{effPre},{effSig}")
        #print(f"{mWR},{mN},{effTrigger},{effTauID},{effSafePt},{effLep},{effBstPre},{effBstSig}")
        print(f"{mWR},{mN},{nbase/nTotal},{n1/nTotal},{n2/nTotal},{n3/nTotal},{n4/nTotal},{n5/nTotal},{n6/nTotal},{n7/nTotal}")
        #htau = f.Get("plots/FinalStates")
        #eff_taetah = htau.GetBinContent(2)/htau.GetBinContent(1)
        #eff_tamutah = htau.GetBinContent(3)/htau.GetBinContent(1)
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tautau*100:.2f}")+"\\%}"
        #print(f"& {eff_tamutah_latex} &{eff_resolved*100:.2f}\% & {eff_boosted*100:.2f}\% \\\\")
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tamutah*100:.2f}")+"\\%}"
        #print(f"{eff_taetah*100:.2f}\% & {eff_tamutah_latex}")