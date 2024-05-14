from utils import *
import os
#import commands as cmd


for era in ["2016","Run2"] :
    os.system(f"mkdir -p Workspaces/{era}")
    for mwr in d_mass :
        for mn in d_mass[mwr] :
            #log = cmd.getoutput(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel DataCard/Cards/2017/card_WR{mwr}_N{mn}.txt -o Workspaces/{era}/card_WR{mwr}_N{mn}.root")
            os.system(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel Cards/{era}/card_WR{mwr}_N{mn}.txt -o Workspaces/{era}/card_WR{mwr}_N{mn}.root | tee -a Workspaces/{era}/card_WR{mwr}_N{mn}.log")