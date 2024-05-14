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

dirname = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2016preVFP"


for mWR in d_mass :
    for mN in d_mass[mWR] :
        f = TFile(f"{dirname}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
        h1 = f.Get(f"Central/Cutflow")
        h_bst_el = f.Get(f"Central/BoostedSignalRegion_ElTau/Nevents")
        h_bst_mu = f.Get(f"Central/BoostedSignalRegion_MuTau/Nevents")
        h_rsv_el = f.Get(f"Central/ResolvedSignalRegion_ElTau/Nevents")
        h_rsv_mu = f.Get(f"Central/ResolvedSignalRegion_MuTau/Nevents")
        h_bstPre_el = f.Get(f"Central/BoostedPreselection_ElTau/Nevents")
        h_bstPre_mu = f.Get(f"Central/BoostedPreselection_MuTau/Nevents")
        h_rsvPre_el = f.Get(f"Central/ResolvedPreselection_ElTau/Nevents")
        h_rsvPre_mu = f.Get(f"Central/ResolvedPreselection_MuTau/Nevents")
        
        nTotal   = h1.GetBinContent(1)
        nTrigger = h1.GetBinContent(2)
        nTauID   = h1.GetBinContent(3)
        nSafePt  = h1.GetBinContent(4)
        nLep     = h1.GetBinContent(5)
        nBstPre  = h_bstPre_el.Integral() + h_bstPre_mu.Integral()
        nRsvPre  = h_rsvPre_el.Integral() + h_rsvPre_mu.Integral()
        nPre     = nBstPre + nRsvPre
        nBst     = h_bst_el.Integral() + h_bst_mu.Integral()
        nRsv     = h_rsv_el.Integral() + h_rsv_mu.Integral()
        nSig     = nBst + nRsv

        effTrigger = nTrigger/nTotal
        effTauID   = nTauID/nTotal
        effSafePt  = nSafePt/nTotal
        effLep     = nLep/nTotal
        effPre     = nPre/nTotal
        effSig     = nSig/nTotal

        effBstPre = nBstPre/nTotal
        effRsvPre = nRsvPre/nTotal
        effBstSig = nBst/nTotal
        effRsvSig = nRsv/nTotal

        
        #print(f"{mWR},{mN},{effTrigger},{effTauID},{effSafePt},{effLep},{effPre},{effSig}")
        #print(f"{mWR},{mN},{effTrigger},{effTauID},{effSafePt},{effLep},{effBstPre},{effBstSig}")
        print(f"{mWR},{mN},{effTrigger},{effTauID},{effSafePt},{effLep},{effRsvPre},{effRsvSig}")
        #htau = f.Get("plots/FinalStates")
        #eff_taetah = htau.GetBinContent(2)/htau.GetBinContent(1)
        #eff_tamutah = htau.GetBinContent(3)/htau.GetBinContent(1)
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tautau*100:.2f}")+"\\%}"
        #print(f"& {eff_tamutah_latex} &{eff_resolved*100:.2f}\% & {eff_boosted*100:.2f}\% \\\\")
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tamutah*100:.2f}")+"\\%}"
        #print(f"{eff_taetah*100:.2f}\% & {eff_tamutah_latex}")