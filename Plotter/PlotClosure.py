import os, sys, argparse, itertools, array, argparse
from ROOT import *
from utils import *
from math import sqrt
from datetime import datetime 
import tracemalloc
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2023) v2.213345661')
parser.add_argument('-a', dest='analyzername', type=str, help='Analyzer name',default="WRTau_Analyzer")
parser.add_argument('-i', dest='input', type=str, help='Input directory timestamp')
parser.add_argument('-e', dest='era', type=str, help='Era to plot', default=2017)
parser.add_argument('-o', dest='outputdir', type=str, help='Output directory name',default=default_outputdir)
parser.add_argument('--blind', action='store_true', help='Blind sensitive datapoints')
parser.add_argument('--onlypng', action='store_true', help='Only save in png')
parser.add_argument('--dividefakes', action='store_true', help='Divide fake contributions')
args = parser.parse_args()

analyzername, inputstamp , era, outputstamp = args.analyzername , args.input, args.era , args.outputdir

SampleDic = {

    "Boson_noVJets" : ["Others",TColor.GetColor("#5790fc")],
    "Top" : ["t#bar{t}+tX", TColor.GetColor("#DE1A1A")],

}

l_regions_presels = ["BoostedSignalRegionMETInvertMTSame","ResolvedSignalRegionMETInvertMTSame"]
l_regions = [f"{region}{suffix}" for region in l_regions_presels for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

os.system(f"mkdir -p FakeClosure/{outputstamp}/{era}")
SampleDir = f"{os.getenv('WRTau_Output')}/{inputstamp}"

for region in l_regions : 
    TauID = "vJetTight_vElTight_vMuTight"
    channel = ""

    if "ElTau" in region : channel = "e#tau_{h}"
    elif "MuTau" in region : channel = "#mu#tau_{h}"
    else : channel = "e#tau_{h}+#mu#tau_{h}"

    VarDic = MainVarDic[(era,region)]
    VarDic = {f"{region}/ProperMeffWR" : VarDic[f"{region}/ProperMeffWR"]}
    
    region_latex = ""

    if "Boosted" in region :
        region_latex = f"Boosted QCD Fake MR^{{SR-Like}}"
    else :
        region_latex = f"Resolved QCD Fake MR^{{SR-Like}}"

    for var in VarDic : 
        c = TCanvas(f"c_{region}_{TauID}_{var}",f"c_{region}_{TauID}_{var}",720,800)
        pad_up = TPad(f"pu_{region}_{TauID}_{var}",f"pu_{region}_{TauID}_{var}",0,0.25,1,1)
        pad_up.SetBottomMargin(0.02)
        pad_down = TPad(f"pd_{region}_{TauID}_{var}",f"pd_{region}_{TauID}_{var}",0,0,1,0.25)
        pad_down.SetGrid(1)
        pad_down.SetTopMargin(0.0315)
        pad_down.SetBottomMargin(0.3)

        l_hPrompt = []
        h_PromptSum , h_Fake , h_Data = TH1D(), TH1D(), TH1D()
        #print(var,VarDic[var])
        # sum prompt
        for samplename in SampleDic :
            f = TFile(f"{SampleDir}/{era}/{analyzername}_{samplename}.root")
            if check(f,f"Central/__PromptTau__PromptLepton/{var}") : 
                h_temp1_ = f.Get(f"Central/__PromptTau__PromptLepton/{var}").Clone(f"{var}{samplename}{era}P")
                if len(VarDic[var]) == 8 : h_temp1 = h_temp1_.Rebin(len(VarDic[var][6])-1,f"{var}{samplename}{era}P",array.array('d',VarDic[var][6]))
                else : h_temp1 = h_temp1_.Rebin(VarDic[var][1]).Clone("")
                l_hPrompt.append(h_temp1)
                h_temp1.SetDirectory(0)
            if check(f,f"Central/__PromptTau__NonPromptLepton/{var}") : 
                h_temp2_ = f.Get(f"Central/__PromptTau__NonPromptLepton/{var}").Clone(f"{var}{samplename}{era}NP")
                if len(VarDic[var]) == 8 :  h_temp2 = h_temp2_.Rebin(len(VarDic[var][6])-1,f"{var}{samplename}{era}P",array.array('d',VarDic[var][6]))
                else : h_temp2 = h_temp2_.Rebin(VarDic[var][1]).Clone("")
                l_hPrompt.append(h_temp2)
                h_temp2.SetDirectory(0)

        #print(l_hPrompt)
        if len(l_hPrompt) > 0 :
            for i,h in enumerate(l_hPrompt) :
                if i == 0 : 
                    h_PromptSum = h.Clone(f"{var}{era}PromptSum")
                else : h_PromptSum.Add(h)
        
        f_data = TFile(f"{SampleDir}/{era}/DATA/{analyzername}_DATA.root")
        h_data_tmp_ = f_data.Get(f"Central/{var}").Clone(f"{var}{era}Data__")
        if len(VarDic[var]) == 8 : h_data_tmp = h_data_tmp_.Rebin(len(VarDic[var][6])-1,f"{var}{era}Data_",array.array('d',VarDic[var][6]))
        else : h_data_tmp = h_data_tmp_.Rebin(VarDic[var][1])

        h_Data = h_data_tmp.Clone(f"{var}{era}Data")
        h_Data.Add(h_PromptSum,-1)

        f_Fake = TFile(f"{SampleDir}/{era}/{analyzername}_Fakes.root")
        h_Fake_tmp_ = f_Fake.Get(f"Central/{var}").Clone(f"{var}{era}Fake__")
        if len(VarDic[var]) == 8 : h_Fake_tmp = h_Fake_tmp_.Rebin(len(VarDic[var][6])-1,f"{var}{era}Fake_",array.array('d',VarDic[var][6]))
        else : h_Fake_tmp = h_Fake_tmp_.Rebin(VarDic[var][1])

        maxi = max( h_Fake.GetMaximum(), h_Data.GetMaximum() )

        h_Fake = h_Fake_tmp.Clone(f"{var}{era}Fake")
        h_Fake.SetStats(0)
        h_Fake.SetFillColorAlpha(TColor.GetColor("#f89c20"),0.75)

        h_Data.Sumw2(False)
        h_Data.SetBinErrorOption(TH1.kPoisson)
        h_Data.SetMarkerStyle(8)
        h_Data.SetLineColor(kBlack)

        h_Fake_err = h_Fake.Clone(f"{var}{era}FakeError")
        h_Fake_err.SetStats(0)
        h_Fake_err.SetFillStyle(3144)
        h_Fake_err.SetFillColorAlpha(kBlack,0.6)

        for h in [h_Fake,h_Data,h_Fake_err] : 
            h.GetXaxis().SetLabelSize(0)
            h.GetYaxis().SetRangeUser(1e-1,maxi*1000)

        ratio = h_Data.Clone(f"{var}{era}ratio")
        pred = h_Fake.Clone(f"{var}{era}pred")
        ratio.Divide(pred)
        ratio.SetStats(0)
        ratio_err = ratio.Clone(f"{var}{era}ratio_err")

        for r in [ratio,ratio_err]:
            r.SetTitle("")
            r.GetXaxis().SetTitle(VarDic[var][2])
            r.GetXaxis().SetTitleSize(0.15)
            r.GetXaxis().SetLabelSize(0.125)
            r.GetXaxis().SetTitleOffset(0.85)
            r.GetYaxis().SetRangeUser(0,2.)
            r.GetYaxis().SetLabelSize(0.1)
            r.GetYaxis().SetTitle("Obs./Pred.")
            r.GetYaxis().SetTitleSize(0.125)
            r.GetYaxis().SetTitleOffset(0.35)
            r.GetYaxis().CenterTitle(True)
            r.GetYaxis().SetNdivisions(204)
            r.SetMarkerStyle(8)   
        
        ratio_err.SetStats(0)
        ratio_err.SetFillColorAlpha(TColor.GetColor('#f89c20'),0.8)
        ratio_err.SetFillStyle(1001)
        ratio_err.SetMarkerStyle(20)
        ratio_err.SetMarkerColorAlpha(kBlack,0)

        textSize = 0.625*gStyle.GetPadTopMargin()

        l = TLegend(0.475,0.675,0.875,0.875)
        l.SetNColumns(1)
        l.SetFillStyle(0)
        l.SetBorderSize(0)
        l.AddEntry(h_Fake,"Predicted #tau_{h} Nonprompt",'f')
        l.AddEntry(h_Data,"Observed - Prompt MC", 'lep')

        pad_up.cd()
        pad_up.SetLogy()
        h_Fake.Draw("hist&f&e2")
        h_Fake_err.Draw("e2&f&same")
        h_Data.Draw("same&hist&e1&p")

        latex = TLatex()
        latex.SetNDC()
        latex.SetTextFont(61)
        latex.SetTextSize(textSize*1.5)
        latex.DrawLatex(0.15, 0.795,"CMS")
        latex.SetTextFont(52)
        latex.SetTextSize(0.7*textSize)
        latex.DrawLatex(0.15, 0.75,"Work In Progress")
        latex.DrawLatex(0.15, 0.715,"Preliminary")
        latex.SetTextFont(42)
        latex.SetTextSize(0.6*textSize)
        latex.SetTextAlign(31)
        lumi = str(getLumi(str(args.era)))
        latex.DrawLatex(0.885, 0.9175,lumi+" fb^{-1} (13 TeV)")
        latex.SetTextAlign(13)
        latex.SetTextFont(42)
        latex.SetTextSize(0.575*textSize)
        latex.DrawLatex(0.15, 0.65,f"{region_latex}")
        latex.SetTextSize(0.575*textSize)
        latex.DrawLatex(0.15, 0.615,f"{channel} Channel")
        l.Draw()

        pad_down.cd()
        ratio_err.Draw("e2&f")
        ratio.Draw("p&hist&same")

        lineUp = TLine(900,1.3,2000,1.3)
        lineDown = TLine(900,0.7,2000,0.7)
        for line in [lineUp,lineDown]:
            line.SetLineStyle(9)
            line.SetLineColor(kRed)
            line.SetLineWidth(3)
        l3 = TLegend(0.45,0.8,0.9,0.965)
        l3.SetNColumns(2)
        l3.SetFillStyle(1001)
        #l3.SetBorderSize(0)
        l3.AddEntry(ratio,"Obs./Pred.","p")
        l3.AddEntry(ratio_err,"Stat. Unc.","lpf") 
        l3.Draw()
        lineUp.Draw()
        lineDown.Draw()

        c.cd()
        pad_up.Draw()
        pad_down.Draw()

        c.SaveAs(f"FakeClosure/{outputstamp}/{era}/{region}_{var.split('/')[-1]}.png")
        c.SaveAs(f"FakeClosure/{outputstamp}/{era}/{region}_{var.split('/')[-1]}.pdf")