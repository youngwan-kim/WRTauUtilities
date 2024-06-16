from ROOT import *

l_regions_prefix = ["BoostedPreselection","BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion","ResolvedPreselection"]

l_regions = [f"{region}{suffix}" for region in l_regions_prefix for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

stamp = "240521"
l_era = ["2016preVFP","2016","2017","2018","Run2"]

l_era = ["2017","2018"]
for era in l_era :
    f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
    f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
    f_MC_Loose = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_LooseTauPrompt.root")
    f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_MCLeptonFake.root")
    for region in ["Boosted","Resolved"] :
        for lep in ["ElTau","MuTau"] :
            h_A_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/Nevents")
            h_A_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/Nevents")
            n_A_MC = h_A_MC_prompt.Integral() + h_A_MC_nonprompt.Integral()

            h_B = f_fake.Get(f"Central/{region}SignalRegion_{lep}/Nevents")
            h_B_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegion_{lep}/Nevents")
            h_B_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegion_{lep}/Nevents")
            n_B_MC = h_B_MC_prompt.Integral() + h_B_MC_nonprompt.Integral()

            h_C = f_data.Get(f"Central/{region}SignalRegionMETInvert_{lep}/Nevents")
            h_C_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/Nevents")
            h_C_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/Nevents")
            n_C_MC = h_C_MC_prompt.Integral() + h_C_MC_nonprompt.Integral()

            h_D = f_fake.Get(f"Central/{region}SignalRegionMETInvert_{lep}/Nevents")
            h_D_MC_prompt    = f_MC_Loose.Get(f"Central/__PromptTau__PromptLepton/{region}SignalRegionMETInvert_{lep}/Nevents")
            h_D_MC_nonprompt = f_MC_Loose.Get(f"Central/__PromptTau__NonPromptLepton/{region}SignalRegionMETInvert_{lep}/Nevents")
            n_D_MC = h_D_MC_prompt.Integral() + h_D_MC_nonprompt.Integral()

            rho = (n_A_MC/n_B_MC)/(n_C_MC/n_D_MC)

            nB = h_B.Integral() - n_B_MC
            nC = h_C.Integral() - n_C_MC
            nD = h_D.Integral() - n_D_MC
            nA = nC/nD * nB * rho
            print(era,region,lep,nA)#,nB,nC,nD,nC/nD)
            #print(h_B.Integral(),n_B_MC)
