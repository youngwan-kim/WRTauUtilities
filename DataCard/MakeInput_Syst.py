import os , array
from ROOT import * 
from utils import *
from math import ceil

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



l_era = ["2016preVFP","2016postVFP","2017","2018"]
l_era = ["2017"]

 
inputTag = "240808"
inputDir = f"{os.getenv('WRTau_Output')}/{inputTag}"



#l_era = ["Run2"]
# save root input file with shape of mWR in ResolvedSR / BoostedSR for prompt, fake, signal
# Prompt = shape of mWR in (Resolved+Boosted)SR for prompt MC
# Fake   = shape of mWR in (Resolved+Boosted)SR for fake MC + data-driven tau 
# Signal = shape of mWR in (Resolved+Boosted)SR for signal
for era in l_era : 
    os.system(f"mkdir -p Outputs/{inputTag}/{era}")
    os.system(f"mkdir -p Outputs/{era}")

    f_prompt = TFile.Open(f"{inputDir}/{era}/RunSyst/WRTau_Analyzer_PromptMC.root")
    f_fake   = TFile.Open(f"{inputDir}/{era}/WRTau_Analyzer_DataDrivenTau.root")
    #f_data   = TFile.Open(f"{inputDir}/{era}/DATA/WRTau_Analyzer_DATA.root")

    lh_prompt = {}
    lh_fakeMC = {}
    lh_fakeData = {}

    d_prompt , d_fake = {} , {}
    d_prompt_save , d_fake_save  = {} , {}

    l_syst_fakes = ["Central","Central_TauFRErrDown","Central_TauFRErrUp"]
    l_syst = GetSystList(inputTag,"Top",era) # [{syst},syst1,syst2,...]

    for syst in l_syst :
        print(syst)
        lh_prompt[syst] , lh_fakeMC[syst] = [] , []
        for i,region in enumerate(["ResolvedSignalRegion","BoostedSignalRegion"]) :
            for j,channel in enumerate(["ElTau","MuTau"]) :  
                print(f"\t {region} {channel}")
                if check(f_prompt, f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR") :
                    h_prompt_tmp   = f_prompt.Get(f"{syst}/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR")
                    h_prompt_tmp.SetDirectory(0)
                    lh_prompt[syst].append(h_prompt_tmp)

                if check(f_prompt, f"{syst}/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR") : 
                    h_fakeMC_tmp   = f_prompt.Get(f"{syst}/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR")
                    h_fakeMC_tmp.SetDirectory(0)
                    lh_fakeMC[syst].append(h_fakeMC_tmp)

        #print(f"\t {lh_prompt}, {lh_fakeMC}")
        h_prompt = TH1D()
        h_fakeMC = TH1D()

        for i1,h1 in enumerate(lh_prompt[syst]):
            if i1 == 0 : 
                h_prompt = h1.Clone("prompt_")
                h_prompt.SetDirectory(0)
            else : h_prompt.Add(h1)

        for i2,h2 in enumerate(lh_fakeMC[syst]):
            if i2 == 0 :
                h_fakeMC = h2.Clone("fakeMCPrompt_")
                h_fakeMC.SetDirectory(0)
            else : h_fakeMC.Add(h2)

        h_prompt.Add(h_fakeMC)
        d_prompt[syst]  = h_prompt 
        #print(d_prompt[syst])
        h_prompt_save = d_prompt[syst].Clone(f"prompt{getSystString(syst)}").Rebin(len(rebins)-1,f"prompt{getSystString(syst)}",array.array('d',rebins))
        h_prompt_save.SetDirectory(0)
        
        d_prompt_save[syst] = h_prompt_save 
        #print(d_prompt_save,d_prompt_save[syst])


    for syst in l_syst_fakes :
        lh_fakeData[syst] = [] 
        if check(f_fake, f"{syst}/{region}_{channel}/ProperMeffWR") :
            h_fakeData_tmp = f_fake.Get(f"{syst}/{region}_{channel}/ProperMeffWR")
            h_fakeData_tmp.SetDirectory(0)
            lh_fakeData[syst].append(h_fakeData_tmp)
        
        h_fakeData = TH1D()    
        for i3,h3 in enumerate(lh_fakeData[syst]):
            if i3 == 0 :
                h_fakeData = h3.Clone("fake_")
                h_fakeData.SetDirectory(0)
            else : h_fakeData.Add(h3)
                
        d_fake[syst] = h_fakeData
        h_fake_save   = h_fakeData.Clone(f"fake{getSystString(syst)}").Rebin(len(rebins)-1,f"fake{getSystString(syst)}",array.array('d',rebins))
        h_fake_save.SetDirectory(0)
        d_fake_save[syst] =  h_fake_save

    h_data_tmp = d_prompt_save["Central"] + d_fake_save["Central"]
    h_data_save = round_histogram(h_data_tmp).Clone(f"data_obs")
    #print(h_data_save.Integral())

    for mwr in d_mass :
        for mn in d_mass[mwr] :

            outfile = TFile.Open(f"Outputs/{inputTag}/{era}/WR{mwr}_N{mn}_card_input.root","RECREATE")
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

                h_signal_save = d_signal[syst].Clone(f"signal{getSystString(syst)}").Rebin(len(rebins)-1,f"signal{getSystString(syst)}",array.array('d',rebins))
                h_signal_save.Scale(GetSignalScale(mwr))
                h_signal_save.SetDirectory(0)

                for item in [d_prompt_save[syst],h_signal_save] :
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
            h_data_save.Write()
            gDirectory.cd(original_directory)
            outfile.Close()
            print(f"Card Input for {mwr}GeV {mn}GeV is done")