from ROOT import *
import os,array
from utils import *

stamp = "240716"
l_era = ["2017"]

pt_bins_ = [190,220,250,350,450,600,1000]
pt_bins = array.array('d',pt_bins_)

pt_bins_b_ = [190,200,220,250,300,350,475,600]
pt_bins_b = array.array('d',pt_bins_b_)
os.system(f"mkdir -p FakeFactorRatio/{stamp}")

for era in l_era :
    output_file = TFile(f"FakeFactorRatio/{stamp}/{era}.root", 'RECREATE')
    for nj in [0,1,2] :
        
        nTT, nQCD, nPrompt, nData = 0. , 0. , 0. , 0.
        f_data   = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/DATA/WRTau_Analyzer_DATA.root")
        f_prompt = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_Prompt.root")
        f_ttbar  = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_TT.root")
        f_st     = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_ST.root")

        if check(f_prompt,f"Central/__PromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT") :
            h_prompt_resolved = f_prompt.Get(f"Central/__PromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
        else : h_prompt_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
        if check(f_prompt,f"Central/__PromptTau/BoostedSignalRegion_j{nj}/Tauh_pT") :
            h_prompt_boosted  = f_prompt.Get(f"Central/__PromptTau/BoostedSignalRegion_j{nj}/Tauh_pT").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
        else : h_prompt_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

        h_prompt = h_prompt_boosted + h_prompt_resolved

        if check(f_ttbar,f"Central/__NonPromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT") :
            h_ttbar_resolved = f_ttbar.Get(f"Central/__NonPromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
        else : h_ttbar_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
        if check(f_ttbar,f"Central/__NonPromptTau/BoostedSignalRegion_j{nj}/Tauh_pT") :
            h_ttbar_boosted  = f_ttbar.Get(f"Central/__NonPromptTau/BoostedSignalRegion_j{nj}/Tauh_pT").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
        else : h_ttbar_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

        h_ttbar = h_ttbar_resolved + h_ttbar_boosted

        if check(f_st,f"Central/__NonPromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT") :
            h_st_resolved = f_st.Get(f"Central/__NonPromptTau/ResolvedSignalRegion_j{nj+2}/Tauh_pT").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
        else : h_st_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
        if check(f_st,f"Central/__NonPromptTau/BoostedSignalRegion_j{nj}/Tauh_pT") :
            h_st_boosted  = f_st.Get(f"Central/__NonPromptTau/BoostedSignalRegion_j{nj}/Tauh_pT").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
        else : h_st_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

        h_st = h_st_resolved + h_st_boosted

        if check(f_data,f"Central/ResolvedSignalRegion_j{nj+2}/Tauh_pT") :
            h_data_resolved = f_data.Get(f"Central/ResolvedSignalRegion_j{nj+2}/Tauh_pT").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
        else : h_data_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
        if check(f_data,f"Central/BoostedSignalRegion_j{nj}/Tauh_pT") :
            h_data_boosted  = f_data.Get(f"Central/BoostedSignalRegion_j{nj}/Tauh_pT").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
        else : h_data_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

        h_data = h_data_resolved + h_data_boosted

        h_fTT_r = TH1D(f"Resolved_j{nj+2}_TT","",len(pt_bins_)-1,pt_bins)
        h_fTT_b = TH1D(f"Boosted_j{nj}_TT","",len(pt_bins_b_)-1,pt_bins_b)
        h_fTT = TH1D(f"Inclusive_j{nj}_TT","",len(pt_bins_)-1,pt_bins)
        h_fQCD_r = TH1D(f"Resolved_j{nj+2}_QCD","",len(pt_bins_)-1,pt_bins)
        h_fQCD_b = TH1D(f"Boosted_j{nj}_QCD","",len(pt_bins_b_)-1,pt_bins_b)
        h_fQCD = TH1D(f"Inclusive_j{nj}_QCD","",len(pt_bins_)-1,pt_bins)
        
#        print(h_data.GetNbinsX(),h_ttbar.GetNbinsX(),h_prompt.GetNbinsX())
        for i in range(1,h_data.GetNbinsX()+1) :
            nData     = h_data.GetBinContent(i)
            nTT       = h_ttbar.GetBinContent(i)
            nST       = h_st.GetBinContent(i)
            nPrompt   = h_prompt.GetBinContent(i)
            nQCD      = max(0., nData-nTT-nPrompt)

            nData_r   = h_data_resolved.GetBinContent(i)
            nTT_r     = h_ttbar_resolved.GetBinContent(i)
            nST_r     = h_st_resolved.GetBinContent(i)
            nPrompt_r = h_prompt_resolved.GetBinContent(i)
            nQCD_r    = max(0., nData_r-nTT_r-nPrompt_r)

            nData_b   = h_data_boosted.GetBinContent(i)
            nTT_b     = h_ttbar_boosted.GetBinContent(i)
            nST_b     = h_st_boosted.GetBinContent(i)
            nPrompt_b = h_prompt_boosted.GetBinContent(i)
            nQCD_b    = max(0., nData_b-nTT_b-nPrompt_b)

            #print("Inclusive",i,nTT,nQCD,nData)
            #print("Resolved",i,nST_r,nTT_r,nQCD_r,nData_r)
            #print("Boosted",i,nST_b,nTT_b,nQCD_b,nData_b)
            if nData_b != 0 :
                fQCD_b = nQCD_b/nData_b
                fTT_b = nTT_b/nData_b
                norm_b = 1./(fQCD_b+fTT_b)
                fQCD_b *= norm_b
                fTT_b *= norm_b
                h_fTT_b.SetBinContent(i,fTT_b)
                h_fQCD_b.SetBinContent(i,fQCD_b)
                #print("Boosted Ratio : ",i,fQCD_b,fTT_b)

            if nData_r != 0 :
                fQCD_r = nQCD_r/nData_r
                fTT_r = nTT_r/nData_r
                norm_r = 1./(fQCD_r + fTT_r)
                fQCD_r *= norm_r 
                fTT_r *= norm_r
                h_fTT_r.SetBinContent(i,fTT_r)
                h_fQCD_r.SetBinContent(i,fQCD_r)
                #print("Resolved Ratio : ",i,fQCD_r,fTT_r)


            if nData != 0 :
                fQCD = nQCD/nData
                fTT = nTT/nData
                norm = 1./(fQCD + fTT)
                fQCD *= norm_r 
                fTT *= norm_r
                h_fTT.SetBinContent(i,fTT)
                h_fQCD.SetBinContent(i,fQCD)

        original_directory = gDirectory.GetPath()
        output_file.cd()
        h_fTT_b.Write()
        h_fQCD_b.Write()
        h_fTT_r.Write()
        h_fQCD_r.Write()
        h_fTT.Write()
        h_fQCD.Write()
        gDirectory.cd(original_directory)

        c   = TCanvas(f"{era}_inclusive_j{nj}",f"{era}_inclusive_j{nj}",1000,1000)
        c_r = TCanvas(f"{era}_resolved_j{nj+2}",f"{era}_resolved_j{nj}",1000,1000)
        c_b = TCanvas(f"{era}_boosted_j{nj}",f"{era}_boosted_j{nj}",1000,1000)

        h_dummy = TH1D("","",len(pt_bins_)-1,pt_bins)
        h_dummy.GetYaxis().SetRangeUser(0.01,1.0)
        h_dummy.SetStats(0)
        h_dummy.GetXaxis().SetTitle("p_{T}^{#tau_{h}} [GeV]")
        h_dummy.GetXaxis().SetTitleSize(0.045)
        h_dummy.GetXaxis().SetLabelSize(0.04)
        h_dummy.GetYaxis().SetTitle("Ratio")
        h_dummy.GetYaxis().SetTitleOffset(1.)
        h_dummy.GetYaxis().SetTitleSize(0.045)

        h_dummy_b = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)
        h_dummy_b.GetYaxis().SetRangeUser(0.01,1.0)
        h_dummy_b.SetStats(0)

        c_r.cd()
        l_r = TLegend(0.65,0.7,0.875,0.8)
        l_r.AddEntry(h_fTT_r,"Top Pair","f")
        l_r.AddEntry(h_fQCD_r,"QCD","f")
        l_r.SetFillStyle(0)
        l_r.SetBorderSize(0)
        l_r.Draw()
        h_dummy.Draw("h")
        
        #c_r.SetLogx()
        #c_r.SetLogy()
        hs_r = THStack(f"hs_{era}_resolved","")
        h_fTT_r.SetFillColor(kRed-7)
        h_fTT_r.SetLineColor(kBlack)
        hs_r.Add(h_fTT_r)
        h_fQCD_r.SetFillColor(kViolet-9)
        h_fQCD_r.SetLineColor(kBlack)
        hs_r.Add(h_fQCD_r)
        #hs_r.GetXaxis().SetRangeUser(190,1000)
        hs_r.Draw('same')
        drawLatexNew2("Resolved",era,nj+2)
        l_r.Draw()
        c_r.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Resolved_j{nj+2}.pdf")
        c_r.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Resolved_j{nj+2}.png")

        c_b.cd()
        l_b = TLegend(0.65,0.7,0.875,0.8)
        l_b.AddEntry(h_fTT_b,"Top Pair","f")
        l_b.AddEntry(h_fQCD_b,"QCD","f")
        l_b.SetFillStyle(0)
        l_b.SetBorderSize(0)
        l_b.Draw()
        h_dummy_b.Draw("h")
        
        #c_b.SetLogx()
        #c_b.SetLogy()
        hs_b = THStack(f"hs_{era}_boosted","")
        h_fTT_b.SetFillColor(kRed-7)
        h_fTT_b.SetLineColor(kBlack)
        hs_b.Add(h_fTT_b)
        h_fQCD_b.SetFillColor(kViolet-9)
        h_fQCD_b.SetLineColor(kBlack)
        hs_b.Add(h_fQCD_b)
        #hs_r.GetXaxis().SetRangeUser(190,1000)
        hs_b.Draw('same')
        drawLatexNew2("Boosted",era,nj)
        l_b.Draw()
        c_b.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Boosted_j{nj}.pdf")
        c_b.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Boosted_j{nj}.png")

        c.cd()
        l = TLegend(0.65,0.7,0.875,0.8)
        l.AddEntry(h_fTT,"Top Pair","f")
        l.AddEntry(h_fQCD,"QCD","f")
        l.SetFillStyle(0)
        l.SetBorderSize(0)
        h_dummy.Draw("h")
        l.Draw()
        #c.SetLogx()
        #c.SetLogy()
        hs = THStack(f"hs_{era}_inclusive","")
        h_fTT.SetFillColor(kRed-7)
        h_fTT.SetLineColor(kBlack)
        hs.Add(h_fTT)
        h_fQCD.SetFillColor(kViolet-9)
        h_fQCD.SetLineColor(kBlack)
        hs.Add(h_fQCD)
        #hs_r.GetXaxis().SetRangeUser(190,1000)
        hs_r.Draw('same')
        #drawLatexNew("Inclusive",era,DM)
        l.Draw()
        c.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Inclusive_j{nj}.pdf")
        c.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Inclusive_j{nj}.png")
