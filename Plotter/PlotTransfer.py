from ROOT import *
from array import array

l_regions_prefix = ["BoostedPreselection","BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion","ResolvedPreselection"]

l_regions = [f"{region}{suffix}" for region in l_regions_prefix for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

stamp = "240619"
l_era = ["2016","2017","2018"]

l = [1.,10.,25.,50.,100.,500,1000.]
l_era = ["2017","2018"]
for era in l_era :
    for lep in ["ElTau","MuTau"] :
        f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
        f_loosedata = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_VVVLooseDATA.root")
        f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
        f_MC_Loose = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_LooseTauPrompt.root")
        f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_MCLeptonFake.root")
        for region in ["Boosted","Resolved"] :
            c = TCanvas(f"{era}{lep}{region}",f"{era}{lep}{region}",1000,1000)

            pad1 = TPad(f"{era}{lep}{region}PU",f"{era}{lep}{region}PU", 0, 0.5, 1, 1)
            pad1.SetBottomMargin(0.035)  # Reduce the bottom margin for the upper pad
            pad1.SetRightMargin(0.025)
            pad1.SetTopMargin(0.1)
            pad1.Draw()

            pad2 = TPad(f"{era}{lep}{region}PD",f"{era}{lep}{region}PD", 0, 0, 1, 0.5)
            pad2.SetTopMargin(0.015)  # Reduce the top margin for the lower pad
            pad2.SetRightMargin(0.025)
            pad2.SetBottomMargin(0.2)
            pad2.Draw()
            h_A_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/MET")
            h_A_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/MET")
            h_A_MC = h_A_MC_prompt.Clone(f"{era}{lep}AMC")
            h_A_MC.Add(h_A_MC_nonprompt)
            n_A_MC = h_A_MC_prompt.Integral() + h_A_MC_nonprompt.Integral()
            print(h_A_MC)

            h_C = f_data.Get(f"Central/{region}SignalRegionMETInvertMTSame_{lep}/MET")
            h_C_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/MET")
            h_C_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/MET")
            n_C_MC = h_C_MC_prompt.Integral() + h_C_MC_nonprompt.Integral()
            h_C_MC = h_C_MC_prompt.Clone(f"{era}{lep}CMC")
            h_C_MC.Add(h_C_MC_nonprompt)

            h_AC1_MC = h_C_MC.Clone(f"AC{era}{lep}")
            nLowAC1 = h_AC1_MC.GetBinContent(1)
            h_AC1 = h_AC1_MC.Clone(f"ACClone{era}{lep}").Rebin(len(l)-1,f"ACRebin{era}{lep}",array('d',l))
            newBin1 = h_AC1.GetBinContent(1) + nLowAC1
            print(newBin1,h_AC1.GetBinContent(1),nLowAC1)
            h_AC1.SetBinContent(1,newBin1)
            h_AC1.GetYaxis().SetRangeUser(0.05,2500)
            h_AC1.GetXaxis().SetRangeUser(1,1000.)
            h_AC1.SetStats(0)
            h_AC1.SetFillColorAlpha(kRed,0.55)
            h_AC1.SetLineColor(kBlack)

            h_AC2_MC = h_A_MC.Clone(f"AC{era}{lep}")
            #nLowAC2 = h_AC2_MC.GetBinContent(1)
            h_AC2 = h_AC2_MC.Clone(f"ACClone{era}{lep}").Rebin(len(l)-1,f"ACRebin{era}{lep}",array('d',l))
            #newBin1 = h_AC2.GetBinContent(1) + nLowAC2
            #print(newBin1,h_AC2.GetBinContent(1),nLowAC2)
            #h_AC2.SetBinContent(1,newBin1)
            h_AC2.GetYaxis().SetRangeUser(0.05,2500)
            h_AC2.GetXaxis().SetRangeUser(1,1000.)
            h_AC2.SetStats(0)
            h_AC2.SetFillColorAlpha(kGreen,0.55)
            h_AC2.SetLineColor(kBlack)

            h_C_Data = h_C.Clone(f"Data{era}{lep}").Rebin(len(l)-1,f"ACRebin{era}{lep}",array('d',l))
            h_C_Data.GetYaxis().SetRangeUser(0.05,2500)
            h_C_Data.GetXaxis().SetRangeUser(1,1000.)
            h_C_Data.SetStats(0)
            h_C_Data.SetMarkerStyle(8)
            h_C_Data.SetLineColor(kBlack)

            h_B = f_loosedata.Get(f"Central/{region}SignalRegion_{lep}/MET")
            h_B_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/MET")
            h_B_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/MET")
            n_B_MC = h_B_MC_prompt.Integral() + h_B_MC_nonprompt.Integral()
            h_B_MC = h_B_MC_prompt.Clone(f"{era}{lep}BMC")
            h_B_MC.Add(h_B_MC_nonprompt)

            h_D = f_loosedata.Get(f"Central/{region}SignalRegionMETInvertMTSame_{lep}/MET")
            h_D_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/MET") 
            h_D_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/MET") 
            n_D_MC = h_D_MC_prompt.Integral() + h_D_MC_nonprompt.Integral()
            #rho = (n_A_MC/n_B_MC)/(n_C_MC/n_D_MC)
            h_D_MC = h_D_MC_prompt.Clone()
            h_D_MC.Add(h_D_MC_nonprompt)

            h_BD1_MC = h_D_MC.Clone(f"BD1{era}{lep}")
            nLowBD1 = h_BD1_MC.GetBinContent(1)
            h_BD1 = h_BD1_MC.Clone(f"BD1Clone{era}{lep}").Rebin(len(l)-1,f"BD1Rebin{era}{lep}",array('d',l))
            newBin2 = h_BD1.GetBinContent(1) + nLowBD1
            print(newBin2,h_BD1.GetBinContent(1),nLowBD1)
            h_AC1.SetBinContent(1,newBin1)
            h_BD1.GetYaxis().SetRangeUser(0.05,2500)
            h_BD1.GetXaxis().SetRangeUser(1,1000.)
            h_BD1.SetStats(0)
            h_BD1.SetFillColorAlpha(kRed,0.25)
            h_BD1.SetLineColor(kBlack)
            h_BD2_MC = h_B_MC.Clone(f"BD2{era}{lep}")
            h_BD2 = h_BD2_MC.Clone(f"BD2Clone{era}{lep}").Rebin(len(l)-1,f"BD2Rebin{era}{lep}",array('d',l))
            h_BD2.GetYaxis().SetRangeUser(0.05,2500)
            h_BD2.GetXaxis().SetRangeUser(1,1000.)
            h_BD2.SetStats(0)
            h_BD2.SetFillColorAlpha(kGreen,0.25)
            h_BD2.SetLineColor(kBlack)
            h_BD_Data_TMP = h_B.Clone()
            h_BD_Data_TMP.Add(h_D)
            h_BD_Data = h_BD_Data_TMP.Clone(f"BDData{era}{lep}").Rebin(len(l)-1,f"BDRebin{era}{lep}",array('d',l))
            h_BD_Data.GetYaxis().SetRangeUser(0.05,2500)
            h_BD_Data.GetXaxis().SetRangeUser(1,1000.)
            h_BD_Data.SetStats(0)
            h_BD_Data.SetMarkerStyle(8)
            h_BD_Data.SetLineColor(kBlack)
            
            
            nB = h_B.Integral() - n_B_MC
            nC = h_C.Integral() - n_C_MC
            nD = h_D.Integral() - n_D_MC
            nA = nC/nD * nB 
            print(era,region,lep,nA)#,nB,nC,nD,nC/nD)
            #print(h_B.Integral(),n_B_MC)

            ylabelsize = 0.065

            line = TLine(100, 0, 100, 2500)
            line.SetLineColor(kBlack)  # Set the color of the line
            line.SetLineWidth(1) 
            c.cd()
            pad1.cd()
            pad1.SetLogy()
            pad1.SetLogx()
            h_AC1.GetYaxis().SetLabelSize(ylabelsize)
            h_AC2.GetYaxis().SetLabelSize(ylabelsize)
            h_C_Data.GetYaxis().SetLabelSize(ylabelsize)
            h_AC1.GetXaxis().SetLabelSize(0)
            h_AC2.GetXaxis().SetLabelSize(0)
            h_C_Data.GetXaxis().SetLabelSize(0)
            h_AC1.Draw("hist")
            h_AC2.Draw("hist&same")

            h_C_Data.Draw("hist&e1&p&same")
            line.Draw("same")

            textSize = 0.1
            latex = TLatex()
            latex.SetNDC()
            latex.SetTextColor(kBlack)
            latex.SetTextFont(61)
            latex.SetTextSize(textSize)
            latex.DrawLatex(0.135, 0.775,"CMS")
            latex.SetTextFont(52)
            latex.SetTextSize(0.7*textSize)
            latex.DrawLatex(0.135, 0.7,"Work in Progress")

            pad2.cd()
            pad2.SetLogy()
            pad2.SetLogx()
            h_BD1.GetYaxis().SetLabelSize(ylabelsize)
            h_BD2.GetYaxis().SetLabelSize(ylabelsize)
            h_BD_Data.GetYaxis().SetLabelSize(ylabelsize)
            xlabelsize = 0.065
            h_BD1.GetXaxis().SetLabelSize(xlabelsize)
            h_BD2.GetXaxis().SetLabelSize(xlabelsize)
            h_BD_Data.GetXaxis().SetLabelSize(xlabelsize)

            h_BD1.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
            h_BD2.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")
            h_BD_Data.GetXaxis().SetTitle("#slash{E}_{T} [GeV]")

            xtitlesize = xlabelsize*1.2
            h_BD1.GetXaxis().SetTitleSize(xtitlesize)
            h_BD2.GetXaxis().SetTitleSize(xtitlesize)
            h_BD_Data.GetXaxis().SetTitleSize(xtitlesize)
            h_BD1.Draw("hist")
            h_BD2.Draw("hist&same")
            h_BD_Data.Draw("hist&e1&p&same")
            line.Draw("same")


            latex2 = TLatex()
            latex2.SetNDC()
            latex2.SetTextColor(kBlack)
            latex2.SetTextFont(61)
            latex2.SetTextSize(textSize)
            latex2.DrawLatex(0.135, 0.865,"CMS")
            latex2.SetTextFont(52)
            latex2.SetTextSize(0.7*textSize)
            latex2.DrawLatex(0.135, 0.795,"Work in Progress")
            c.Update()
            c.SaveAs(f"Transfer/{era}_{region}_{lep}.png")