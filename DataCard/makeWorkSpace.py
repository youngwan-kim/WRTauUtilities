from utils import *
import os,argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
parser.add_argument('--no-scaleSignals', action='store_true')
args = parser.parse_args()

noscaling = args.no_scaleSignals
if noscaling :
    args.tag += "_noScale"

maker = open(f"WorkspaceMaker_{args.tag}.sh",'w')
for era in ["2018"] :
    d_mass_ = d_mass 
    if era == "2018" : d_mass_ = d_mass_2018
    os.system(f"mkdir -p Workspaces/{args.tag}/{era}")
    for mwr in d_mass_ :
        for mn in d_mass_[mwr] :
            #log = cmd.getoutput(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel DataCard/Cards/2017/card_WR{mwr}_N{mn}.txt -o Workspaces/{era}/card_WR{mwr}_N{mn}.root")
            maker.write(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt -o Workspaces/{args.tag}/{era}/card_WR{mwr}_N{mn}.root | tee -a Workspaces/{args.tag}/{era}/card_WR{mwr}_N{mn}.log \n")