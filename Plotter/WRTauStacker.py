import os, sys, argparse
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TLatex, TLegend, TH1F, kOrange, kRed, kGreen,kBlue, THStack, gROOT, TRatioPlot
from ROOT import TLegend, kBlack, gStyle
import itertools
gROOT.SetBatch(True)

def getLumi(dirname) :
    era = dirname.split("SKFlatOutput")[1].split("/")[3]
    if era == "2016preVFP" : return 19.5
    elif era == "2016postVFP" : return 16.8
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8

l_vJetID = ["Tight"]
l_vElID = ["Loose","Tight"]
l_vMuID = ["Loose","Tight"]
l_ID = [l_vJetID,l_vElID,l_vMuID]
IDcomb = list(itertools.product(*l_ID))


SampleDir = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_SR/2017/PreselOnly__"

SampleDic = {

    #"SingleTop" : ["Single Top", kBlue-7],
    "VV" : ["VV", kBlue-4],
    "SingleTop" : ["Single Top", kBlue-7],
    "WJets_MG" : ["W+Jets", kGreen-1 ],
    "TT" : ["Top Pair", kRed-9 ],
    "DYJets" : ["DY", kOrange+2 ],
    
}

# varname : [setlogy, rebin , xtitle,filename,xmin,xmax]

l_regions = ["Preselection","Preselection_hasAtLeast2AK4Jets","Preselection_isResolvedPreselection",
            "Preselection_hasAtLeast1AK8Jets","Preselection_isBoostedPreselection",
            "Preselection_hasAtLeast1LooseLeptons"]

VarDic = {

    "Cutflow" : [True,1,"Cutflow","Cutflow",0,5],
    "Preselection/MET" : [True,50,"#slash{E}_{T} (GeV)","MET",0.,1000.],
    "Preselection/Tauh_pT" : [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,1000.],
    "Preselection/Jets/FatJet_0_Pt" : [True,100,"Leading AK8 Jet Pt (GeV)","J0_Pt",0.,2500.],
    "Preselection/Jets/FatJet_0_Eta" : [True,2,"Leading AK8 Jet #eta","J0_Eta",-3.,3.],
    "Preselection/Jets/FatJet_0_LSF" : [True,5,"Leading AK8 Jet LSF_{3}","J0_LSF",0.,1.],
    "Preselection/Jets/Jet_0_Pt" : [True,100,"Leading AK4 Jet Pt (GeV)","j0_Pt",0.,2500.],
    "Preselection/Jets/Jet_0_Eta" : [True,2,"Leading AK4 Jet #eta","j0_Eta",-3.,3.],
    "Preselection/Jets/Jet_1_Pt" : [True,100,"Subleading AK4 Jet Pt (GeV)","j1_Pt",0.,2000.],
    "Preselection/Jets/Jet_1_Eta" : [True,2,"Subleading AK4 Jet #eta","j1_Eta",-3.,3.],
    "Preselection/HighPtTight/Lepton_0_Pt" : [True,50,"Leading Tight Lepton Pt (GeV)","TightLep0_Pt",0.,1000.],
    "Preselection/HighPtTight/Lepton_0_Eta" : [True,2,"Leading Tight Lepton #eta","TightLep0_Eta",-3.,3.],
    "Preselection/HighPtTight/Lepton_1_Pt" : [True,20,"Subleading Tight Lepton Pt (GeV)","TightLep1_Pt",0.,500.],
    "Preselection/HighPtTight/Lepton_1_Eta" : [True,2,"Subleading Tight Lepton #eta","TightLep1_Eta",-3.,3.],
    "Preselection/HighPtLoose_TauVeto/Lepton_0_Pt" : [True,50,"Leading Loose Lepton Pt (GeV)","LooseLep0_Pt",0.,1000.],
    "Preselection/HighPtLoose_TauVeto/Lepton_0_Eta" : [True,2,"Leading Loose Lepton #eta","LooseLep0_Eta",-3.,3.],
    "Preselection/nFatJet" : [True,1,"Number of AK8 Jets","nAK8",0.,4.],
    "Preselection/nJets" : [True,1,"Number of AK4 Jets","nAK4",0.,4.],
    "Preselection/dRJ0Tau" : [True,3,"#DeltaR(J_{lead},#tau_{h})","dRJ0Tau",0.,6.],
}

#l_region = list(range(1,5))
#l_nocut = [ str(i)+"_notaucut" for i in l_region]
#l_region += l_nocut +["0"]

#for i in l_region :
#    #print(i)
#    for obj in ["Tau","Muon","Jet","BJet"] :
#        os.system(f"mkdir -p TauStudyPlots/Region{i}/{obj}")

debug = False


for (vJ,vEl,vMu) in IDcomb :
    TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"
    for var in VarDic : 
        if debug : print(f"var : {var}")
        os.system(f"mkdir -p Plotter/SingleLeptonTrigger/Preselection_AK8Req/{TauID}")
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
        for samplename in SampleDic :
            if debug : print(f"{i} : {samplename}")
            f = TFile(f"{SampleDir}/WRTau_SR_{samplename}.root")
            if debug : print(f"{samplename} file : {f}")
            h = f.Get(f"WRTauStudy/SingleLeptonTrigger/{TauID}/{var}")
            if h == None : continue
            if debug : print(f"{samplename} hist : {h}")
            gROOT.cd()
            h_tmp = h.Clone()
            h_tmp.Rebin(VarDic[var][1])
            h_tmp.GetYaxis().SetMaxDigits(2)
            h_tmp.GetXaxis().SetLabelSize(0)
            h_tmp.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
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
        f_data = TFile(f"{SampleDir}/DATA/WRTau_SR_DATA.root")
        h_data = f_data.Get(f"WRTauStudy/SingleLeptonTrigger/{TauID}/{var}")
        if h_data == None : continue

        if debug : print(f"DATA file : {f}")
        if debug : print(h_data)
        hs.Draw()
        hs.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
        hs.GetXaxis().SetLabelSize(0)
        hs.GetYaxis().SetTitle("Events/Bin")
        hs.GetYaxis().SetTitleSize(0.0425)
        hs.GetYaxis().SetTitleOffset(1.025)
        

        if debug : print(hs)

        h_data.SetStats(0) 
        h_data.SetMarkerStyle(8)
        h_data.GetXaxis().SetLabelSize(0)
        h_data.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][5])
        h_data.Rebin(VarDic[var][1])
        l.AddEntry(h_data,"Data","lp")

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
            h_data.GetYaxis().SetRangeUser(0.1,max(l_max)*1000)
            hs.SetMinimum(0.1); hs.SetMaximum(max(l_max)*1000)
            pad_up.SetLogy()

        hs.Draw("hist"); h_data.Draw("hist&p&same"); h_data_error.Draw("e2&f&same"); 

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
        l.Draw()
        pad_down.cd()
        ratio.Draw("p&hist")
        ratio_syst.Draw("e2&f&same")
        c.cd()
        pad_up.Draw()
        pad_down.Draw()

        c.SaveAs(f"Plotter/SingleLeptonTrigger/Preselection_AK8Req/{TauID}/{VarDic[var][3]}.png")
        c.Close()
