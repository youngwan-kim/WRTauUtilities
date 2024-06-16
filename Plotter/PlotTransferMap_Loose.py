from ROOT import *
from array import array

stamp = "240527"
l_era = ["2016preVFP","2016","2017","2018","Run2"]

l = [1.,10.,25.,50.,100.,200.,350.,500.,700.,1000.,2500.]
l_era = ["2017"]
for era in l_era :
    for lep in ["ElTau","MuTau"] :
        f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
        f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
        f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_LooseTauPrompt.root")
        for region in ["Boosted","Resolved"] :
            c = TCanvas(f"{era}{lep}{region}",f"{era}{lep}{region}",1000,1000)
            

            h_MetMt_MCPrompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_MtWR").Rebin2D(10,10)
            h_MetMt_MCNonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_MtWR").Rebin2D(10,10)

            h_MetMt = h_MetMt_MCPrompt.Clone(f"{era}{region}{lep}")
            h_MetMt.Add(h_MetMt_MCNonprompt)

            h_MetMt.GetXaxis().SetRangeUser(1,1500)
            h_MetMt.GetYaxis().SetRangeUser(1,1500)

            h_MetMt.SetStats(0)
            print(h_MetMt.Integral())

            h_MetMeff_MCPrompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/Benchmark{region}Preselection_{lep}/MET_MeffWR").Rebin2D(10,10)
            h_MetMeff_MCNonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/Benchmark{region}Preselection_{lep}/MET_MeffWR").Rebin2D(10,10)

            h_MetMeff = h_MetMeff_MCPrompt.Clone(f"{era}{region}{lep}")
            h_MetMeff.Add(h_MetMeff_MCNonprompt)

            h_MetMeff.GetXaxis().SetRangeUser(1,1500)
            h_MetMeff.GetYaxis().SetRangeUser(400,1500)

            h_MetMeff.SetStats(0)


            line_MET = TLine(100,0,100,1500)
            line_Mt  = TLine(0,450,1500,450)
            line_Meff  = TLine(0,600,1500,600)
            line_MET.SetLineColor(kRed)  # Set the color of the line
            line_MET.SetLineWidth(2) 
            line_Mt.SetLineColor(kRed)  # Set the color of the line
            line_Mt.SetLineWidth(2) 
            line_Meff.SetLineColor(kRed)  # Set the color of the line
            line_Meff.SetLineWidth(2) 
            
            c.cd()
            c.SetLogy()
            c.SetLogx()
            h_MetMt.Draw("colz")
            line_MET.Draw("same")
            line_Mt.Draw("same")
            c.Update()
            c.SaveAs(f"Transfer/MapMET_MtWR_{era}_{region}_{lep}_VVVL.png")

            c2 = TCanvas(f"{era}{lep}{region}",f"{era}{lep}{region}",1000,1000)
            c2.cd()
            c2.SetLogy()
            c2.SetLogx()
            h_MetMeff.Draw("colz")
            line_MET.Draw("same")
            line_Meff.Draw("same")
            c2.Update()
            c2.SaveAs(f"Transfer/MapMET_MeffWR_{era}_{region}_{lep}_VVVL.png")