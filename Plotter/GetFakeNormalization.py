from ROOT import *

l_regions_prefix = ["BoostedPreselection","BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion","ResolvedPreselection"]

l_regions_prefix = ["BoostedSignalRegion","ResolvedSignalRegion"]

l_regions = [f"{region}{suffix}" for region in l_regions_prefix for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

stamp = "240521"
l_era = ["2016preVFP","2016postVFP","2016","2017","2018","Run2"]
l_era = ["2017","2018"]
for era in l_era :
    f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
    f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
    f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_MCLeptonFake.root")
    for region in l_regions :
        h_data = f_data.Get(f"Central/{region}/Nevents")
        n_data = h_data.Integral()
        h_fake = f_fake.Get(f"Central/{region}/Nevents")
        n_fake = h_fake.Integral()
        h_MC_prompt    = f_MC.Get(f"Central/__PromptTau__PromptLepton/{region}/Nevents")
        h_MC_nonprompt = f_MC.Get(f"Central/__PromptTau__NonPromptLepton/{region}/Nevents")
        n_MC = h_MC_prompt.Integral() + h_MC_nonprompt.Integral() 
        ratio = (n_data - n_MC)/n_fake 
        #print(f"Region: {region} Era: {era} Data: {n_data} Fake: {n_fake} MC: {h_MC_prompt.Integral()}+{h_MC_nonprompt.Integral()}={n_MC} Ratio: {ratio}")
        #print(f"('{era}','{region}') : {ratio},")
        print(f"('{era}','{region}') : {n_data - n_MC},")
