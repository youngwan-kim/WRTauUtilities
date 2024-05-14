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

dirname = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2016preVFP"
dir_benchmark = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2016preVFP/EXO_16_023__"

for mWR in d_mass :
    for mN in d_mass[mWR] :
        f = TFile(f"{dirname}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
        f_benchmark = TFile(f"{dir_benchmark}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
        h1 = f.Get(f"Central/Cutflow")
        h_gen = f_benchmark.Get("Central/GenLevelChannel")
        h_benchmark_mu = f_benchmark.Get("Central/EXO_16_023_Preselection_MuTau/Nevents")
        nTotal = h_gen.GetBinContent(3)
        #nTotal = h1.GetBinContent(1)
        #nTest = h_benchmark.GetBinContent(1)
        #print(nTotal,nTest)
        n_BenchmarkPresel_mu = h_benchmark_mu.Integral()
        h_benchmark_el = f_benchmark.Get("Central/EXO_16_023_Preselection_ElTau/Nevents")
        n_BenchmarkPresel_el = h_benchmark_el.Integral()
        h_bst_el = f.Get(f"Central/BoostedSignalRegion_ElTau/Nevents")
        h_bst_mu = f.Get(f"Central/BoostedSignalRegion_MuTau/Nevents")
        h_rsv_el = f.Get(f"Central/ResolvedSignalRegion_ElTau/Nevents")
        h_rsv_mu = f.Get(f"Central/ResolvedSignalRegion_MuTau/Nevents")
        h_bstPre_el = f_benchmark.Get(f"Central/BenchmarkBoostedPreselection_ElTau/Nevents")
        h_bstPre_mu = f_benchmark.Get(f"Central/BenchmarkBoostedPreselection_MuTau/Nevents")
        h_rsvPre_el = f_benchmark.Get(f"Central/BenchmarkResolvedPreselection_ElTau/Nevents")
        h_rsvPre_mu = f_benchmark.Get(f"Central/BenchmarkResolvedPreselection_MuTau/Nevents")
        
        eff_bst_el = 100. * h_bst_el.Integral()/nTotal
        eff_bst_mu = 100. * h_bst_mu.Integral()/nTotal
        eff_rsv_el = 100. * h_rsv_el.Integral()/nTotal
        eff_rsv_mu = 100. * h_rsv_mu.Integral()/nTotal
        eff_bstPre_el = 100. * h_bstPre_el.Integral()/nTotal
        eff_bstPre_mu = 100. * h_bstPre_mu.Integral()/nTotal
        eff_rsvPre_el = 100. * h_rsvPre_el.Integral()/nTotal
        eff_rsvPre_mu = 100. * h_rsvPre_mu.Integral()/nTotal
        
        eff_Presel_mu = eff_rsvPre_mu + eff_bstPre_mu
        eff_Presel_el = eff_rsvPre_el + eff_bstPre_el
        eff_BenchmarkPresel_mu = 100. * n_BenchmarkPresel_mu/nTotal
        eff_BenchmarkPresel_el = 100. * n_BenchmarkPresel_el/nTotal

        print(f"{mWR},{mN},{eff_rsvPre_el},{eff_bstPre_el},{eff_Presel_el},{eff_BenchmarkPresel_el}")
        #print(f"{mWR},{mN},{eff_rsvPre_mu},{eff_bstPre_mu},{eff_Presel_mu},{eff_BenchmarkPresel_mu}")
        #print(f"{mWR},{mN},{eff_bst_el},{eff_bst_mu},{eff_rsv_el},{eff_rsv_mu},{eff_bstPre_el},{eff_bstPre_mu},{eff_rsvPre_el},{eff_rsvPre_mu}")
        #htau = f.Get("plots/FinalStates")
        #eff_taetah = htau.GetBinContent(2)/htau.GetBinContent(1)
        #eff_tamutah = htau.GetBinContent(3)/htau.GetBinContent(1)
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tautau*100:.2f}")+"\\%}"
        #print(f"& {eff_tamutah_latex} &{eff_resolved*100:.2f}\% & {eff_boosted*100:.2f}\% \\\\")
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tamutah*100:.2f}")+"\\%}"
        #print(f"{eff_taetah*100:.2f}\% & {eff_tamutah_latex}")