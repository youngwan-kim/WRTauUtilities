import os, sys, argparse
from ROOT import *
import itertools, array
gROOT.SetBatch(True)

def getLumi(dirname) :
    era = dirname.split("SKFlatOutput")[1].split("/")[3]
    if era == "2016preVFP" : return 19.5
    elif era == "2016postVFP" : return 16.8
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8

l_vJetID = ["Medium","Tight"]
l_vElID = ["VVLoose","Tight"]
l_vMuID = ["VVLoose","Medium","Tight"]

l_vJetID = ["VLoose","Medium","Tight"]
l_vElID = ["VVVLoose","Tight"]
l_vMuID = ["VLoose","Tight"]


l_ID = [l_vJetID,l_vElID,l_vMuID]
IDcomb = list(itertools.product(*l_ID))


SampleDir = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/ZTauTau/2017/PromptLepton__PromptTau__/"

SampleDic = {

    "QCD" : ["QCD",TColor.GetColor("#1F487E")],
    "VVV" : ["VVV",TColor.GetColor("#4E0110")],
    "VV" : ["VV", TColor.GetColor("#DE1A1A")],
    "WJets_MG_TauHLT" : ["W+Jets", TColor.GetColor("#F2C14E")],
    "ST" : ["Single Top", TColor.GetColor("#04471C")],
    "TT" : ["Top Pair", TColor.GetColor("#5FAD56") ],
    "DYJets_MG_TauHLT" : ["DY", TColor.GetColor("#F26419") ],
    
}

SampleDic["TauNonprompt"] = ["Nonprompt #tau_{h}",TColor.GetColor("#19376D")]
SampleDic["LeptonNonprompt"] = ["Nonprompt #mu",TColor.GetColor("#576CBC")]
SampleDic["BothNonprompt"] = ["Nonprompt (Both)",TColor.GetColor("#A5D7E8")]


l_regions = ["ZTauTau"]

debug = False

