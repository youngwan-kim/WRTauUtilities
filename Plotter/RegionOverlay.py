from ROOT import *

# Create the first TH2D histogram

signals = {
    2000 : [100,200,400,600,1000,1400,1800,1900]
}

era = 2017

mcut = 900

line_MET = TLine(100,300,100,2200)
line_var  = TLine(0,mcut,900,mcut)
line_MET.SetLineStyle(2)
line_var.SetLineStyle(2)
line_MET.SetLineWidth(2)
line_var.SetLineWidth(2)

for region in ["Boosted","Resolved"] :
    for lep in ["MuTau","ElTau"] :
        f_bkg = TFile(f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/2DScan__ST__/WRTau_Analyzer_Bkg.root")
        h_bkg_MCPrompt    = f_bkg.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_ST").Rebin2D(50,100)
        h_bkg_MCNonprompt = f_bkg.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_ST").Rebin2D(50,100)
        h_bkg = h_bkg_MCPrompt.Clone(f"{era}{region}{lep}")
        h_bkg.Add(h_bkg_MCNonprompt)
        nBkg = h_bkg.Integral()
        if lep == "ElTau" : lepstr = "e#tau_{h}"
        elif lep == "MuTau" : lepstr = "#mu#tau_{h}"
    
        for mwr in signals :
            for mn in signals[mwr] :
                f_Signal = TFile(f"/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/2DScan__ST__/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
                h_Signal = f_Signal.Get(f"Central/Benchmark{region}Preselection_{lep}/MET_ST").Rebin2D(50,100)
                nSig = h_Signal.Integral()
                h_Signal.Scale(nBkg/nSig)
                scale = nBkg/nSig
                canvas = TCanvas("", "", 1000, 1000)
                canvas.SetBottomMargin(0.125)
                canvas.SetLeftMargin(0.125)
                hs = THStack()
                h_bkg.SetFillColorAlpha(kBlue, 0.65)
                hs.Add(h_bkg)
                h_Signal.SetFillColorAlpha(kRed, 0.65)
                hs.Add(h_Signal)
                hs.Draw()
                hs.GetXaxis().SetRangeUser(0,900)
                hs.GetXaxis().SetLabelSize(0.03)
                hs.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
                hs.GetXaxis().SetTitleSize(0.045)
                hs.GetYaxis().SetLabelSize(0.03)
                if "Boosted" in region : 
                    hs.GetYaxis().SetTitle("m(#tau_{h}J) [GeV]")
                elif "Resolved" in region :
                    lep_ = ""
                    if "El" in lep : lep_ = "e"
                    elif "Mu" in lep : lep_ = "#mu"
                    hs.GetYaxis().SetTitle(f"m(#tau_{{h}}{lep_}jj) [GeV]")
                hs.GetYaxis().SetTitle(f"L_{{T}}+H_{{T}} [GeV]")
                hs.GetYaxis().SetTitleSize(0.0475)
                hs.GetYaxis().SetTitleOffset(1.2)
                hs.GetYaxis().SetRangeUser(300,2200)
                hs.Draw("box")
                #canvas.SetLogy()
                #canvas.SetLogx()
                latex = TLatex()
                y_ = 0.675
                l = TLegend(0.465,y_,0.875,y_ + 0.2)
                #l.SetNColumns(2)
                l.AddEntry(h_bkg,"Prompt Background","f")
                l.AddEntry(h_Signal,f"#splitline{{m(W_{{R}})=2TeV, m(N)={mn/1000.}TeV}}{{(scaled by {scale:.2f})}} ","f")
                textSize = 0.625*gStyle.GetPadTopMargin()
                latex.SetNDC()
                latex.SetTextColor(kBlack)
                latex.SetTextFont(61)
                latex.SetTextSize(textSize)
                latex.DrawLatex(0.125, 0.925,"CMS")
                latex.SetTextFont(52)
                latex.SetTextSize(0.7*textSize)
                latex.DrawLatex(0.25, 0.925,"Simulation")
                latex.SetTextFont(42)
                latex.SetTextSize(0.4*textSize)
                latex.SetTextAlign(31)
                l.SetFillStyle(0)
                l.SetBorderSize(0)
                l.Draw()
                latex.SetTextFont(42)
                latex.SetTextSize(0.5*textSize)
                latex.SetTextAlign(31)
                latex.DrawLatex(0.875, 0.335,f"{region} {lepstr} Low Mass CR")
                
                latex.DrawLatex(0.875, 0.385, f"{region} {lepstr} SR")
                
                line_MET.Draw("same")
                line_var.Draw("same")
                canvas.Update()
                canvas.SaveAs(f"Overlay/LTHT/RegionOverlay_{region}_{lep}_WR2000_N{mn}.png")
