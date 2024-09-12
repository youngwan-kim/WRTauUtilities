#!/usr/bin/env python3
import os, sys, argparse, itertools, array, argparse
from ROOT import *
from utils import *
from math import sqrt
from datetime import datetime 
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2023) v2.213345661')
parser.add_argument('-a', dest='analyzername', type=str, help='Analyzer name',default="WRTau_Analyzer")
parser.add_argument('-i', dest='input', type=str, help='Input directory timestamp')
parser.add_argument('-e', dest='era', type=str, help='Era to plot', default=2017)
parser.add_argument('--userflags', type=str, help='user flag used', default="")
parser.add_argument('--WJGen', type=str, help='Wjets generator', default="MG")
parser.add_argument('--outputdir', type=str, help='Output directory name',default=default_outputdir)
parser.add_argument('--blind', action='store_true', help='Blind sensitive datapoints')
parser.add_argument('--debugmode', action='store_true', help='debug flag')
parser.add_argument('--onlypng', action='store_true', help='Only save in png')
parser.add_argument('--dividefakes', action='store_true', help='Divide fake contributions')
parser.add_argument('--fakevar', action='store_true', help='variation of fake fit')
args = parser.parse_args()

print("====== Plotter Initialization ======")
print(f"Analyzer : {args.analyzername} ({args.era}) , will be saved in {args.outputdir}")
print(f"Userflags : {args.userflags} ")
print(f"Divide Fakes : {args.dividefakes}")

bst_remove = ["Tight","Jets/Jet","AK4"]
rsv_remove = ["Loose","FatJet"]
presel_remove = ["ProperMTWR","ProperMeffWR","HighPt"]

debug = args.debugmode
willBlind = args.blind
onlyPNG = args.onlypng
wjgen = args.WJGen
fakev = args.fakevar
divfake = args.dividefakes

if wjgen not in ["MG","Sherpa"] :
    print(f"{wjgen} is not available")
    exit

print(f"Blinded : {willBlind} , OnlyPNG : {onlyPNG}, Debug : {debug}")
print(f"WJets Generator : {wjgen}")


l_vJetID = ["Tight"] 
l_vElID = ["Tight"]
l_vMuID = ["Tight"]


l_ID = [l_vJetID,l_vElID,l_vMuID]
IDcomb = list(itertools.product(*l_ID))


d_signals = {
    2000 : [50,TColor.GetColor("#94FC13")],
    4000 : [500,TColor.GetColor("#FF008E")],
    4800 : [50000,TColor.GetColor("#00FFD1")],
}


userflag = ""; savedirsuffix = ""
if args.userflags != "" : 
    userflag = f"{args.userflags}__"
    savedirsuffix = f"_{args.userflags}"

branchlist = ["__PromptTau__NonPromptLepton"]
SampleDir = f"{os.getenv('WRTau_Output')}/{args.input}"

# Multiboson+jet : Red~Orange 
# Multitop : Greenish
# QCD : Blue

# prompt_prompt

SampleDic = {

    "Boson" : ["Others",TColor.GetColor("#576CBC")],
    "Top" : ["t#bar{t}+tX", TColor.GetColor("#DE1A1A")],
    "Fakes" : ["Nonprompt",TColor.GetColor("#5FAD56")]

}

SampleDic = {

    "Boson_noVJets" : ["Others",TColor.GetColor("#5790fc")],
    "Top" : ["t#bar{t}+tX", TColor.GetColor("#DE1A1A")],
    "Fakes" : ["Nonprompt",TColor.GetColor("#f89c20")]

}

# regions to be plotted
l_SignalRegions = ["ResolvedSignalRegion_ElTau","ResolvedSignalRegion_MuTau",
                   "BoostedSignalRegion_ElTau", "BoostedSignalRegion_MuTau"]
plotsavedirname = f"{args.outputdir}{savedirsuffix}_Nevents"  

os.system(f"mkdir -p ../Plots/{plotsavedirname}/{args.era}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{args.era}")