for region in l_regions :
    for (vJ,vEl,vMu) in IDcomb :
        TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"

        VarDic = {
            "ZCandMass" : [True,2,"m(#mu#tau_{h})","ZCandMass",50,130],
            "ZCandMT" : [True,2,"m_{T}(#mu#tau_{h})","ZCandMT",0,200],
            "dRtm" : [True,3,"#DeltaR(#mu#tau_{h})","dRtm",0,6],
        }

        channel = ""

        for var in VarDic : 
            ditauchannel = "#mu#tau_{h} channel"
            #if not "noTauWeight" in var : channel = ditauchannel + " #times Tau weight"
            #else : channel = ditauchannel
            if debug : print(f"var : {var}")
            savedir = f"TauIDTestZPeak_NewCuts"
            os.system(f"mkdir -p {savedir}")
            c = TCanvas("c","",720,800)
            if debug : print(f"canvas : {c}")
            l = TLegend(0.385,0.75,0.865,0.875)
            l.SetNColumns(3)
            latex = TLatex()
            latex.SetNDC()
            l.SetFillStyle(0)
            l.SetBorderSize(0)
            pad_up = TPad("pad_up","",0,0.25,1,1)
            pad_up.SetBottomMargin(0.02)
            pad_down = TPad("pad_down","",0,0,1,0.25)
            pad_down.SetGrid(1)
            pad_down.SetTopMargin(0.0315)
            pad_down.SetBottomMargin(0.3)
            hs = THStack(f"hs{var}","")
            i = 0
            h_stack = TH1D()
            for samplename in SampleDic :
                if debug : print(f"{i} : {samplename}")
                f = TFile(f"{SampleDir}/ZTauTau_{samplename}.root")
                if debug : print(f"{samplename} file : {f}")
                h = f.Get(f"ZTauTau/{TauID}/{var}")
                if h == None : continue
                if debug : print(f"{samplename} hist : {h}")
                gROOT.cd()
                #h_tmp = h.Clone()
                if len(VarDic[var]) > 6 : h_tmp = h.Clone().Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                else : h_tmp = h.Clone().Rebin(VarDic[var][1])
                h_tmp.GetYaxis().SetMaxDigits(2)
                h_tmp.GetXaxis().SetLabelSize(0)
                h_tmp.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
                h_tmp.Scale(1.08)
                if i == 0 :
                    h_stack = h_tmp.Clone()
                else : h_stack.Add(h_tmp)
                h_tmp.SetStats(0); h_tmp.SetFillColorAlpha(SampleDic[samplename][1],0.6); h_tmp.SetLineColor(kBlack)
                hs.Add(h_tmp)
                l.AddEntry(h_tmp,SampleDic[samplename][0],"lf")
                i += 1
                h_stack.GetXaxis().SetLabelSize(0)
                h_stack.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
                if debug : print(f"THStack : {h_stack}")

            h_stackerr = h_stack.Clone(f"{region}_{TauID}_{var}_hserr")
            h_stackerr.SetStats(0)
            h_stackerr.SetFillStyle(3144)
            h_stackerr.SetFillColorAlpha(12,0.6)
            h_stackerr.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            h_stackerr.GetXaxis().SetLabelSize()
            f_data = TFile(f"{SampleDir}/DATA/ZTauTau_DATA.root")
            h_data_tmp = f_data.Get(f"ZTauTau/{TauID}/{var}")
            if h_data_tmp == None : continue
            if debug : print(f"DATA file : {f}")
            #if debug : print(h_data)
            hs.Draw()
            hs.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            hs.GetXaxis().SetLabelSize(0)
            hs.GetYaxis().SetTitle("Events/Bin")
            hs.GetYaxis().SetTitleSize(0.0425)
            hs.GetYaxis().SetTitleOffset(1.025)
            if debug : print(hs)
            if len(VarDic[var]) > 6 : h_data = h_data_tmp.Clone().Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
            else : h_data = h_data_tmp.Clone().Rebin(VarDic[var][1])
            h_data.SetStats(0) 
            h_data.SetMarkerStyle(8)
            h_data.SetFillColorAlpha(12,0.6)
            h_data.SetFillStyle(3144)
            h_data.SetLineColor(kBlack)
            h_data.GetXaxis().SetLabelSize(0)
            h_data.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
            #h_data.Rebin(VarDic[var][1])
            l.AddEntry(h_data,"Data+Stat.","lpf")
            h_data_error = h_data.Clone("data_err")
            h_data_error.SetFillColorAlpha(12,0.6)
            h_data_error.SetFillStyle(3144)
            h_data_error.GetXaxis().SetLabelSize(0)
            h_data_error.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
            ratio = h_stack.Clone("ratio")
            data = h_data.Clone("data")
            ratio.Divide(data)
            ratio.SetStats(0)
            if debug : print(ratio)
            ratio_syst = ratio.Clone("ratio_syst")
            ratio_syst.SetStats(0)
            ratio_syst.SetFillColorAlpha(12,0.6)
            ratio_syst.SetFillStyle(3144)
            ratio.SetTitle("")
            ratio.GetXaxis().SetTitle(VarDic[var][2])
            ratio.GetXaxis().SetTitleSize(0.15)
            ratio.GetXaxis().SetLabelSize(0.125)
            ratio.GetXaxis().SetTitleOffset(0.85)
            ratio.GetYaxis().SetRangeUser(0,2)
            ratio.GetYaxis().SetLabelSize(0.1)
            ratio.GetYaxis().SetTitle("Pred./Obs.")
            ratio.GetYaxis().SetTitleSize(0.125)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetYaxis().CenterTitle(True)
            ratio.GetYaxis().SetNdivisions(204)
            ratio.SetMarkerStyle(7)   
            l_max = [] ; l_max.append(hs.GetMaximum()) ; l_max.append(h_data.GetMaximum())
            pad_up.cd()
            h_data.GetYaxis().SetRangeUser(0,max(l_max)*1.8)
            hs.SetMinimum(0); hs.SetMaximum(max(l_max)*1.8)
            if VarDic[var][0] :
                h_data.GetYaxis().SetRangeUser(0.1,max(l_max)*5000)
                hs.SetMinimum(0.1); hs.SetMaximum(max(l_max)*5000)
                pad_up.SetLogy()
            hs.Draw("hist"); h_stackerr.Draw("e2&f&same"); h_data.Draw("hist&e1&p&same"); #  

            # Latex input
            textSize = 0.625*gStyle.GetPadTopMargin()
            latex.SetTextFont(61)
            latex.SetTextSize(textSize)
            latex.DrawLatex(0.15, 0.815,"CMS")
            latex.SetTextFont(52)
            latex.SetTextSize(0.75*textSize)
            latex.DrawLatex(0.15, 0.765,"Preliminary")
            latex.SetTextFont(42)
            latex.SetTextSize(0.6*textSize)
            lumi = str(getLumi(SampleDir))
            latex.DrawLatex(0.68, 0.9175,lumi+" fb^{-1} (13 TeV)")
            latex.SetTextFont(42)
            latex.SetTextSize(0.65*textSize)
            latex.DrawLatex(0.15, 0.7,f"{channel}")
            latex.SetTextSize(0.6*textSize)
            latex.DrawLatex(0.145, 0.9175,f"{TauID}")
            


            l.Draw()
            pad_down.cd()
            ratio.Draw("p&hist")
            ratio_syst.Draw("e2&f&same")
            c.cd()
            pad_up.Draw()
            pad_down.Draw()
            c.SaveAs(f"{savedir}/{TauID}_{VarDic[var][3]}.png")
            c.Close()