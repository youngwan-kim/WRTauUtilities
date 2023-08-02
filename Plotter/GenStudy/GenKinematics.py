import os
from ROOT import TCanvas,TH1D,TFile, TLegend, TLatex
from ROOT import kRed,kOrange,kGreen,kAzure, gStyle

d_mp = {1000:[100,500,900],2000:[100,400],4000:[100,2000,3900]}
l_col = [kRed+1,kGreen+2,kAzure+2]
d_merged_plots = {"Lepton0":["pt","eta"],"Lepton1":["pt","eta"],
           "FatJet0":["pt","eta"],"WR":["mass","mass_test"],"N":["mass","mass_test"]}
d_resolved_plots = {"Lepton0":["pt","eta"],"Lepton1":["pt","eta"],
           "Jet0":["pt","eta"],"Jet1":["pt","eta"],
           "WR":["mass","eta","pT"],"N":["mass","eta","pT"]}
dirname = "/data9/Users/youngwan/work/FastSim/CMSSW_10_6_22/src/PhysicsTools/NanoAODTools/python/postprocessing/analyser/WRTauStudy/"
d_merged_objname = {"Lepton0":"l_{pri}","Lepton1":"l_{sec}",
           "FatJet0":"J","WR":"#tau_{pri}J","N":"J"}
d_resolved_objname = {"Lepton0":"l_{pri}","Lepton1":"l_{sec}",
           "Jet0":"j_{lead}","Jet1":"j_{sublead}",
           "WR":"l_{pri}l_{sec}","N":"J"}
d_varname = {"pt":"p_{T}","pT":"p_{T}","eta":"#eta"}
d_plots_region = {"merged" : d_merged_plots, "resolved" : d_resolved_plots}


def getXsec(mWR,mN) :
    with open("../data/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def getTitle(obj,var) :
    d_objname = d_plots_region[region]
    if var == "mass" : return f"m({d_objname[obj]})"
    unit = ["(GeV)",""][d_varname[var] is not "eta"]
    return f"{d_varname[var]} of {d_objname[obj]} {unit}"

for region in ["merged","resolved"] :
    for obj in d_plots_region[region] :
        for var in d_plots_region[region][obj] :
            for mWR in d_mp :
                os.system(f"mkdir -p ../fig/signalsample/WR{mWR}/{region}")
                c = TCanvas(f"{region}_WR{mWR}_{obj}_{var}","",1000,1000)
                l = TLegend(0.5,0.675,0.85,0.875)
                latex = TLatex()
                latex.SetNDC()
                l.SetFillStyle(0)
                l.SetBorderSize(0)
                idx = 0 ; maxy = []
                for mN in d_mp[mWR] :
                    f = TFile(f"{dirname}/WR{mWR}N{mN}.root")
                    h = f.Get(f"plots/{region}_{obj}_{var}")
                    h.Scale(1./h.Integral())
                    ptmax = mWR*0.8
                    if var == "pt"  or var == "pT": 
                        if obj == "WR"  : ptmax = 1000
                        h.GetXaxis().SetRangeUser(0,ptmax)
                    if var == "mass" : 
                        h.Rebin(10)
                        if obj == "WR" : h.GetXaxis().SetRangeUser(mWR-500,mWR+500)
                        elif obj == "N" : h.GetXaxis().SetRangeUser(0,mWR)
                    if obj == "N" and var == "eta" : h.Rebin(5)
                    maxy.append(h.GetMaximum())
                for mN in d_mp[mWR] :
                    f = TFile(f"{dirname}/WR{mWR}N{mN}.root")
                    h = f.Get(f"plots/{region}_{obj}_{var}")
                    h.SetTitle("")
                    h.SetDirectory(0)
                    h.SetStats(0)
                    h.Scale(1./h.Integral())
                    h.SetLineColor(l_col[idx])
                    h.SetLineWidth(4)
                    ptmax = mWR*0.8
                    if var == "pt" or var == "pT": 
                        if obj == "WR" : ptmax = 1000
                        h.GetXaxis().SetRangeUser(0,ptmax)
                    if var == "mass" : 
                        h.Rebin(10)
                        if obj == "WR" : h.GetXaxis().SetRangeUser(mWR-500,mWR+500)
                        elif obj == "N" : h.GetXaxis().SetRangeUser(0,mWR)
                    if obj == "N" and var == "eta" : h.Rebin(5)
                    #h.GetXaxis().SetTitle(getTitle(obj,var))
                    h.GetYaxis().SetRangeUser(0,max(maxy)*1.5)
                    h.GetYaxis().SetTitle("A.U.")
                    h.GetYaxis().SetTitleSize(0.05)
                    l.AddEntry(h,"m_{W_{R}}="+str(mWR)+" GeV, m_{N}="+str(mN)+" GeV","l")
                    c.cd()
                    if idx == 0 : h.Draw("hist")
                    else : h.Draw("hist&same")
                    idx += 1
                textSize = 0.5*gStyle.GetPadTopMargin()
                #latex.SetTextAlign(31)
                latex.SetTextFont(61)
                latex.SetTextSize(textSize)
                latex.DrawLatex(0.2, 0.8,"CMS")
                latex.SetTextFont(52)
                latex.SetTextSize(0.75*textSize)
                latex.DrawLatex(0.2, 0.76,"Simulation")
                l.Draw()
                c.SetLeftMargin(0.15)
                c.SetBottomMargin(0.1)
                c.Draw()
                c.SaveAs(f"../fig/signalsample/WR{mWR}/{region}/{obj}_{var}.png")
                c.SaveAs(f"../fig/signalsample/WR{mWR}/{region}/{obj}_{var}.pdf")
