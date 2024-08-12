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
l_era = ["2016","Run2"]

rebins = [0,50,100,150,200,500,1000,1500,2000,2500,3000,3500,4000,5000,6000,7000,8000,9000,10000,15000]

inputTag = "240808"
inputDir = f"{os.getenv('WRTau_Output')}/{inputTag}"

#l_era = ["Run2"]
# save root input file with shape of mWR in ResolvedSR / BoostedSR for prompt, fake, signal
# Prompt = shape of mWR in (Resolved+Boosted)SR for prompt MC
# Fake   = shape of mWR in (Resolved+Boosted)SR for fake MC + data-driven tau 
# Signal = shape of mWR in (Resolved+Boosted)SR for signal
for era in l_era : 

    os.system(f"mkdir -p Outputs/{era}")

    f_prompt = TFile.Open(f"{inputDir}/{era}/WRTau_Analyzer_Fakes.root")
    f_fake   = TFile.Open(f"{inputDir}/{era}/WRTau_Analyzer_DataDrivenTau.root")
    f_data   = TFile.Open(f"{inputDir}/{era}/DATA/WRTau_Analyzer_DATA.root")

# fix  script for exceoption skipping (missing branches)

    lh_prompt = []
    lh_fakeMC = []
    lh_fakeData =[]
    lh_Data = []
    l_scale = []

    l_syst = GetSystList(stamp,"Fakes",era) # [central,syst1,syst2,...]
    for syst in l_syst :
        for i,region in enumerate(["ResolvedSignalRegion","BoostedSignalRegion"]) :
            for j,channel in enumerate(["ElTau","MuTau"]) :  
                nPrompt = 0
                nFakeMC = 0
                nFake = 0
                nData = 0
                print(region,channel)
                if check(f_prompt, f"Central/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR") :
                    h_prompt_tmp   = f_prompt.Get(f"Central/__PromptTau__PromptLepton/{region}_{channel}/ProperMeffWR")
                    h_prompt_tmp.SetDirectory(0)
                    lh_prompt.append(h_prompt_tmp)
                    nPrompt += f_prompt.Get(f"Central/__PromptTau__PromptLepton/{region}_{channel}/Nevents").Integral()

                if check(f_prompt, f"Central/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR") : 
                    h_fakeMC_tmp   = f_prompt.Get(f"Central/__PromptTau__NonPromptLepton/{region}_{channel}/ProperMeffWR")
                    h_fakeMC_tmp.SetDirectory(0)
                    lh_fakeMC.append(h_fakeMC_tmp)
                    nFakeMC += f_prompt.Get(f"Central/__PromptTau__NonPromptLepton/{region}_{channel}/Nevents").Integral()

                if check(f_fake, f"Central/{region}_{channel}/ProperMeffWR") :
                    h_fakeData_tmp = f_fake.Get(f"Central/{region}_{channel}/ProperMeffWR")
                    h_fakeData_tmp.SetDirectory(0)
                    #lh_fakeData.append(h_fakeData_tmp)
                    nFake += f_fake.Get(f"Central/{region}_{channel}/Nevents").Integral()

                if check(f_data, f"Central/{region}_{channel}/Nevents") : 
                    h_Data_nEv = f_data.Get(f"Central/{region}_{channel}/Nevents")
                    h_Data_nEv.SetDirectory(0)
                    print(h_Data_nEv.Integral())
                    nData += h_Data_nEv.Integral()

                fakeScale = (nData-nPrompt-nFakeMC)/nFake
                print(nData,nPrompt,nFakeMC,nFake)
                print(fakeScale)

                if check(f_fake, f"Central/{region}_{channel}/ProperMeffWR") :
                    h_fakeData_tmp = f_fake.Get(f"Central/{region}_{channel}/ProperMeffWR")
                    h_fakeData_tmp.SetDirectory(0)
                    h_fakeData_tmp.Scale(fakeScale)
                    lh_fakeData.append(h_fakeData_tmp)
                    nFake += f_fake.Get(f"Central/{region}_{channel}/Nevents").Integral()


        h_prompt = TH1D()
        h_fakeMC = TH1D()
        h_fakeData = TH1D()    

        for i1,h1 in enumerate(lh_prompt):
            if i1 == 0 : 
                h_prompt = h1.Clone("prompt_")
                h_prompt.SetDirectory(0)
            else : h_prompt.Add(h1)

        for i2,h2 in enumerate(lh_fakeMC):
            if i2 == 0 :
                h_fakeMC = h2.Clone("fakeMCPrompt_")
                h_fakeMC.SetDirectory(0)
            else : h_fakeMC.Add(h2)

        for i3,h3 in enumerate(lh_fakeData):
            if i3 == 0 :
                h_fakeData = h3.Clone("fake_")
                h_fakeData.Scale(fakeScale)
                h_fakeData.SetDirectory(0)
            else : h_fakeData.Add(h3)

        h_prompt.Add(h_fakeMC)

        for mwr in d_mass :
            for mn in d_mass[mwr] :

                outfile = TFile.Open(f"Outputs/{era}/WR{mwr}_N{mn}_card_input.root","RECREATE")
                f_signal = TFile.Open(f"{inputDir}/{era}/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")

                for i,region in enumerate(["ResolvedSignalRegion","BoostedSignalRegion"]) :
                    for j,channel in enumerate(["ElTau","MuTau"]) :  
                        if check(f_signal,f"Central/{region}_{channel}/ProperMeffWR") :
                            h_signal_tmp = f_signal.Get(f"Central/{region}_{channel}/ProperMeffWR")
                            h_signal_tmp.SetDirectory(0)
                            if i == 0 and j == 0 :
                                h_signal = h_signal_tmp.Clone(f"signal_{mwr}_{mn}")
                                h_signal.SetDirectory(0)
                            else :
                                h_signal.Add(h_signal_tmp)

                #outfile.cd()

                h_prompt_save = h_prompt.Clone("prompt").Rebin(len(rebins)-1,"prompt",array.array('d',rebins))
                h_prompt_save.SetDirectory(0)
                h_fake_save   = h_fakeData.Clone("fake").Rebin(len(rebins)-1,"fake",array.array('d',rebins))
                h_fake_save.SetDirectory(0)
                h_signal_save = h_signal.Clone("signal").Rebin(len(rebins)-1,"signal",array.array('d',rebins))
                h_signal_save.Scale(GetSignalScale(mwr))
                #h_signal_save.Scale(10)
                h_signal_save.SetDirectory(0)
                h_data_tmp = h_prompt_save + h_fake_save
                h_data_save = round_histogram(h_data_tmp).Clone("data_obs")
                print(h_data_save.Integral())

                for item in [h_prompt_save,h_fake_save,h_signal_save,h_data_save] :
                    original_directory = gDirectory.GetPath()
                    outfile.cd()
                    item.Write()
                    gDirectory.cd(original_directory)

                outfile.Close()