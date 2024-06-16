from ROOT import *
from array import array

stamp = "240527"
l_era = ["2016preVFP","2016","2017","2018","Run2"]

l = [1.,10.,25.,50.,100.,200.,350.,500.,700.,1000.,2500.]
l_era = ["2017"]
for era in l_era :
    for lep in ["ElTau","MuTau"] :
        if lep == "ElTau" : lepstr = "e#tau_{h}"
        elif lep == "MuTau" : lepstr = "#mu#tau_{h}"
        f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
        f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
        f_MC_Loose = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_LooseTauPrompt.root")
        f_MC = TFile("/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/2DScan__Delta__/WRTau_Analyzer_Bkg.root")
        for region in ["Boosted","Resolved"] :
            #c = TCanvas(f"{era}{lep}{region}",f"{era}{lep}{region}",1000,1000)
            

            #h_MetMt_MCPrompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_MtWR").Rebin2D(10,10)
            #h_MetMt_MCNonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_MtWR").Rebin2D(10,10)
#
            #h_MetMt = h_MetMt_MCPrompt.Clone(f"{era}{region}{lep}")
            #h_MetMt.Add(h_MetMt_MCNonprompt)
#
            #h_MetMt.GetXaxis().SetRangeUser(1,1500)
            #h_MetMt.GetYaxis().SetRangeUser(1,1500)
            #h_MetMt.GetXaxis().SetLabelSize(0.025)
            #h_MetMt.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
            #h_MetMt.GetXaxis().SetTitleSize(0.05)
            #h_MetMt.GetXaxis().SetTitleOffset(0.55)
#
            #h_MetMt.SetStats(0)
            #print(h_MetMt.Integral())

            h_MetMeff_MCPrompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_ST").Rebin2D(10,10)
            h_MetMeff_MCNonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_ST").Rebin2D(10,10)

            h_MetMeff = h_MetMeff_MCPrompt.Clone(f"{era}{region}{lep}")
            h_MetMeff.Add(h_MetMeff_MCNonprompt)


            h_MetMeff.SetStats(0)

            mcut = 1050
            line_MET = TLine(100,0,100,2500)
            line_Mt  = TLine(0,450,1500,450)
            line_Meff  = TLine(0,mcut,1500,mcut)
            line_MET.SetLineColor(kRed)  # Set the color of the line
            line_MET.SetLineWidth(5) 
            line_Mt.SetLineColor(kRed)  # Set the color of the line
            line_Mt.SetLineWidth(5) 
            line_Meff.SetLineColor(kRed)  # Set the color of the line
            line_Meff.SetLineWidth(5) 
            

            #bin_MET0  = h_MetMt.GetXaxis().FindBin(100)
            #bin_Mt0   = h_MetMt.GetYaxis().FindBin(450)
            bin_MET0_ = h_MetMeff.GetXaxis().FindBin(100)
            bin_Meff0 = h_MetMeff.GetYaxis().FindBin(mcut)