h_nEv0 = TH1D("nEv_boson","nEv_boson",4,0.,4.)
h_nEv1 = TH1D("nEv_top","nEv_top",4,0.,4.)
h_nEv2 = TH1D("nEv_fakes","nEv_fakes",4,0.,4.)

l_hn = [h_nEv0,h_nEv1,h_nEv2]

hs = THStack(f"hs",f"hs")
h_stack = TH1D("h_stack","h_stack",4,0.,4.)

c = TCanvas("","",1000,1000)
l = TLegend(0.55,0.75,0.875,0.875)
l.SetNColumns(2)
latex = TLatex()
latex.SetNDC()
l.SetFillStyle(0)
l.SetBorderSize(0)

for i,samplename in enumerate(SampleDic) :
    print(i)
    f = TFile(f"{SampleDir}/{args.era}/{args.analyzername}_{samplename}.root")
    for j,region in enumerate(l_SignalRegions) : 
        if samplename == "Fakes" :
            h1 = f.Get(f"Central/{region}/Nevents") 
            if not h1 == None and region not in l_SignalRegions : 
                h1.Scale(getTauFakeNormalization(args.era,region))
            h2 = f.Get(f"Central/__PromptTau__NonPromptLepton/{region}/Nevents") 
            h = h1 + h2 if h1 is not None and h2 is not None else h1 if h1 is not None else h2 if h2 is not None else None
        else : h = f.Get(f"Central/__PromptTau__PromptLepton/{region}/Nevents")
        l_hn[i].SetBinContent(j+1,h.Integral())
        print(j,h.Integral())
    print(l_hn[i])
    #if i == 0 : h_stack = l_hn[i].Clone()
    #else : h_stack.Add(l_hn[i])
    l_hn[i].SetStats(0)
    l_hn[i].SetFillColorAlpha(SampleDic[samplename][1],0.95)
    l_hn[i].SetLineColor(kBlack)
    l_hn[i].GetXaxis().SetBinLabel(1, "#splitline{Resolved SR}{e#tau_{h} Channel}")
    l_hn[i].GetXaxis().SetBinLabel(2, "#splitline{Resolved SR}{#mu#tau_{h} Channel}")
    l_hn[i].GetXaxis().SetBinLabel(3, "#splitline{Boosted SR}{e#tau_{h} Channel}")
    l_hn[i].GetXaxis().SetBinLabel(4, "#splitline{Boosted SR}{#mu#tau_{h} Channel}")
    l_hn[i].GetXaxis().SetLabelSize(0.15)
    l_hn[i].GetYaxis().SetTitle("Events")
    l.AddEntry(l_hn[i],SampleDic[samplename][0],"f")
    hs.Add(l_hn[i])

h_stack = h_nEv0 + h_nEv1 + h_nEv2

h_stackerr = h_stack.Clone("hstackerr")
h_stackerr.SetStats(0)
h_stackerr.SetFillStyle(3144)
h_stackerr.SetFillColorAlpha(12,0.6)
h_stackerr.GetXaxis().SetLabelSize()

l.AddEntry(h_stackerr,"Stat. Unc","f")

c.cd()
c.SetLogy()
hs.SetTitle("")
hs.SetMinimum(0.01)
hs.SetMaximum(5000)
hs.Draw()
h_stackerr.Draw("e2&same")
l.Draw()

textSize = 0.625*gStyle.GetPadTopMargin()
latex.SetTextFont(61)
latex.SetTextSize(textSize*1.5)
latex.DrawLatex(0.15, 0.785,"CMS")

latex.SetTextFont(52)
latex.SetTextSize(0.7*textSize)
latex.DrawLatex(0.15, 0.74,"Simulation")

latex.SetTextFont(42)
latex.SetTextSize(0.6*textSize)
lumi = str(getLumi(str(args.era)))
latex.DrawLatex(0.55, 0.9175,lumi+" fb^{-1} (13 TeV, "+f"{str(args.era)})")



c.SaveAs("test.png")
c.Close()