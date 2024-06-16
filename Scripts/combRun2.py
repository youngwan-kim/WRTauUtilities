#!/usr/bin/python3
import os

tag = "240525"


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


os.system(f"mkdir -p ../RootFiles/{tag}/Run2/DATA")
os.system(f"mkdir -p ../RootFiles/{tag}/Run2/Signals")

for sample in ["Boson","Fakes","DataDrivenTau","Top","MCLeptonFake"] :
    haddstr = ""
    for era in ["2016preVFP","2016postVFP","2017","2018"] :
        haddstr += f"../RootFiles/{tag}/{era}/WRTau_Analyzer_{sample}.root "
    os.system(f"hadd ../RootFiles/{tag}/Run2/WRTau_Analyzer_{sample}.root {haddstr}")

for mwr in signals :
    for mn in signals[mwr] :
            haddstr = ""
            for era in ["2016preVFP","2016postVFP","2017","2018"] :
                haddstr += f"../RootFiles/{tag}/{era}/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root "
            os.system(f"hadd ../RootFiles/{tag}/Run2/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root {haddstr}")

haddstr = ""
for era in ["2016preVFP","2016postVFP","2017","2018"] :
    haddstr += f"../RootFiles/{tag}/{era}/DATA/WRTau_Analyzer_DATA.root "
os.system(f"hadd ../RootFiles/{tag}/Run2/DATA/WRTau_Analyzer_DATA.root {haddstr}")
