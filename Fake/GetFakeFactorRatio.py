from ROOT import *
import os,array
from utils import *

stamp = "240805"
l_era = ["2016preVFP","2016postVFP","2017","2018"]

pt_bins_ = [190,220,250,350,450,600,1000]
pt_bins_b_ = [190,220,250,350,450,600,1000]

d_bins_era = {

    "SignalRegion" : {
        "2016preVFP" : {   
            "Tauh_pT_0"      : [[150,200,300,450,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,220,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,200,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2016postVFP" : {   
            "Tauh_pT_0"      : [[150,250,350,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,200,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,250,350,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2017" : {   
            "Tauh_pT_0"      : [[190,220,250,350,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,1000],[190,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,220,250,350,450,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,220,250,350,450,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1000,1100,1500,3000],[900,1000,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900,1200,1500,1800,2100,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900,1000,1100,1200,1500,1800,2100,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900,1200,1500,1800,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"]
        },

        "2018" : {   
            "Tauh_pT_0"      : [[190,220,250,350,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,1000],[190,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,220,250,350,450,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,250,350,450,600,1000],[190,220,250,350,450,600,1000],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1000,1100,1500,3000],[900,1000,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900,1200,1500,1800,2100,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900,1000,1100,1200,1500,1800,2100,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900,1200,1500,1800,2500,4000],[900,1000,1100,1200,1500,1800,2100,2500,4000],"m_{Eff} [GeV]"]
        }
    },

    "LowMassControlRegion" : {
        "2016preVFP" : {   
            "Tauh_pT_0"      : [[150,200,250,300,450],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,200,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,250,300,450],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,200,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[0,500,550,600,650,700,800,900],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[0,500,550,600,650,700,800,900],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2016postVFP" : {   
            "Tauh_pT_0"      : [[150,200,250,300,450],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,200,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,250,300,450],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,200,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[0,500,550,600,650,700,800,900],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[0,500,550,600,650,700,800,900],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2017" : {   
           "Tauh_pT_0"      : [[190,250,300,450],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,250,300,450],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,250,300,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[0,500,550,600,650,700,800,900],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[0,500,550,600,650,700,800,900],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2018" : {   
           "Tauh_pT_0"      : [[190,250,300,450],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,250,300,450],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,250,300,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[0,500,550,600,650,700,800,900],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[0,500,550,600,650,700,800,900],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[0,500,550,600,650,700,800,900],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
            }
    },

    "SignalRegionMETInvertMTSame" : {
        "2016preVFP" : {   
            "Tauh_pT_0"      : [[150,200,300,450,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,220,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,200,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2016postVFP" : {               
            "Tauh_pT_0"      : [[150,200,300,450,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[150,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[150,200,220,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[150,200,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        },

        "2017" : {   
            "Tauh_pT_0"      : [[190,300,450,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,220,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
            },

        "2018" : {   
            "Tauh_pT_0"      : [[190,300,450,600],[190,300,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_1"      : [[190,250,350,450,800],[190,250,350,450,800],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_10"      : [[190,220,250,350,450,600],[190,220,250,350,450,600],"p_{T}^{#tau_{h}} [GeV]"],
            "Tauh_pT_11"      : [[190,250,300,400,500],[190,250,300,350,400,450,500,600],"p_{T}^{#tau_{h}} [GeV]"],
            "ProperMeffWR_0" : [[900,1100,1500,2000,4000],[900,1100,1500,2000,4000],"m_{Eff} [GeV]"],
            "ProperMeffWR_1" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_10" : [[900 ,1000,1300,1800,2500],[900 ,1000,1300,1800,2500],"m_{Eff} [GeV]"],
            "ProperMeffWR_11" : [[900 ,1000,1200,1400,1700,2000,2500],[900 ,1000,1200,1400,1700,2000,2500],"m_{Eff} [GeV]"]
        }
    },

}

os.system(f"mkdir -p FakeFactorRatio/{stamp}")

for era in l_era :
    output_file = TFile(f"FakeFactorRatio/{stamp}/{era}.root", 'RECREATE')
    
    for r in ["SignalRegion","LowMassControlRegion","SignalRegionMETInvertMTSame"] :
        d_bins = d_bins_era[r][era]
        for var in ["Tauh_pT","ProperMeffWR"] :
            for DM in [0,1,10,11] :
                pt_bins_ = d_bins[f"{var}_{DM}"][0]
                #pt_bins_b_ = d_bins[f"{var}_{DM}"][1]
                pt_bins_b_ = pt_bins_
                pt_bins = array.array('d',pt_bins_)
                pt_bins_b = array.array('d',pt_bins_b_)
                nTT, nQCD, nPrompt, nData = 0. , 0. , 0. , 0.
                f_data   = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/DATA/WRTau_Analyzer_DATA.root")
                f_prompt = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_Prompt.root")
                f_ttbar  = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_TT.root")
                f_st     = TFile(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/AR/WRTau_Analyzer_ST.root")

                if check(f_prompt,f"Central/__PromptTau/Resolved{r}_DM{DM}/{var}") :
                    h_prompt_resolved = f_prompt.Get(f"Central/__PromptTau/Resolved{r}_DM{DM}/{var}").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
                else : h_prompt_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
                if check(f_prompt,f"Central/__PromptTau/Boosted{r}_DM{DM}/{var}") :
                    h_prompt_boosted  = f_prompt.Get(f"Central/__PromptTau/Boosted{r}_DM{DM}/{var}").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
                else : h_prompt_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

                h_prompt = h_prompt_boosted + h_prompt_resolved

                if check(f_ttbar,f"Central/__NonPromptTau/Resolved{r}_DM{DM}/{var}") :
                    h_ttbar_resolved = f_ttbar.Get(f"Central/__NonPromptTau/Resolved{r}_DM{DM}/{var}").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
                else : h_ttbar_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
                if check(f_ttbar,f"Central/__NonPromptTau/Boosted{r}_DM{DM}/{var}") :
                    h_ttbar_boosted  = f_ttbar.Get(f"Central/__NonPromptTau/Boosted{r}_DM{DM}/{var}").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
                else : h_ttbar_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

                h_ttbar = h_ttbar_resolved + h_ttbar_boosted

                if check(f_st,f"Central/__NonPromptTau/Resolved{r}_DM{DM}/{var}") :
                    h_st_resolved = f_st.Get(f"Central/__NonPromptTau/Resolved{r}_DM{DM}/{var}").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
                else : h_st_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
                if check(f_st,f"Central/__NonPromptTau/Boosted{r}_DM{DM}/{var}") :
                    h_st_boosted  = f_st.Get(f"Central/__NonPromptTau/Boosted{r}_DM{DM}/{var}").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
                else : h_st_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

                h_st = h_st_resolved + h_st_boosted

                if check(f_data,f"Central/Resolved{r}_DM{DM}/{var}") :
                    h_data_resolved = f_data.Get(f"Central/Resolved{r}_DM{DM}/{var}").Rebin(len(pt_bins_)-1,"prompt_res",pt_bins)
                else : h_data_resolved = TH1D("","",len(pt_bins_)-1,pt_bins)
                if check(f_data,f"Central/Boosted{r}_DM{DM}/{var}") :
                    h_data_boosted  = f_data.Get(f"Central/Boosted{r}_DM{DM}/{var}").Rebin(len(pt_bins_b_)-1,"prompt_res",pt_bins_b)
                else : h_data_boosted = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)

                h_data = h_data_resolved + h_data_boosted

                h_fTT_r = TH1D(f"Resolved{r}_DM{DM}_TT_{var}","",len(pt_bins_)-1,pt_bins)
                h_fTT_b = TH1D(f"Boosted{r}_DM{DM}_TT_{var}","",len(pt_bins_b_)-1,pt_bins_b)
                h_fTT = TH1D(f"Inclusive{r}_DM{DM}_TT_{var}","",len(pt_bins_)-1,pt_bins)
                h_fQCD_r = TH1D(f"Resolved{r}_DM{DM}_QCD_{var}","",len(pt_bins_)-1,pt_bins)
                h_fQCD_b = TH1D(f"Boosted{r}_DM{DM}_QCD_{var}","",len(pt_bins_b_)-1,pt_bins_b)
                h_fQCD = TH1D(f"Inclusive{r}_DM{DM}_QCD_{var}","",len(pt_bins_)-1,pt_bins)

                print(h_data.GetNbinsX(),h_ttbar.GetNbinsX(),h_prompt.GetNbinsX())
                for i in range(1,h_data.GetNbinsX()+1) :
                    nData     = h_data.GetBinContent(i)
                    nTT       = h_ttbar.GetBinContent(i)
                    nST       = h_st.GetBinContent(i)
                    nPrompt   = h_prompt.GetBinContent(i)
                    nQCD      = max(0., nData-nTT-nPrompt)

                    nData_r   = h_data_resolved.GetBinContent(i)
                    nTT_r     = h_ttbar_resolved.GetBinContent(i)
                    nST_r     = h_st_resolved.GetBinContent(i)
                    nPrompt_r = h_prompt_resolved.GetBinContent(i)
                    nQCD_r    = max(0., nData_r-nTT_r-nPrompt_r)

                    nData_b   = h_data_boosted.GetBinContent(i)
                    nTT_b     = h_ttbar_boosted.GetBinContent(i)
                    nST_b     = h_st_boosted.GetBinContent(i)
                    nPrompt_b = h_prompt_boosted.GetBinContent(i)
                    nQCD_b    = max(0., nData_b-nTT_b-nPrompt_b)

                    print("Inclusive",i,nTT,nQCD,nData)
                    #print("Resolved",i,nST_r,nTT_r,nQCD_r,nData_r)
                    #print("Boosted",i,nST_b,nTT_b,nQCD_b,nData_b)
                    if nData_b != 0 :
                        fQCD_b = nQCD_b/nData_b
                        fTT_b = nTT_b/nData_b
                        norm_b = 1./(fQCD_b+fTT_b)
                        fQCD_b *= norm_b
                        fTT_b *= norm_b
                        h_fTT_b.SetBinContent(i,fTT_b)
                        h_fQCD_b.SetBinContent(i,fQCD_b)
                        #print("Boosted Ratio : ",i,fQCD_b,fTT_b)

                    if nData_r != 0 :
                        fQCD_r = nQCD_r/nData_r
                        fTT_r = nTT_r/nData_r
                        norm_r = 1./(fQCD_r + fTT_r)
                        fQCD_r *= norm_r 
                        fTT_r *= norm_r
                        h_fTT_r.SetBinContent(i,fTT_r)
                        h_fQCD_r.SetBinContent(i,fQCD_r)
                        #print("Resolved Ratio : ",i,fQCD_r,fTT_r)


                    if nData != 0 :
                        fQCD = nQCD/nData
                        fTT = nTT/nData
                        norm = 1./(fQCD + fTT)
                        fQCD *= norm 
                        fTT *= norm
                        h_fTT.SetBinContent(i,fTT)
                        h_fQCD.SetBinContent(i,fQCD)
                        print(" Ratio : ",i,fQCD,fTT,fQCD+fTT)

                original_directory = gDirectory.GetPath()
                output_file.cd()
                h_fTT_b.Write()
                h_fQCD_b.Write()
                h_fTT_r.Write()
                h_fQCD_r.Write()
                h_fTT.Write()
                h_fQCD.Write()
                gDirectory.cd(original_directory)

                c   = TCanvas(f"{era}_inclusive{r}_DM{DM}_{var}",f"{era}_inclusive{r}_DM{DM}_{var}",1000,1000)
                c_r = TCanvas(f"{era}_resolved{r}_DM{DM}_{var}" ,f"{era}_resolved{r}_DM{DM}_{var}",1000,1000)
                c_b = TCanvas(f"{era}_boosted{r}_DM{DM}_{var}"  ,f"{era}_boosted{r}_DM{DM}_{var}",1000,1000)

                h_dummy = TH1D("","",len(pt_bins_)-1,pt_bins)
                h_dummy.GetYaxis().SetRangeUser(0.0,1.0)
                h_dummy.SetStats(0)
                h_dummy.GetXaxis().SetTitle(d_bins[f"{var}_{DM}"][2])
                h_dummy.GetXaxis().SetTitleSize(0.045)
                h_dummy.GetXaxis().SetLabelSize(0.04)
                h_dummy.GetYaxis().SetTitle("Ratio")
                h_dummy.GetYaxis().SetTitleOffset(1.)
                h_dummy.GetYaxis().SetTitleSize(0.045)

                h_dummy_b = TH1D("","",len(pt_bins_b_)-1,pt_bins_b)
                h_dummy_b.GetYaxis().SetRangeUser(0.01,1.0)
                h_dummy_b.SetStats(0)

                c.cd()
                l = TLegend(0.65,0.7,0.875,0.8)
                l.AddEntry(h_fTT,"Top Pair","f")
                l.AddEntry(h_fQCD,"QCD","f")
                l.SetFillStyle(0)
                l.SetBorderSize(0)
                h_dummy.Draw("h")
                l.Draw()
                #c.SetLogx()
                #c.SetLogy()
                hs = THStack(f"hs{r}_{era}_inclusive","")
                h_fTT.SetFillColor(kRed-7)
                h_fTT.SetLineColor(kBlack)
                hs.Add(h_fTT)
                h_fQCD.SetFillColor(kViolet-9)
                h_fQCD.SetLineColor(kBlack)
                hs.Add(h_fQCD)
                #hs_r.GetXaxis().SetRangeUser(190,1000)
                hs.Draw('same')
                drawLatexNew(r,era,DM)
                l.Draw()
                c.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Inclusive{r}_DM{DM}_{var}.pdf")
                c.SaveAs(f"FakeFactorRatio/{stamp}/{era}_Inclusive{r}_DM{DM}_{var}.png")
