import os
from ROOT import TCanvas,TH1D,TFile, TLegend, TLatex
from ROOT import kRed,kOrange,kGreen,kAzure, gStyle


d_mp = {100:[1000,2000,4000]}
l_col = [kRed+1,kGreen+2,kAzure+2]

d_plots = {"WR":["mass_test"],"N":["mass_test"]}

d_plots = {"N":["mass_test"]}
dirname = "/data9/Users/youngwan/work/FastSim/CMSSW_10_6_22/src/PhysicsTools/NanoAODTools/python/postprocessing/analyser/WRTauStudy/"

d_objname = {"Lepton0":"#tau_{pri}","Lepton1":"#tau_{sec}",
           "Jet0":"j_{lead}","Jet1":"j_{sublead}",
           "WR":"#tau_{pri}J","N":"J"}
d_varname = {"pt":"p_{T}","pT":"p_{T}","eta":"#eta"}


def getXsec(mWR,mN) :
    with open("../data/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def getTitle(obj,var) :
    if "mass" in var : return f"m({d_objname[obj]})"
    unit = ["(GeV)",""][d_varname[var] is not "eta"]
    return f"{d_varname[var]} of {d_objname[obj]} {unit}"

for region in ["merged"] :
    for obj in d_plots :
        for var in d_plots[obj] :
            for mN in d_mp :
                os.system(f"mkdir -p ../fig/signalsample/N{mN}")
                c = TCanvas(f"N{mN}_{obj}_{var}","",1000,1000)
                l = TLegend(0.5,0.675,0.85,0.875)
                latex = TLatex()
                latex.SetNDC()
                l.SetFillStyle(0)
                l.SetBorderSize(0)
                idx = 0 ; maxy = []
                for mWR in d_mp[mN] :
                    f = TFile(f"{dirname}/WR{mWR}N{mN}.root")
                    h = f.Get(f"plots/{region}_{obj}_{var}")
                    h.Scale(1./h.Integral())
                    h.Rebin(2)
                    h.GetXaxis().SetRange(5,20)
                    maxy.append(h.GetMaximum())
                for mWR in d_mp[mN] :
                    f = TFile(f"{dirname}/WR{mWR}N{mN}.root")
                    h = f.Get(f"plots/{region}_{obj}_{var}")
                    h.SetTitle("")
                    h.SetDirectory(0)
                    h.SetStats(0)
                    h.Scale(1./h.Integral())
                    h.SetLineColor(l_col[idx])
                    h.SetLineWidth(4) 
                    h.Rebin(2)
                    h.GetXaxis().SetRange(5,20)
                    h.GetXaxis().SetTitle(getTitle(obj,var))
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
                c.SaveAs(f"../fig/signalsample/N{mN}/{obj}_{var}.png")
                c.SaveAs(f"../fig/signalsample/N{mN}/{obj}_{var}.pdf")
