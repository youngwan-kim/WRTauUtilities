import ROOT

# Open the ROOT file
file = ROOT.TFile.Open("/gv0/DATA/SKFlat/Run2UltraLegacy_v3/2018/MC/WRtoTauNtoTauTauJets_WR3200_N1800_TuneCP5_13TeV-madgraph-pythia8/SKFlat_Run2UltraLegacy_v3/240124_015705/0000/SKFlatNtuple_2018_MC_10.root")
if not file or file.IsZombie():
    raise Exception("Error opening file")

dir = file.Get("recoTree")
if not dir:
    raise Exception("Error accessing TDirectoryFile 'recoTree'")

tree = dir.Get("SKFlat")
if not tree:
    raise Exception("Error getting TTree 'SKFlat'")

# Loop over all entries
for i in range(0,min(1,tree.GetEntries())):
    tree.GetEntry(i)
    
    # Access the branch and print its values
    values = tree.weight_PDF
    print(f"Entry {i}: ", list(values))

# Close the file
file.Close()
