from utils import *
import os,argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
parser.add_argument('--no-scaleSignals', action='store_true')
args = parser.parse_args()

noscaling = args.no_scaleSignals
if noscaling :
    args.tag += "_noScale"


for era in ["2017"] :
    os.system(f"mkdir -p Workspaces/{args.tag}/{era}")
    for mwr in d_mass :
        for mn in d_mass[mwr] :
            #log = cmd.getoutput(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel DataCard/Cards/2017/card_WR{mwr}_N{mn}.txt -o Workspaces/{era}/card_WR{mwr}_N{mn}.root")
            os.system(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.LRSMModel:lrsmModel Cards/{args.tag}/{era}/card_WR{mwr}_N{mn}.txt -o Workspaces/{args.tag}/{era}/card_WR{mwr}_N{mn}.root | tee -a Workspaces/{args.tag}/{era}/card_WR{mwr}_N{mn}.log")