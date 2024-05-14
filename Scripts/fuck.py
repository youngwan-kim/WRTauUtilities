import os

haddstr = ""
for era in ["2016preVFP","2016postVFP","2017","2018"] :
    haddstr += f"../RootFiles/240511/{era}/DATA/WRTau_Analyzer_DATA.root "
os.system(f"hadd ../RootFiles/240511/Run2/DATA/WRTau_Analyzer_DATA.root {haddstr}")