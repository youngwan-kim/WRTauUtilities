import os

tag = "240416"

signals = {
    2000 : [200,1900],
    4000 : [200,3900],
    4800 : [200,4700]
}

os.system(f"mkdir -p ../RootFiles/{tag}/2016/DATA")
os.system(f"mkdir -p ../RootFiles/{tag}/2016/Signals")

for sample in ["Boson","Fakes","DataDrivenTau","Top","MCLeptonFake"] :
    os.system(f"hadd ../RootFiles/{tag}/2016/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016postVFP/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016preVFP/WRTau_Analyzer_{sample}.root")

for mwr in signals :
    for mn in signals[mwr] :
        os.system(f"hadd ../RootFiles/{tag}/2016/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root ../RootFiles/{tag}/2016postVFP/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root ../RootFiles/{tag}/2016preVFP/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")

os.system(f"hadd ../RootFiles/{tag}/2016/DATA/WRTau_Analyzer_DATA.root ../RootFiles/{tag}/2016postVFP/DATA/WRTau_Analyzer_DATA.root ../RootFiles/{tag}/2016preVFP/DATA/WRTau_Analyzer_DATA.root")
