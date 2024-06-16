from ROOT import *
from array import array
import math

stamp = "240527"
l_era = ["2016preVFP","2016","2017","2018","Run2"]

signals = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [100,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

signals = {
    2000 : [100,200,400,600,1000,1400,1800,1900]
}

def FoM(sig, bkg): 
    return math.sqrt( 2.*((sig+bkg)*math.log(1+(sig/max(bkg,1e-20))) - sig))

def check(root_file, histogram_name):

    if not root_file or root_file.IsZombie():
        print("Error: Unable to open file:", file_name)
        return False

    histogram = root_file.Get(histogram_name)

    if histogram:
        #print("Histogram", histogram_name, "exists in the file.")
        return True
    else:
        #print("Histogram", histogram_name, "does not exist in the file.")
        return False


l_era = ["2017"]
for era in l_era :
    for region in ["Resolved","Boosted"] :
        for lep in ["MuTau","ElTau"] :
            f_MC     = TFile(f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/2DScan__Delta__/WRTau_Analyzer_Bkg.root")
            h_MetMeff_MCPrompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_ST")
            h_MetMeff_MCNonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_ST")
            h_MetMeff = h_MetMeff_MCPrompt.Clone(f"{era}{region}{lep}")
            h_MetMeff.Add(h_MetMeff_MCNonprompt)
            for mwr in signals :
                for mn in signals[mwr] :
                        f_Signal = TFile(f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/2DScan__Delta__/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
                        h_MetMeff_Signal      = f_Signal.Get(f"Central/Benchmark{region}Preselection_{lep}/MET_ST")
                        if not check(f_Signal,f"Central/Benchmark{region}Preselection_{lep}/MET_ST") : continue
                        for cut in range(300,2000,50) :

                            h_MetMeff.SetStats(0)

                            bin_MET0  = h_MetMeff.GetXaxis().FindBin(100)
                            bin_Meff0 = h_MetMeff.GetYaxis().FindBin(cut)
                            n_bins_x = h_MetMeff.GetNbinsX()
                            n_bins_y = h_MetMeff.GetNbinsY()

                            nBkg = h_MetMeff.Integral(bin_MET0, n_bins_x, bin_Meff0, n_bins_y)
                            nSig = h_MetMeff_Signal.Integral(bin_MET0, n_bins_x, bin_Meff0, n_bins_y)


                            print(f"{era},{region},{lep},{cut},{mwr},{mn},{nBkg},{nSig},{FoM(nSig,nBkg)}")
            h_MetMeff_MCPrompt.Delete()
            h_MetMeff_MCNonprompt.Delete()