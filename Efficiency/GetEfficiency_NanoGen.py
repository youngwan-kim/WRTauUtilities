import os
from ROOT import TCanvas,TH1D,TFile, TLegend, TLatex
from ROOT import kRed,kOrange,kGreen,kAzure, gStyle

d_mp = {1000:[100,200,500,900],2000:[100,400,1000,1900],4000:[100,800,2000,3900]}
l_col = [kRed+1,kGreen+2,kAzure+2]
d_plots = {"Lepton0":["pt","eta"],"Lepton1":["pt","eta"],
           "Jet0":["pt","eta"],"Jet1":["pt","eta"],
           "WR":["mass","eta","pT"],"N":["mass","eta","pT"]}
dirname = "/data9/Users/youngwan/work/FastSim/CMSSW_10_6_22/src/PhysicsTools/NanoAODTools/python/postprocessing/analyser/WRTauStudy/"
d_objname = {"Lepton0":"#tau_{pri}","Lepton1":"#tau_{sec}",
           "Jet0":"j_{lead}","Jet1":"j_{sublead}",
           "WR":"#tau_{pri}#tau_{sec}jj","N":"#tau_{sec}jj"}
d_varname = {"pt":"p_{T}","pT":"p_{T}","eta":"#eta"}


def getXsec(mWR,mN) :
    with open("../data/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def getTitle(obj,var) :
    if var == "mass" : return f"m({d_objname[obj]})"
    unit = ["(GeV)",""][d_varname[var] is not "eta"]
    return f"{d_varname[var]} of {d_objname[obj]} {unit}"

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