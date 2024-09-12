#!/usr/bin/python3
import os

tag = "240808"

signals = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [100,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

os.system(f"mkdir -p ../RootFiles/{tag}/2016/DATA")
os.system(f"mkdir -p ../RootFiles/{tag}/2016/Signals")
os.system(f"mkdir -p ../RootFiles/{tag}/2016/RunSyst")

for sample in ["Boson_noVJets","PromptFakes","Fakes","DataDrivenTau","Top","MCLeptonFake"] :
    #os.system(f"hadd ../RootFiles/{tag}/2016/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016postVFP/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016preVFP/WRTau_Analyzer_{sample}.root")
    os.system(f"hadd ../RootFiles/{tag}/2016/RunSyst/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016postVFP/RunSyst/WRTau_Analyzer_{sample}.root ../RootFiles/{tag}/2016preVFP/RunSyst/WRTau_Analyzer_{sample}.root")

#for mwr in signals :
#    for mn in signals[mwr] :
#        os.system(f"hadd ../RootFiles/{tag}/2016/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root ../RootFiles/{tag}/2016postVFP/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root ../RootFiles/{tag}/2016preVFP/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")

#os.system(f"hadd ../RootFiles/{tag}/2016/DATA/WRTau_Analyzer_DATA.root ../RootFiles/{tag}/2016postVFP/DATA/WRTau_Analyzer_DATA.root ../RootFiles/{tag}/2016preVFP/DATA/WRTau_Analyzer_DATA.root")
