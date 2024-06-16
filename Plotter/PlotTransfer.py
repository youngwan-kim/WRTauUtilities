from ROOT import *
from array import array

l_regions_prefix = ["BoostedPreselection","BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion","ResolvedPreselection"]

l_regions = [f"{region}{suffix}" for region in l_regions_prefix for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

stamp = "240521"
l_era = ["2016preVFP","2016","2017","2018","Run2"]

l = [1.,10.,25.,50.,100.,200.,350.,500.,700.,1000.,2500.]
l_era = ["2017","2018"]
for era in l_era :
    for lep in ["ElTau","MuTau"] :
        f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
        f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
        f_MC_Loose = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_LooseTauPrompt.root")
        f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_MCLeptonFake.root")
        for region in ["Boosted","Resolved"] :
            c = TCanvas(f"{era}{lep}{region}",f"{era}{lep}{region}",1000,1000)

            pad1 = TPad(f"{era}{lep}{region}PU",f"{era}{lep}{region}PU", 0, 0.5, 1, 1)
            pad1.SetBottomMargin(0.02)  # Reduce the bottom margin for the upper pad
            pad1.Draw()

            pad2 = TPad(f"{era}{lep}{region}PD",f"{era}{lep}{region}PD", 0, 0, 1, 0.5)
            pad2.SetTopMargin(0.02)  # Reduce the top margin for the lower pad
            pad2.Draw()
            h_A_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/MET")
            h_A_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/MET")
            h_A_MC = h_A_MC_prompt.Clone(f"{era}{lep}AMC")
            h_A_MC.Add(h_A_MC_nonprompt)
            n_A_MC = h_A_MC_prompt.Integral() + h_A_MC_nonprompt.Integral()
            print(h_A_MC)

            h_C = f_data.Get(f"Central/{region}SignalRegionMETInvert_{lep}/MET")
            h_C_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/MET")
            h_C_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/MET")
            n_C_MC = h_C_MC_prompt.Integral() + h_C_MC_nonprompt.Integral()
            h_C_MC = h_C_MC_prompt.Clone(f"{era}{lep}CMC")
            h_C_MC.Add(h_C_MC_nonprompt)

            h_AC_MC = h_C_MC.Clone(f"AC{era}{lep}")
            h_AC_MC.Add(h_A_MC)
            nLowAC = h_AC_MC.GetBinContent(1)
            h_AC = h_AC_MC.Clone(f"ACClone{era}{lep}").Rebin(len(l)-1,f"ACRebin{era}{lep}",array('d',l))
            newBin1 = h_AC.GetBinContent(1) + nLowAC
            print(newBin1,h_AC.GetBinContent(1),nLowAC)
            h_AC.SetBinContent(1,newBin1)
            h_AC.GetYaxis().SetRangeUser(1e-2,1e+4)
            h_AC.GetXaxis().SetRangeUser(1,1000.)
            h_AC.SetStats(0)
            h_AC.SetFillColorAlpha(TColor.GetColor("#5755FE"),0.85)
            h_AC.SetLineColor(kBlack)
            h_C_Data = h_C.Clone(f"Data{era}{lep}").Rebin(len(l)-1,f"ACRebin{era}{lep}",array('d',l))
            h_C_Data.GetYaxis().SetRangeUser(1e-2,1e+4)
            h_C_Data.GetXaxis().SetRangeUser(1,1000.)
            h_C_Data.SetStats(0)
            h_C_Data.SetMarkerStyle(8)
            h_C_Data.SetLineColor(kBlack)

            h_B = f_fake.Get(f"Central/{region}SignalRegion_{lep}/MET")
            h_B_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/MET")
            h_B_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/MET")
            n_B_MC = h_B_MC_prompt.Integral() + h_B_MC_nonprompt.Integral()
            h_B_MC = h_B_MC_prompt.Clone(f"{era}{lep}BMC")
            h_B_MC.Add(h_B_MC_nonprompt)

            h_D = f_fake.Get(f"Central/{region}SignalRegionMETInvert_{lep}/MET")
            h_D_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/MET") 
            h_D_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/MET") 
            n_D_MC = h_D_MC_prompt.Integral() + h_D_MC_nonprompt.Integral()
            #rho = (n_A_MC/n_B_MC)/(n_C_MC/n_D_MC)
            h_D_MC = h_D_MC_prompt.Clone()
            h_D_MC.Add(h_D_MC_nonprompt)

            h_BD_MC = h_D_MC.Clone(f"BD{era}{lep}")
            h_BD_MC.Add(h_B_MC)
            h_BD = h_BD_MC.Clone(f"BDClone{era}{lep}").Rebin(len(l)-1,f"BDRebin{era}{lep}",array('d',l))
            h_BD.GetYaxis().SetRangeUser(1e-2,1e+4)
            h_BD.GetXaxis().SetRangeUser(1,1000.)
            h_BD.SetStats(0)
            h_BD.SetFillColorAlpha(TColor.GetColor("#5755FE"),0.85)
            h_BD.SetLineColor(kBlack)
            h_BD_Data_TMP = h_B.Clone()
            h_BD_Data_TMP.Add(h_D)
            h_BD_Data = h_BD_Data_TMP.Clone(f"BDData{era}{lep}").Rebin(len(l)-1,f"BDRebin{era}{lep}",array('d',l))
            h_BD_Data.GetYaxis().SetRangeUser(1e-2,1e+4)
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


            line = TLine(100, 0, 100, 1e+4)
            line.SetLineColor(kBlack)  # Set the color of the line
            line.SetLineWidth(2) 
            c.cd()
            pad1.cd()
            pad1.SetLogy()
            pad1.SetLogx()
            h_AC.Draw("hist")
            h_C_Data.Draw("hist&e1&p&same")
            line.Draw("same")

            pad2.cd()
            pad2.SetLogy()
            pad2.SetLogx()
            h_BD.Draw("hist")
            h_BD_Data.Draw("hist&e1&p&same")
            line.Draw("same")
            c.Update()
            c.SaveAs(f"Transfer/{era}_{region}_{lep}.png")