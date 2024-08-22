import os , array
from ROOT import * 
from utils import *
from math import ceil
import argparse

input_path = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Workspaces"
parser = argparse.ArgumentParser(description='')
parser.add_argument('-e', dest='l_era', nargs="+")
parser.add_argument('-t', dest='tag', type=str, help='Input tag',default="240808")
parser.add_argument('--no-scaleSignals', action='store_true')
args = parser.parse_args()

noscaling = args.no_scaleSignals

d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [100,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

l_era = args.l_era

inputTag = args.tag
saveTag = inputTag
if noscaling : saveTag += "_noScale"

inputDir = f"{os.getenv('WRTau_Output')}/{inputTag}"

d_region = {
    
    #"LowMassControlRegion" : "LMCR",
    #"SignalRegionMETInvertMTSame" : "QCDFakeMR",
    "SignalRegion" : "SR",
}

#l_era = ["Run2"]
# save root input file with shape of mWR in ResolvedSR / BoostedSR for prompt, fake, signal
# Prompt = shape of mWR in (Resolved+Boosted)SR for prompt MC
# Fake   = shape of mWR in (Resolved+Boosted)SR for fake MC + data-driven tau 
# Signal = shape of mWR in (Resolved+Boosted)SR for signal
for r in d_region :
    if r == "LowMassControlRegion" : 
        rebins = [0,25,50,75,100,150,200,250,300,350,400,450,550,650,750,850,950]
    elif r == "SignalRegionMETInvertMTSame" :
        rebins = [900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2400,2600,3000]
    for era in l_era : 
        os.system(f"mkdir -p Outputs/{saveTag}/{d_region[r]}/{era}")

        f_prompt = TFile.Open(f"{inputDir}/{era}/RunSyst/WRTau_Analyzer_PromptMC.root")
        f_top    = TFile.Open(f"{inputDir}/{era}/RunSyst/WRTau_Analyzer_Top.root")
        f_boson  = TFile.Open(f"{inputDir}/{era}/RunSyst/WRTau_Analyzer_Boson_noVJets.root")
        f_fake   = TFile.Open(f"{inputDir}/{era}/WRTau_Analyzer_DataDrivenTau.root")
        f_data   = TFile.Open(f"{inputDir}/{era}/DATA/WRTau_Analyzer_DATA.root")

        lh_top, lh_boson , lh_fakeMC , lh_fakeData= {}, {}, {}, {}
        d_top, d_boson, d_fakeMC, d_fake = {}, {}, {}, {}
        d_top_save, d_boson_save , d_fakeMC_save, d_fake_save  = {}, {}, {}, {}

        l_syst_fakes = ["Central","Central_TauFRErrDown","Central_TauFRErrUp"]
        l_syst = GetSystList(inputTag,"Top",era) # [{syst},syst1,syst2,...]

        l_data = [] 
        h_data_real,h_data_real_tmp = TH1D(),TH1D()
        if r != "SignalRegion" :
            for i,region in enumerate([f"Resolved{r}",f"Boosted{r}"]) :
                for j,channel in enumerate(["ElTau","MuTau"]) :  
                    if check(f_data, f"Central/{region}_{channel}/ProperMeffWR") :
                        h_data_tmp   = f_data.Get(f"Central/{region}_{channel}/ProperMeffWR")
                        h_data_tmp.SetDirectory(0)
                        l_data.append(h_data_tmp)
            
            for i,h in enumerate(l_data) : 
                if i == 0 :
                    h_data_real_tmp = h.Clone(f"data_obs_{d_region[r]}")
                    h_data_real_tmp.SetDirectory(0)
                else : h_data_real_tmp.Add(h)

            h_data_real = h_data_real_tmp.Clone(f"data_obs_{d_region[r]}").Rebin(len(rebins)-1,f"data_obs_{d_region[r]}",array.array('d',rebins))
        print(h_data_real)
        for syst in l_syst :
            print(syst)
            lh_boson[syst] , lh_fakeMC[syst] , lh_top[syst] = [] , [] , []
            for i,region in enumerate([f"Resolved{r}",f"Boosted{r}"]) :
                for j,channel in enumerate(["ElTau","MuTau"]) :  
                    print(f"\t {region} {channel}")
                    if check(f_top, f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR") :
                        h_top_tmp   = f_top.Get(f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR")
                        h_top_tmp.SetDirectory(0)
                        lh_top[syst].append(h_top_tmp)
                    
                    if check(f_boson, f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR") :
                        h_boson_tmp   = f_boson.Get(f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR")
                        h_boson_tmp.SetDirectory(0)
                        lh_boson[syst].append(h_boson_tmp)

                    if check(f_prompt, f"{syst}/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR") : 
                        h_fakeMC_tmp   = f_prompt.Get(f"{syst}/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR")
                        h_fakeMC_tmp.SetDirectory(0)
                        lh_fakeMC[syst].append(h_fakeMC_tmp)

            #print(f"\t {lh_prompt}, {lh_fakeMC}")
            h_top , h_boson , h_fakeMC = TH1D() , TH1D() , TH1D()

            for i1,h1 in enumerate(lh_boson[syst]):
                if i1 == 0 : 
                    h_boson = h1.Clone(f"boson_{d_region[r]}")
                    h_boson.SetDirectory(0)
                else : h_boson.Add(h1)

            for i1,h1 in enumerate(lh_top[syst]):
                if i1 == 0 : 
                    h_top = h1.Clone(f"top_{d_region[r]}")
                    h_top.SetDirectory(0)
                else : h_top.Add(h1)

            for i2,h2 in enumerate(lh_fakeMC[syst]):
                if i2 == 0 :
                    h_fakeMC = h2.Clone(f"fakeMC_{d_region[r]}")
                    h_fakeMC.SetDirectory(0)
                else : h_fakeMC.Add(h2)

            d_top[syst], d_boson[syst], d_fakeMC[syst]  = h_top, h_boson, h_fakeMC 

            #print(d_prompt[syst])
            h_top_save = d_top[syst].Clone(f"top_{d_region[r]}{getSystString(syst)}").Rebin(len(rebins)-1,f"top_{d_region[r]}{getSystString(syst)}",array.array('d',rebins))
            h_top_save.SetDirectory(0)

            h_boson_save = d_boson[syst].Clone(f"boson_{d_region[r]}{getSystString(syst)}").Rebin(len(rebins)-1,f"boson_{d_region[r]}{getSystString(syst)}",array.array('d',rebins))
            h_boson_save.SetDirectory(0)

            h_fakeMC_save = d_fakeMC[syst].Clone(f"fakeMC_{d_region[r]}{getSystString(syst)}").Rebin(len(rebins)-1,f"fakeMC_{d_region[r]}{getSystString(syst)}",array.array('d',rebins))
            h_fakeMC_save.SetDirectory(0)

            d_top_save[syst], d_boson_save[syst], d_fakeMC_save[syst] = h_top_save, h_boson_save, h_fakeMC_save 

        for syst in l_syst_fakes :
            lh_fakeData[syst] = [] 
            if check(f_fake, f"{syst}/{region}_{channel}/ProperMeffWR") :
                h_fakeData_tmp = f_fake.Get(f"{syst}/{region}_{channel}/ProperMeffWR")
                h_fakeData_tmp.SetDirectory(0)
                lh_fakeData[syst].append(h_fakeData_tmp)

            h_fakeData = TH1D()    
            for i3,h3 in enumerate(lh_fakeData[syst]):
                if i3 == 0 :
                    h_fakeData = h3.Clone(f"fake_{d_region[r]}")
                    h_fakeData.SetDirectory(0)
                else : h_fakeData.Add(h3)

            d_fake[syst] = h_fakeData
            h_fake_save   = h_fakeData.Clone(f"fake_{d_region[r]}{getSystString(syst)}").Rebin(len(rebins)-1,f"fake_{d_region[r]}{getSystString(syst)}",array.array('d',rebins))
            h_fake_save.SetDirectory(0)
            d_fake_save[syst] =  h_fake_save

        h_data_tmp = d_top_save["Central"] + d_boson_save["Central"] + d_fakeMC_save["Central"] + d_fake_save["Central"]
        h_data_save = round_histogram(h_data_tmp).Clone(f"data_obs_{d_region[r]}")
        #print(h_data_save.Integral())

        for mwr in d_mass :
            for mn in d_mass[mwr] :

                outfile = TFile.Open(f"Outputs/{saveTag}/{d_region[r]}/{era}/WR{mwr}_N{mn}_card_input.root","RECREATE")
                f_signal = TFile.Open(f"{inputDir}/{era}/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")

                d_signal = {}
                d_signal_save = {}

                for syst in l_syst : 
                    for i,region in enumerate(["ResolvedSignalRegion","BoostedSignalRegion"]) :
                        for j,channel in enumerate(["ElTau","MuTau"]) :  
                            if check(f_signal,f"{syst}/{region}_{channel}/ProperMeffWR") :
                                h_signal_tmp = f_signal.Get(f"{syst}/{region}_{channel}/ProperMeffWR")
                                h_signal_tmp.SetDirectory(0)
                                if i == 0 and j == 0 :
                                    h_signal = h_signal_tmp.Clone(f"signal_{mwr}_{mn}")
                                    h_signal.SetDirectory(0)
                                else :
                                    h_signal.Add(h_signal_tmp)
                    d_signal[syst] = h_signal

                    h_signal_save = d_signal[syst].Clone(f"signal_{d_region[r]}{getSystString(syst)}").Rebin(len(rebins)-1,f"signal_{d_region[r]}{getSystString(syst)}",array.array('d',rebins))
                    if r == "SignalRegion" and not noscaling : h_signal_save.Scale(GetSignalScale(mwr))
                    h_signal_save.SetDirectory(0)

                    for item in [d_top_save[syst],d_boson_save[syst],d_fakeMC_save[syst],h_signal_save] :
                        original_directory = gDirectory.GetPath()
                        outfile.cd()
                        item.Write()
                        gDirectory.cd(original_directory)

                for syst in l_syst_fakes :
                    original_directory = gDirectory.GetPath()
                    h_ = d_fake_save[syst]
                    outfile.cd()
                    h_.Write()
                    gDirectory.cd(original_directory)
                original_directory = gDirectory.GetPath()
                outfile.cd()
                if r == "SignalRegion" : h_data_save.Write()
                else : h_data_real.Write()
                gDirectory.cd(original_directory)
                outfile.Close()
                print(f"Card Input for {mwr}GeV {mn}GeV is done")