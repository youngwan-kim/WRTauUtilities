from ROOT import *
import os, argparse
from utils import *
from datetime import datetime

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

parser = argparse.ArgumentParser(description='xsec systematic envelope extractor')
parser.add_argument('-e', dest='era'  , type=str, help='Era to plot', default=2017)
parser.add_argument('-o', dest='out'  , type=str, help='Output directory name',default=default_outputdir)
parser.add_argument('-i', dest='inputtag'  , type=str, help='Output directory name',default=240907)
parser.add_argument('-s', dest='systematic', nargs='+', help='Systematic source')
parser.add_argument('--signals', action='store_true')
args = parser.parse_args()

era, outputtag, inputtag = args.era , args.out, args.inputtag
runSignals = args.signals
runBkgs = False
if not runSignals : runBkgs = True
l_systematic = args.systematic

d_mass_ = d_mass
if era == "2018" : d_mass_ = d_mass_2018

os.system(f"mkdir -p SystematicPlots/{outputtag}/{era}")

if runSignals : 
    for mwr in d_mass_ :
        for mn in d_mass_[mwr] : 
            for region in ["SR"] :
                dirname = f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Outputs/{inputtag}/{region}/{era}/WR{mwr}_N{mn}_card_input.root"
                for syst_ in l_systematic :
                    f = TFile.Open(dirname)
                    h_central = f.Get(f"signal_{region}").Clone(f"{mwr}{mn}{region}{syst_}")
                    h_central.Scale(1./GetSignalScale(mwr))
                    h_up = f.Get(f"signal_{region}_{syst_}Up").Clone(f"{mwr}{mn}{region}{syst_}up")
                    h_up.Scale(1./GetSignalScale(mwr))
                    h_down = f.Get(f"signal_{region}_{syst_}Down").Clone(f"{mwr}{mn}{region}{syst_}down")
                    h_down.Scale(1./GetSignalScale(mwr))
                    print(h_central)
                    print(h_up)
                    c = TCanvas("","",1000,1000)
                    l = TLegend(0.8,0.7,0.9,0.9)
                    h_central.SetLineColor(kBlack)
                    h_up.SetLineColor(kRed)
                    h_down.SetLineColor(kBlue)
                    c.cd()
                    maxy = max(h_up.GetMaximum(),h_down.GetMaximum())
                    val_mins = []
                    for h in [h_up,h_central,h_down ] : 
                        for i in range(1,h.GetNbinsX()+1) :
                            if h.GetBinContent(i) > 0 : val_mins.append(h.GetBinContent(i))
                    miny = min(val_mins)
                    print(miny)
                    l.AddEntry(h_central,"Central","l")
                    l.AddEntry(h_up,"Up","l")
                    l.AddEntry(h_down,"Down","l")
                    for h in [h_up,h_central,h_down] : 
                        h.SetStats(0)
                        h.GetYaxis().SetRangeUser(miny*0.5,maxy*2.5)
                    h_up.SetLineWidth(3)
                    h_down.SetLineWidth(3)
                    h_central.SetLineWidth(2)
                    #h_central.SetLineStyle(2)
                    c.SetLogy()
                    c.SetLogx()
                    
                    h_up.Draw("hist")
                    h_down.Draw("same&hist")
                    h_central.Draw("e&hist&same")
                    l.Draw()
                    print(f"{mwr},{mn} signal up/down for {syst_} in {era},{region} done")
                    c.SaveAs(f"SystematicPlots/{outputtag}/{era}/WR{mwr}_N{mn}_{region}_{syst_}.png")
                    c.SaveAs(f"SystematicPlots/{outputtag}/{era}/WR{mwr}_N{mn}_{region}_{syst_}.pdf")

elif runBkgs : 
    for bkg in [top,boson] : 
        dirname = f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Outputs/{inputtag}/{region}/{era}/WR1000_N100_card_input.root"
        f = TFile.Open(f"{dirname}")
        for syst_ in l_systematic :
            h_central = f.Get(f"{bkg}_{region}") 
            h_up = f.Get(f"{bkg}_{region}_{syst_}Up") 
            h_down = f.Get(f"{bkg}_{region}_{syst_}Down") 
            c = TCanvas("","",1000,1000)
            l = TLegend(0.8,0.7,0.9,0.9)
            h_up.SetLineColor(kRed)
            h_down.SetLineColor(kBlue)
            c.cd()
            maxy = max(h_up.GetMaximum(),h_down.GetMaximum())
            for h in [h_up,h_central,h_down] : 
                h.SetStats(0)
                h.SetRangeUser(1e-7,maxy*1e+3)
            c.SetLogy()
            h_up.Draw("hist&l")
            h_central.Draw("same&hist&l")
            h_down.Draw("same&hist")
            c.SaveAs(f"SystematicPlots/{outputtag}/{era}/{bkg}_{region}_{syst_}.png")
            c.SaveAs(f"SystematicPlots/{outputtag}/{era}/{bkg}_{region}_{syst_}.pdf")