#
            #n_bins_x = h_MetMt.GetNbinsX()
            #n_bins_y = h_MetMt.GetNbinsY()
            #integral_bl = h_MetMt.Integral(1, bin_MET0 - 1, 1, bin_Mt0 - 1)
            #integral_br = h_MetMt.Integral(bin_MET0, n_bins_x, 1, bin_Mt0 - 1)
            #integral_tl = h_MetMt.Integral(1, bin_MET0 - 1, bin_Mt0, n_bins_y)
            #integral_tr = h_MetMt.Integral(bin_MET0, n_bins_x, bin_Mt0, n_bins_y)

            n_bins_x_ = h_MetMeff.GetNbinsX()
            n_bins_y_ = h_MetMeff.GetNbinsY()
            integral_bl_ = h_MetMeff.Integral(1, bin_MET0_ - 1, 1, bin_Meff0 - 1)
            integral_br_ = h_MetMeff.Integral(bin_MET0_, n_bins_x_, 1, bin_Meff0 - 1)
            integral_tl_ = h_MetMeff.Integral(1, bin_MET0_ - 1, bin_Meff0, n_bins_y_)
            integral_tr_ = h_MetMeff.Integral(bin_MET0_, n_bins_x_, bin_Meff0, n_bins_y_)

            h_MetMeff.GetXaxis().SetRangeUser(1,1500)
            h_MetMeff.GetYaxis().SetRangeUser(400,2500)
            h_MetMeff.GetXaxis().SetLabelSize(0.0275)
            h_MetMeff.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
            h_MetMeff.GetXaxis().SetTitleSize(0.045)
            h_MetMeff.GetXaxis().SetTitleOffset(0.7)
            h_MetMeff.GetYaxis().SetLabelSize(0.0275)
            title = "S_{T} [GeV]"
            #if "Boosted" in region : title = "m(#tau_{h}J) [GeV]"
            #elif "Resolved" in region :
            #    if "El" in lep : title = "m(#tau_{h}ejj) [GeV]"
            #    elif "Mu" in lep : title = "m(#tau_{h}#mujj) [GeV]"
            h_MetMeff.GetYaxis().SetTitle(title)
            h_MetMeff.GetYaxis().SetTitleSize(0.045)
            h_MetMeff.GetYaxis().SetTitleOffset(0.75)


            #c.cd()
            #c.SetLogy()
            #c.SetLogx()
            #h_MetMt.Draw("colz")
            #line_MET.Draw("same")
            #line_Mt.Draw("same")
            #latex = TLatex()
            #latex.SetNDC()
            textSize = 0.625*gStyle.GetPadTopMargin()
            #latex.SetTextFont(61)
            #latex.SetTextSize(textSize)
            #latex.DrawLatex(0.125, 0.925,"CMS")
            #latex.SetTextFont(52)
            #latex.SetTextSize(0.7*textSize)
            #latex.DrawLatex(0.25, 0.925,"Simulation")
            #latex.SetTextFont(42)
            #latex.SetTextSize(0.4*textSize)
            #latex.SetTextAlign(31)
            #latex.SetTextColor(kWhite)
            #latex.DrawLatex(0.45, 0.855, f"{region} {lepstr} Fake Region")
            #latex.DrawLatex(0.45, 0.825,f"n = {integral_tl:.2f}")
            #latex.DrawLatex(0.45, 0.67,f"{region} Overlap Region")
            #latex.DrawLatex(0.45, 0.64,f"n = {integral_bl:.2f}")
            #latex.DrawLatex(0.875, 0.67,f"{region} {lepstr} Low Mass CR")
            #latex.DrawLatex(0.875, 0.64,f"n = {integral_br:.2f}")
            #latex.DrawLatex(0.875, 0.855, f"{region} {lepstr} SR")
            #latex.DrawLatex(0.875, 0.825,f"n = {integral_tr:.2f}")
            #c.Update()
            #c.SaveAs(f"Transfer/MapMET_MtWR_{era}_{region}_{lep}.png")
#
            c2 = TCanvas(f"{era}{lep}{region}2",f"{era}{lep}{region}2",1000,1000)
            c2.cd()
            c2.SetLogy()
            c2.SetLogx()
            h_MetMeff.Draw("colz")
            line_MET.Draw("same")
            line_Meff.Draw("same")
            latex2 = TLatex()
            latex2.SetNDC()
            latex2.SetTextColor(kBlack)
            latex2.SetTextFont(61)
            latex2.SetTextSize(textSize)
            latex2.DrawLatex(0.125, 0.925,"CMS")
            latex2.SetTextFont(52)
            latex2.SetTextSize(0.7*textSize)
            latex2.DrawLatex(0.25, 0.925,"Simulation")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.4*textSize)
            latex2.SetTextAlign(31)
            latex2.SetTextColor(kWhite)
            latex2.DrawLatex(0.45, 0.855, f"{region} {lepstr} Fake Region")
            latex2.DrawLatex(0.45, 0.825,f"n = {integral_tl_:.2f}")
            latex2.DrawLatex(0.45, 0.47,f"{region} Overlap Region")
            latex2.DrawLatex(0.45, 0.44,f"n = {integral_bl_:.2f}")
            latex2.DrawLatex(0.875, 0.47,f"{region} {lepstr} Low Mass CR")
            latex2.DrawLatex(0.875, 0.44,f"n = {integral_br_:.2f}")
            latex2.DrawLatex(0.875, 0.855, f"{region} {lepstr} SR")
            latex2.DrawLatex(0.875, 0.825,f"n = {integral_tr_:.2f}")
            c2.Update()
            c2.SaveAs(f"Transfer/MapMET_ST_{era}_{region}_{lep}.png")