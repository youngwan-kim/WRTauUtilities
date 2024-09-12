# Place it at /data6/Users/jihkim/HNDiLeptonWorskspace/Limits/ReadLimits/Shape
# python ReadLimitFromTree.py --Full[--Asymptotic]

from ROOT import *
import os, argparse
from utils import *

parser = argparse.ArgumentParser(description='option')
parser.add_argument('--Asymptotic', action='store_true')
parser.add_argument('--Full', action='store_true')
parser.add_argument('-e', dest='years', nargs="+")
parser.add_argument('-t', dest='myWPs', nargs="+")
args = parser.parse_args()

workdir = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Batch/"

myWPs, years = args.myWPs, args.years

#years = ["2016preVFP","2016postVFP","2017","2018"]
#years = ["2016","Run2"]
#myWPs = ["240513"]

channels = [""]
tags     = [""] 
IDs      = [""]

d_mass_ = d_mass

for WP in myWPs:
  this_workdir = workdir+WP
  for year, channel, ID, tag in [[year, channel, ID, tag] for year in years for channel in channels for ID in IDs for tag in tags]:
    os.system("mkdir -p Limits/"+WP+"/"+year)  
    if year == "2018" : d_mass_ = d_mass_2018
    if args.Asymptotic:
      for mwr in d_mass_ :
        with open("Limits/"+WP+"/"+year+"/WR"+str(mwr)+".txt", 'w') as f:
          for mn in d_mass_[mwr]:
            this_name = "WR" + str(mwr) + "_N" + str(mn) 
            path = this_workdir + "/" + year + "/Asymptotic/" + this_name + "/output/"+this_name+"_Asymptotic.root"
            
            f_Asym = TFile.Open(path)
            if not check(f_Asym, "limit") : continue
            tree_Asym = f_Asym.Get("limit")
            print(f_Asym, tree_Asym)
            tree_Asym.GetEntry(2) # substitute for obs. limit for now
            #f.write(mass+"\t"+str(round(tree_Asym.limit,3))+"\t")
            #f.write(mass+"\t"+str(round(tree_Asym.limit/1.87,3))+"\t") # FIXME estimating full Run2 from 2017
            f.write(str(mn)+"\t"+str(round(tree_Asym.limit/1.296,7))+"\t") # FIXME estimating full Run2+3 from 2017
        
            for i in range(5): # expected limits
              tree_Asym.GetEntry(i)
              #f.write(str(round(tree_Asym.limit,3))+"\t")
              #f.write(str(round(tree_Asym.limit/1.87,3))+"\t") # FIXME estimating full Run2 from 2017
              f.write(str(round(tree_Asym.limit/1.296,7))+"\t") # FIXME estimating full Run2+3 from 2017
              print(round(tree_Asym.limit/1.296,7))
            f.write("\n")
  
    if args.Full:
      with open("out/"+WP+"/"+year+"_"+channel+ID+tag+"_Full_limit.txt", 'w') as f:
  
        for mass in masses:
          this_name = year+"_"+channel+"_M"+mass+ID+tag
          paths = [
                  this_workdir+"/full_CLs/"+this_name+"/output/"+this_name+"_Q1.root",
                  this_workdir+"/full_CLs/"+this_name+"/output/"+this_name+"_Q2.root",
                  this_workdir+"/full_CLs/"+this_name+"/output/"+this_name+"_Q3.root",
                  this_workdir+"/full_CLs/"+this_name+"/output/"+this_name+"_Q4.root",
                  this_workdir+"/full_CLs/"+this_name+"/output/"+this_name+"_Q5.root",
                  ]
  
          f_Q1 = TFile.Open(paths[0])
          f_Q2 = TFile.Open(paths[1])
          f_Q3 = TFile.Open(paths[2])
          f_Q4 = TFile.Open(paths[3])
          f_Q5 = TFile.Open(paths[4])
  
          tree_Q1 = f_Q1.Get("limit")
          tree_Q2 = f_Q2.Get("limit")
          tree_Q3 = f_Q3.Get("limit")
          tree_Q4 = f_Q4.Get("limit")
          tree_Q5 = f_Q5.Get("limit")
          
          tree_Q1.GetEntry(0)
          tree_Q2.GetEntry(0)
          tree_Q3.GetEntry(0)
          tree_Q4.GetEntry(0)
          tree_Q5.GetEntry(0)
          
          f.write(mass+"\t"+str(round(tree_Q3.limit,3))+"\t"+str(round(tree_Q1.limit,3))+"\t"+str(round(tree_Q2.limit,3))+"\t"+str(round(tree_Q3.limit,3))+"\t"+str(round(tree_Q4.limit,3))+"\t"+str(round(tree_Q5.limit,3))+"\n")