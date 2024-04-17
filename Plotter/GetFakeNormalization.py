from ROOT import *

l_regions_prefix = ["BoostedPreselection","BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion","ResolvedPreselection"]

l_regions = [f"{region}{suffix}" for region in l_regions_prefix for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

stamp = "240416"

for era in ["2016","2016preVFP","2016postVFP","2017","2018"] :
    f_data = TFile(f"../RootFiles/{stamp}/{era}/DATA/WRTau_Analyzer_DATA.root")
    f_fake = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_DataDrivenTau.root")
    f_MC = TFile(f"../RootFiles/{stamp}/{era}/WRTau_Analyzer_MCLeptonFake.root")
    for region in l_regions :
        h_data = f_data.Get(f"WRTau_SignalSingleTauTrg/vJetTight_vElTight_vMuTight/{region}/Nevents")
        n_data = h_data.Integral()
        h_fake = f_fake.Get(f"WRTau_SignalSingleTauTrg/vJetVVVLoose_vElTight_vMuTight/{region}/Nevents")
        n_fake = h_fake.Integral()*1.08
        h_MC_prompt    = f_MC.Get(f"WRTau_SignalSingleTauTrg__PromptTau__PromptLepton/vJetTight_vElTight_vMuTight/{region}/Nevents")
        h_MC_nonprompt = f_MC.Get(f"WRTau_SignalSingleTauTrg__PromptTau__NonPromptLepton/vJetTight_vElTight_vMuTight/{region}/Nevents")
        n_MC = h_MC_prompt.Integral()*1.08 + h_MC_nonprompt.Integral()*1.08
        ratio = (n_data - n_MC)/n_fake 
        #print(f"Region: {region} Era: {era} Data: {n_data} Fake: {n_fake} MC: {h_MC_prompt.Integral()}+{h_MC_nonprompt.Integral()}={n_MC} Ratio: {ratio}")
        print(f"('{era}','{region}') : {ratio},")
