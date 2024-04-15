import os 

era = ["2016preVFP","2016postVFP","2017","2018"]
regions = [
            "BaselinePreselection",
            "ResolvedPreselection",
            "BoostedPreselection",
            "ResolvedLowMassControlRegion",
            "BoostedLowMassControlRegion",
            "ResolvedLowMassControlRegionMass1",
            "BoostedLowMassControlRegionMass1",
            "ResolvedSignalRegion",
            "BoostedSignalRegion",
            "ResolvedSignalRegionMETInvert",
            "BoostedSignalRegionMETInvert",
            "ResolvedSignalRegionMass1",
            "BoostedMassOptSel",
            "ResolvedMassOptSel",
            "WJetsControlRegion",
            "QCDEnrichedControlRegionAK4",
            "QCDEnrichedControlRegionAK8",
            "FakeTTControlRegion",
            "FakeDYControlRegion",
            "BoostedSignalRegionLSFInvert"]

regions = [
            "ResolvedPreselection",
            "BoostedPreselection",
            "ResolvedLowMassControlRegion",
            "BoostedLowMassControlRegion",
            "ResolvedSignalRegion",
            "BoostedSignalRegion",
            "ResolvedSignalRegionMETInvert",
            "BoostedSignalRegionMETInvert" ]

channel = {"ElTau" : ["Electron","e"],
           "MuTau" : ["Muon","#mu"]}

for e in era :
    for c in channel :
        for r in regions :
            os.system(f"mkdir -p {e}/{r}_{c}")
            if "Boosted" in r :
                os.system(f"cp hists_Boosted.csv {e}/{r}_{c}/hists.csv")
            if "Resolved" in r :
                os.system(f"cp hists_Resolved.csv {e}/{r}_{c}/hists.csv") 
            os.system(f"sed s/##LEPTONEX##/{channel[c][0]}/g {e}/{r}_{c}/hists.csv")
            os.system(f"sed s/##LEPTON##/{channel[c][1]}/g {e}/{r}_{c}/hists.csv")