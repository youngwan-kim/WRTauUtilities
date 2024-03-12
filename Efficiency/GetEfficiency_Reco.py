import os
from ROOT import TCanvas,TH1D,TFile, TLegend, TLatex
from ROOT import kRed,kOrange,kGreen,kAzure, gStyle

signaldir = f"{os.environ['SKFlatOutputDir']}/Run2UltraLegacy_v3/WRTau_Analyzer/2017"
file_pattern = "WRTau_Analyzer_WRtoTauNtoTauTauJets_WR"
extension = ".root"

files = [file for file in os.listdir(signaldir) if file.startswith(file_pattern) and file.endswith(extension)]

def getXsec(mWR,mN) :
    with open("../Data/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def getTitle(obj,var) :
    if var == "mass" : return f"m({d_objname[obj]})"
    unit = ["(GeV)",""][d_varname[var] is not "eta"]
    return f"{d_varname[var]} of {d_objname[obj]} {unit}"

for signal in files :
    mWR = signal.split("_")[3].split("WR")[1]
    mWR = signal.split("_")[4].split("N")

for mWR in d_mp :
    for mN in d_mp[mWR] :
        f = TFile(f"{dirname}/WR{mWR}N{mN}.root")
        h = f.Get(f"plots/Cutflow")
        #htau = f.Get("plots/FinalStates")
        eff_tautau = h.GetBinContent(2)/h.GetBinContent(1)
        eff_boosted = h.GetBinContent(3)/h.GetBinContent(1)
        eff_resolved = h.GetBinContent(4)/h.GetBinContent(1)
        #eff_taetah = htau.GetBinContent(2)/htau.GetBinContent(1)
        #eff_tamutah = htau.GetBinContent(3)/htau.GetBinContent(1)
        eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tautau*100:.2f}")+"\\%}"
        print(f"& {eff_tamutah_latex} &{eff_resolved*100:.2f}\% & {eff_boosted*100:.2f}\% \\\\")
        #eff_tamutah_latex = "\multicolumn{1}{c|}{"+str(f"{eff_tamutah*100:.2f}")+"\\%}"
        #print(f"{eff_taetah*100:.2f}\% & {eff_tamutah_latex}")