from utils import *

input_path = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Workspaces"

myWPs = ["240513"]

for WP in myWPs:
    with open("RunList_"+WP+".txt",'w') as f:
        for era in ["2016","Run2"]:
            for mwr in d_mass :
                for mn in d_mass[mwr]:
                    card = f"{input_path}/{era}/card_WR{mwr}_N{mn}.root\n"
                    f.write(card)
