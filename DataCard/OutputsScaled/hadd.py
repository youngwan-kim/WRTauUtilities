import os

d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

os.system(f"mkdir -p Run2")

for mwr in d_mass :
    for mn in d_mass[mwr] :
        haddstr = ""
        for era in ["2016preVFP","2016postVFP","2017","2018"] :
            haddstr += f"{era}/WR{mwr}_N{mn}_card_input.root "
        os.system(f"hadd Run2/WR{mwr}_N{mn}_card_input.root {haddstr}")
