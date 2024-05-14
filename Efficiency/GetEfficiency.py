import os
from ROOT import *
 
d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}


dirname = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017"

for mWR in d_mass :
    for mN in d_mass[mWR] :
        f = TFile(f"{dirname}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
        
        h1 = f.Get(f"Central/Cutflow")
        h_gen = f.Get("Central/GenLevelChannel")
        nTotal = h_gen.GetBinContent(3)+h_gen.GetBinContent(4)
        nTotal = h_gen.Integral()
        
        h_bst_el = f.Get(f"Central/BoostedSignalRegion_ElTau/Nevents")
        h_bst_mu = f.Get(f"Central/BoostedSignalRegion_MuTau/Nevents")
        h_rsv_el = f.Get(f"Central/ResolvedSignalRegion_ElTau/Nevents")
        h_rsv_mu = f.Get(f"Central/ResolvedSignalRegion_MuTau/Nevents")
        
        eff_bst_el = 100. * h_bst_el.Integral()/nTotal
        eff_bst_mu = 100. * h_bst_mu.Integral()/nTotal
        eff_rsv_el = 100. * h_rsv_el.Integral()/nTotal
        eff_rsv_mu = 100. * h_rsv_mu.Integral()/nTotal
        
        eff_bst = eff_bst_el + eff_bst_mu
        eff_rsv = eff_rsv_el + eff_rsv_mu
        eff_total = eff_bst + eff_rsv

        print(f"{mWR},{mN},{eff_bst},{eff_rsv},{eff_total}")
