#!/usr/bin/env python3

import os, sys, argparse, itertools, array, argparse
from ROOT import *
from datetime import datetime 
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2023) v2.213345661')
parser.add_argument('-a', dest='analyzername', type=str, help='Analyzer name',default="WRTau_SR_Test")
parser.add_argument('-i', dest='input', type=str, help='Input directory timestamp')
parser.add_argument('-e', dest='era', type=int, help='Era to plot', default=2017)
parser.add_argument('--userflags', type=str, help='user flag used', default="")
parser.add_argument('--WJGen', type=str, help='Wjets generator', default="MG")
parser.add_argument('--outputdir', type=str, help='Output directory name',default=default_outputdir)
parser.add_argument('--blind', action='store_true', help='Blind sensitive datapoints')
parser.add_argument('--debugmode', action='store_true', help='debug flag')
parser.add_argument('--onlypng', action='store_true', help='Only save in png')
parser.add_argument('--dividefakes', action='store_true', help='Divide fake contributions')
args = parser.parse_args()

print("====== Plotter Initialization ======")
print(f"Analyzer : {args.analyzername} ({args.era}) , will be saved in {args.outputdir}")
print(f"Userflags : {args.userflags} ")
print(f"Divide Fakes : {args.dividefakes}")

bst_remove = ["Tight","Jets/Jet","AK4"]
rsv_remove = ["Loose","FatJet"]

def getXsec(mWR,mN) :
    with open(f"{os.getenv('WRTau_Data')}/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])


def getNormalization(era,mwr,mn) :
    return getLumi(str(era))/getXsec(mwr,mn) 


def remove_keys_containing_strings(dic, strings_to_remove):
    keys_to_remove = []

    for key in dic.keys():
        for string in strings_to_remove:
            if string in key:
                keys_to_remove.append(key)
                break
    
    for key in keys_to_remove:
        dic.pop(key)
    
    return dic


def getLumi(era) :
    if era == "2016preVFP" : return 19.5
    elif era == "2016postVFP" : return 16.8
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8

def LeptonString(region) :
    if "ElTau" in region : return "e"
    elif "MuTau" in region : return "#mu"
    else : return "e,#mu"

def LeptonString_Explicit(region) :
    if "ElTau" in region : return "Electron"
    elif "MuTau" in region : return "Muon"
    else : return "Lepton"

debug = args.debugmode
willBlind = args.blind
onlyPNG = args.onlypng
wjgen = args.WJGen
divfake = args.dividefakes

if wjgen not in ["MG","Sherpa"] :
    print(f"{wjgen} is not available")
    exit

print(f"Blinded : {willBlind} , OnlyPNG : {onlyPNG}, Debug : {debug}")
print(f"WJets Generator : {wjgen}")


l_vJetID = ["Tight"] 
l_vElID = ["Tight"]
l_vMuID = ["Tight"]


l_ID = [l_vJetID,l_vElID,l_vMuID]
IDcomb = list(itertools.product(*l_ID))


d_signals = {
    2000 : [50,TColor.GetColor("#94FC13")],
    4000 : [500,TColor.GetColor("#FF008E")],
    4800 : [50000,TColor.GetColor("#00FFD1")],
}


userflag = ""; savedirsuffix = ""
if args.userflags != "" : 
    userflag = f"{args.userflags}__"
    savedirsuffix = f"_{args.userflags}"


SampleDir = f"{os.getenv('WRTau_Output')}/{args.input}"

# Multiboson+jet : Red~Orange 
# Multitop : Greenish
# QCD : Blue

SampleDic = {

    "QCD" : ["QCD",TColor.GetColor("#1F487E")],
    "VVV" : ["VVV",TColor.GetColor("#4E0110")],
    "VV" : ["VV", TColor.GetColor("#DE1A1A")],
    "WJets_MG_TauHLT" : ["W+Jets", TColor.GetColor("#F2C14E")],
    "ST" : ["Single Top", TColor.GetColor("#04471C")],
    "TT" : ["Top Pair", TColor.GetColor("#5FAD56") ],
    "DYJets_MG_TauHLT" : ["DY", TColor.GetColor("#F26419") ],
    
}

l_regions_presels = ["ResolvedPreselection","BoostedPreselection",
                     "ResolvedLowMassControlRegion","BoostedLowMassControlRegion",
                     "ResolvedLowMassControlRegionMass1","BoostedLowMassControlRegionMass1"]


l_regions_presels = ["BoostedPreselection","BoostedLowMassControlRegion","BoostedLowMassControlRegionMass1","BoostedSignalRegion","BoostedSignalRegionMass1"]
#l_regions_presels = [ "BoostedLowMassControlRegionMass1"]

l_regions_presels = ["ResolvedLowMassControlRegion"]

l_regions = [f"{region}{suffix}" for region in l_regions_presels for suffix in ["_MuTau"]] # ,"_ElTau", "_MuTau"

print(l_regions)

plotsavedirname = f"{args.outputdir}{savedirsuffix}"  

os.system(f"mkdir -p ../Plots/{plotsavedirname}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}")

for region in l_regions :

    lep = LeptonString(region)
    lep_ex = LeptonString_Explicit(region)

    if not divfake : SampleDic["Nonprompt"] = ["Nonprompt(#tau_{h},"+lep+")",TColor.GetColor("#0B2447")]
    else : 
        SampleDic["PromptLepton__NonpromptTau__"] = ["NP #tau_{h}",TColor.GetColor("#19376D")]
        SampleDic["NonpromptLepton__PromptTau__"] = [f"NP {lep}",TColor.GetColor("#576CBC")]
        SampleDic["NonpromptLepton__NonpromptTau__"] = ["NP (Both)",TColor.GetColor("#A5D7E8")]

    os.system(f"mkdir -p ../Plots/{plotsavedirname}/{region}")
    os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{region}")
    for (vJ,vEl,vMu) in IDcomb :
        TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"

        # Dictionary structure [bool:Logy , int:rebin , string:xaxislabel , string:outputfilename , double:xmin , double:xmax , list(double):rebinningarray , bool:hastobeblind ]
        VarDic = {
            #f"{region}/Cutflow" : [True,1,"Cutflow","Cutflow",0,10],
            f"{region}/MET" : [True,50,"#slash{E}_{T} (GeV)","MET",0.,1000.,[0,50,100,150,200,250,300,350,1000],True],
            f"{region}/Tauh_pT" : [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,1000.,[0,50,100,150,200,250,300,350,400,450,500,550,600,1000],True],
            f"{region}/Jets/FatJet_0_Pt" : [True,100,"Leading AK8 Jet Pt (GeV)","AK8J0_Pt",0.,2500.,[0,100,200,300,400,500,600,700,800,900,1000,2500],True],
            f"{region}/Jets/FatJet_0_Eta" : [True,2,"Leading AK8 Jet #eta","AK8J0_Eta",-3.,3.],
            f"{region}/Jets/FatJet_0_LSF" : [True,5,"Leading AK8 Jet LSF_{3}","AK8J0_LSF",0.,1.],
            f"{region}/Jets/Jet_0_Pt" : [True,100,"Leading AK4 Jet Pt (GeV)","AK4j0_Pt",0.,2000.,[0,100,200,300,400,600,800,1000,2000],True],
            f"{region}/Jets/Jet_0_Eta" : [True,2,"Leading AK4 Jet #eta","AK4j0_Eta",-3.,3.],
            f"{region}/Jets/Jet_1_Pt" : [True,50,"Subleading AK4 Jet Pt (GeV)","AK4j1_Pt",0.,1200.,[0,50,100,150,200,250,300,400,600,1200],True],
            f"{region}/Jets/Jet_1_Eta" : [True,5,"Subleading AK4 Jet #eta","AK4j1_Eta",-3.,3.],
            f"{region}/HighPtTight/Lepton_0_Pt" : [True,50,f"Leading Tight {lep_ex} Pt (GeV)","TightLep0_Pt",0.,1000.,[0,50,100,150,200,250,300,350,400,500,1000],True],
            f"{region}/HighPtTight/Lepton_0_Eta" : [True,2,f"Leading Tight {lep_ex} #eta","TightLep0_Eta",-3.,3.],
            f"{region}/HighPtLoose/Lepton_0_Pt" : [True,50,f"Leading Loose {lep_ex} Pt (GeV)","LooseLep0_Pt",0.,1000.,[0,50,100,150,200,250,300,350,400,500,1000],True],
            f"{region}/HighPtLoose/Lepton_0_Eta" : [True,2,f"Leading Loose {lep_ex} #eta","LooseLep0_Eta",-3.,3.],
            f"{region}/nFatJet" : [True,1,"Number of AK8 Jets","nAK8",0.,10.],
            f"{region}/nJets" : [True,1,"Number of AK4 Jets","nAK4",0.,10.],
            f"{region}/nBJets" : [True,1,"Number of b-Tagged AK4 Jets","nbAK4",0.,10.],
            f"{region}/nLooseLeptons" : [True,1,f"Number of Loose {lep_ex}","nLooseLeps",0.,3.,[0,1,2,3],True],
            f"{region}/nTightLeptons" : [True,1,f"Number of Tight {lep_ex}","nTightLeps",0.,3.,[0,1,2,3],True],
        }

        channel = ""

        #if "ElTau" in region or "MuTau" in region :
            #del VarDic[f"{region}/Cutflow"]
            #del VarDic[f"{region}/MET"]

        if "Boosted" in region :
            VarDic = remove_keys_containing_strings(VarDic,bst_remove)
            VarDic[f"{region}/ProperMeffWR"] = [True,200,f"m(#tau_{{h}}{lep}J) [GeV]","ProperMeffWR",0.,5000.]
            VarDic[f"{region}/ProperMTWR"] = [True,200,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","ProperMTWR",0.,5000.,[0,200,400,600,800,1500,5000],True]
            VarDic[f"{region}/dRl0tau"] = [True,3,"#DeltaR(l,#tau_{h})","dRl0tau",0.,6.]
            VarDic[f"{region}/MET2ST_loose"] = [True,1,"#slash{E^{2}}_{T}/ST (GeV)","MET2ST",0.,100.,[0.,5.,10.,15.,20.,25.,30.,100],True]
            VarDic[f"{region}/Jets/FatJet_0_Mass"] = [True,1,"Leading AK8 Jet Mass [GeV]","AK8J0_Mass",0.,1000.,[0,50,100,150,200,250,300,350,450,1000],True]
            VarDic[f"{region}/dRtJ0"] = [True,3,"#DeltaR(J_{lead},#tau_{h})","dRtauAK8",0.,6.]
            if "LowMassControlRegion" in region : 
                VarDic[f"{region}/MET"] = [True,50,"#slash{E}_{T} (GeV)","MET",0.,1000.,[0,50,100,150,200,1000],True]
                VarDic[f"{region}/Jets/FatJet_0_Mass"] = [True,1,"Leading AK8 Jet Mass [GeV]","AK8J0_Mass",0.,500.,[0,25,50,75,100,125,150,500],True]
                #VarDic[f"{region}/MTBoostedWR"] = [True,5,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","MTthlJ",0.,1000.,[0,25,50,75,100,125,150,175,200,225,250,275,300,400,600,800,1000],True]
                VarDic[f"{region}/Jets/FatJet_0_Pt"] = [True,100,"Leading AK8 Jet Pt (GeV)","AK8J0_Pt",0.,1000.,[0,200,250,300,350,400,450,500,550,600,800,1000],True]
                VarDic[f"{region}/HighPtLoose/Lepton_0_Pt"] = [True,50,f"Leading Loose {lep_ex} Pt (GeV)","LooseLep0_Pt",0.,500.,[0,50,60,70,80,90,100,125,150,175,200,300,400,500],True]
                #VarDic[f"{region}/Tauh_pT"] = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,1000.]#,[0,190,210,230,250,270,290,310,330,350,370,600,1000],True] #[0,190,210,235,300,350,360,375,600,1000]
                VarDic[f"{region}/Tauh_pT"] = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,1000.,[0,190,210,250,300,350,400,450,500,550,600,1000],True] #[0,190,210,235,300,350,360,375,600,1000]
            #elif "SignalRegion" in region :
            #        VarDic[f"{region}/MTBoostedWR"] = [True,5,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","MTthlJ",600.,4800.,[600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800],True]            
            #else : 
            #    VarDic[f"{region}/MTBoostedWR"] = [True,5,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","MTthlJ",0.,1000.,[0,50,100,150,200,250,300,400,600,1000],True]

        if "Resolved" in region : 
            VarDic = remove_keys_containing_strings(VarDic,rsv_remove)
            VarDic[f"{region}/ResolvedWR"] = [True,50,f"m(#tau_{{h}}{lep}J)","WRnoMET",0.,5000.,[0,250,500,750,1000,1250,1500,1750,2000,2500,5000],True]
            VarDic[f"{region}/Mthlt"] = [True,50,f"m(#tau_{{h}}{lep}) [GeV]","Mtl_t",0.,5000.,[0,250,500,750,1000,1250,1500,1750,2000,2500,5000],True]
            VarDic[f"{region}/Mthltmet"] = [True,50,f"m_{{eff}}(#tau_{{h}}{lep}#slash{{E}}_{{T}}) [GeV]","Mtl_t_MET",0.,5000.,[0,250,500,750,1000,1250,1500,1750,2000,2500,5000],True]
            VarDic[f"{region}/MTtauhtightlep"] = [True,50,f"m_{{T}}(#tau_{{h}}{lep}) [GeV]","MTthl",0.,1000.,[0,50,100,150,200,250,300,400,600,1000],True]
            VarDic[f"{region}/ResolvedWR_withMET"] = [True,50,f"m_{{eff}}(#tau_{{h}}{lep}jj) [GeV]","WRwithMET",0.,5000.,[0,250,500,750,1000,1250,1500,1750,2000,2500,5000],True]
            VarDic[f"{region}/MET2ST_tight"] = [True,1,"#slash{E^{2}}_{T}/ST (GeV)","MET2ST",0.,100.,[0.,5.,10.,15.,20.,25.,30.,100],True]
            VarDic[f"{region}/dRtj0"] = [True,3,"#DeltaR(j_{lead},#tau_{h})","dRtauj0",0.,6.]
            VarDic[f"{region}/dRtj1"] = [True,3,"#DeltaR(j_{sublead},#tau_{h})","dRtauj1",0.,6.]
            if "LowMassControlRegion" in region : 
                VarDic[f"{region}/MTResolvedWR"] = [True,50,f"m_{{T}}(#tau_{{h}}{lep}jj) [GeV]","MTthjj",0.,800.,[0,50,100,150,200,250,300,400,600,800],True]
                VarDic[f"{region}/Jets/Jet_0_Pt"] = [True,100,"Leading AK4 Jet Pt (GeV)","AK4j0_Pt",0.,1000.,[0,40,100,150,200,250,300,350,400,500,600,700,800,900,1000],True]
                VarDic[f"{region}/Jets/Jet_1_Pt"] = [True,50,"Subleading AK4 Jet Pt (GeV)","AK4j1_Pt",0.,300.,[0,10,20,30,40,50,60,70,80,90,100,125,300],True]
                VarDic[f"{region}/HighPtLoose/Lepton_0_Pt"] = [True,50,f"Leading Loose {lep_ex} Pt (GeV)","LooseLep0_Pt",0.,1000.,[0,50,100,200,400,600,1000],True]
                VarDic[f"{region}/Tauh_pT"] = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,1000.,[0,190,250,300,350,400,450,500,550,600,1000],True] #[0,190,200,210,220,230,240,250,500]
            else : 
                VarDic[f"{region}/MTResolvedWR"] = [True,50,f"m_{{T}}(#tau_{{h}}{lep}jj) [GeV]","MTthjj",0.,1000.,[0,50,100,150,200,250,300,400,600,1000],True]

        #if "Mass1" in region :
        #    if "LowMassControlRegion" in region :
        #        VarDic[f"{region}/ProperMRecoNu"] = [True,50,"m_{W_{R}}^{#nu_{Reco}} [GeV]","NuRecoWRMass",0.,1500.,[0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500],True]
        #        VarDic[f"{region}/ProperMRecoNu_N"] = [True,50,"m_{N}^{#nu_{Reco}} [GeV] [GeV]","NuRecoNMass",0.,250.,[0,25,50,75,100,125,150,175,200,225,250],True]
        #elif "LowMassControlRegion" in region : 
        #    VarDic[f"{region}/ProperMTWR"] = [True,50,"m_{W_{R}} [GeV]","MTWR",0.,800.,[0,100,200,300,400,500,600,800],True]

        if "Mass1" in region :
            if "LowMassControlRegion" in region : # ProperMeffWR < 800
                VarDic[f"{region}/ProperMeffWR"] = [True,10,f"m(#tau_{{h}}{lep}J) [GeV]","ProperMeffWR",0.,800.,[0,350,550,600,650,700,750,800],True]
            elif "SignalRegion" in region : 
                VarDic[f"{region}/ProperMeffWR"] = [True,10,f"m(#tau_{{h}}{lep}J) [GeV]","ProperMeffWR",800.,2500.,[800,1000,1200,1500,1800,2000,2500],True]
        else :
            if "LowMassControlRegion" in region : # ProperMTWR < 250
                VarDic[f"{region}/ProperMTWR"] = [True,10,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","ProperMTWR",0.,250.,[0,50,100,150,200,250],True]
            elif "SignalRegion" in region : 
                VarDic[f"{region}/ProperMTWR"] = [True,10,f"m_{{T}}(#tau_{{h}}{lep}J) [GeV]","ProperMTWR",250,2000,[250,300,350,400,450,500,550,600,650,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000],True]

        if "ElTau" in region : channel = "e#tau_{h}"
        elif "MuTau" in region : channel = "#mu#tau_{h}"
        else : channel = "e#tau_{h}+#mu#tau_{h}"

        for var in VarDic : 

            hastobeBlinded = len(VarDic[var]) == 8 
            blindbins =[]
            if hastobeBlinded : blindbins = VarDic[var][6][:len(VarDic[var][6])//2]

            if debug : print(f"var : {var} {VarDic[var]}")
            savedir = f"../Plots/{plotsavedirname}/{region}/{TauID}"
            os.system(f"mkdir -p {savedir}")
            os.system(f"cp ../Data/index.php {savedir}")
            c = TCanvas(f"c_{region}_{TauID}_{var}",f"c_{region}_{TauID}_{var}",720,800)
            if debug : print(f"canvas : {c}")
            l = TLegend(0.415,0.7,0.865,0.875)
            l.SetNColumns(3)
            latex = TLatex()
            latex.SetNDC()
            l.SetFillStyle(0)
            l.SetBorderSize(0)
            pad_up = TPad(f"pu_{region}_{TauID}_{var}",f"pu_{region}_{TauID}_{var}",0,0.25,1,1)
            pad_up.SetBottomMargin(0.02)
            pad_down = TPad(f"pd_{region}_{TauID}_{var}",f"pd_{region}_{TauID}_{var}",0,0,1,0.25)
            pad_down.SetGrid(1)
            pad_down.SetTopMargin(0.0315)
            pad_down.SetBottomMargin(0.3)
            hs = THStack(f"hs_{region}_{TauID}_{var}",f"hs_{region}_{TauID}_{var}")
            i = 0
            for samplename in SampleDic :
                if debug : print(f"{i} : {samplename}")
                f = TFile(f"{SampleDir}/{args.analyzername}_{samplename}.root")
                if debug : print(f"{samplename} file : {f}")
                h = f.Get(f"WRTau_SignalSingleTauTrg/{TauID}/{var}")
                if h == None : continue
                #    print(f"no hist {samplename}")
                #    if var == f"{region}/Cutflow" : h = f.Get(f"WRTau_SignalSingleTauTrg/{TauID}/{var}/Cutflow")
                #    else : continue
                if debug : print(f"{samplename} hist : {h}")
                gROOT.cd()
                if len(VarDic[var]) == 7 : 
                    h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                elif hastobeBlinded :
                    h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                else : 
                    h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(VarDic[var][1])
                    h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}_hist_clone").Rebin(VarDic[var][1])
                h_tmp_HS.GetYaxis().SetMaxDigits(2); h_tmp_ratio.GetYaxis().SetMaxDigits(2)
                h_tmp_HS.GetXaxis().SetLabelSize(0); h_tmp_ratio.GetXaxis().SetLabelSize(0)
                h_tmp_HS.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5]); h_tmp_ratio.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
                h_tmp_HS.Scale(1.08); h_tmp_ratio.Scale(1.08)
                if i == 0 :
                    h_stack = h_tmp_ratio.Clone()
                else : h_stack.Add(h_tmp_ratio)
                h_tmp_HS.SetStats(0); h_tmp_HS.SetFillColorAlpha(SampleDic[samplename][1],0.95); h_tmp_HS.SetLineColor(kBlack)
                hs.Add(h_tmp_HS)
                l.AddEntry(h_tmp_HS,SampleDic[samplename][0],"lf")
                i += 1
                h_stack.GetXaxis().SetLabelSize(0)
                h_stack.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
                if debug : print(f"THStack : {h_stack}")


            h_stackerr = h_stack.Clone(f"{region}_{TauID}_{var}_hserr")
            h_stackerr.SetStats(0)
            h_stackerr.SetFillStyle(3144)
            h_stackerr.SetFillColorAlpha(12,0.6)
            h_stackerr.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            h_stackerr.GetXaxis().SetLabelSize()
            f_data = TFile(f"{SampleDir}/DATA/{args.analyzername}_DATA.root")
            h_data_tmp = f_data.Get(f"WRTau_SignalSingleTauTrg/{TauID}/{var}")
            if h_data_tmp == None : continue
            if debug : print(f"DATA file : {f_data}")
            if debug : print(h_data_tmp)
            hs.SetTitle("")
            hs.Draw()
            hs.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            hs.GetXaxis().SetLabelSize(0)
            hs.GetYaxis().SetTitle("Events/Bin")
            hs.GetYaxis().SetTitleSize(0.0425)
            hs.GetYaxis().SetTitleOffset(1.025)
            if debug : print(hs)
            if len(VarDic[var]) == 7 : h_data = h_data_tmp.Clone(f"{region}_{TauID}_{var}_DATA_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
            elif hastobeBlinded :
                #h_data_tmp.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][6][:len(VarDic[var][6])//2][-1])
                h_data = h_data_tmp.Clone(f"{region}_{TauID}_{var}_DATA_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                if willBlind : h_data.GetXaxis().SetRange(1,len(blindbins))
            else : h_data = h_data_tmp.Clone(f"{region}_{TauID}_{var}_DATA_clone").Rebin(VarDic[var][1])
            h_data.SetStats(0) 
            h_data.SetMarkerStyle(8)
            h_data.SetLineColor(kBlack)
            h_data.SetFillColorAlpha(12,0.6)
            h_data.SetFillStyle(3144)
            h_data.Sumw2(False)
            h_data.SetBinErrorOption(TH1.kPoisson)
            h_data.GetXaxis().SetLabelSize(0)
            #if hastobeBlinded : h_data.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][6][:len(VarDic[var][6])//2][-1])
            h_data.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            l.AddEntry(h_stackerr,"Pred. Stat.","f")
            l.AddEntry(h_data,"Obs.+Stat.","lp")
            h_data_error = h_data.Clone(f"{region}_{TauID}_{var}_DATA_err_clone")
            h_data_error.SetFillColorAlpha(12,0.6)
            h_data_error.SetFillStyle(3144)
            h_data_error.GetXaxis().SetLabelSize(0)
            h_data_error.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            if "SignalRegion" in region or "Preselection" in region :
                    for i in range(1,h_data.GetNbinsX()+1):
                        h_data.SetBinContent(i,0.0)
            ratio = h_data.Clone(f"{region}_{TauID}_{var}_ratio")
            data = h_stack.Clone(f"{region}_{TauID}_{var}_datapoints") #swap
            ratio.Divide(data)
            ratio.SetStats(0)
            if debug : print(ratio)
            ratio_syst = ratio.Clone(f"{region}_{TauID}_{var}_ratio_syst")
            ratio_syst.SetStats(0)
            ratio_syst.SetFillColorAlpha(12,0.6)
            ratio_syst.SetFillStyle(3144)
            ratio.SetTitle("")
            ratio.GetXaxis().SetTitle(VarDic[var][2])
            ratio.GetXaxis().SetTitleSize(0.15)
            ratio.GetXaxis().SetLabelSize(0.125)
            ratio.GetXaxis().SetTitleOffset(0.85)

            ratio.GetYaxis().SetRangeUser(0,2)
            ratio.GetYaxis().SetLabelSize(0.1)
            ratio.GetYaxis().SetTitle("Obs./Pred.")
            ratio.GetYaxis().SetTitleSize(0.125)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetYaxis().CenterTitle(True)
            ratio.GetYaxis().SetNdivisions(204)
            ratio.SetMarkerStyle(7)   
      

            if hastobeBlinded and willBlind : 
                for ibin in range(0,len(VarDic[var][6])) :
                    if not ibin < len(blindbins)+1 : 
                        ratio.SetBinContent(ibin,-99.)
                        ratio_syst.SetBinContent(ibin,-99.)
                        ratio_syst.SetBinError(ibin,0.)
            
            ratio.GetXaxis().UnZoom();ratio_syst.GetXaxis().UnZoom()
   
            l_max = [] ; l_max.append(hs.GetMaximum()) ; l_max.append(h_data.GetMaximum())
            pad_up.cd()
            h_data.GetYaxis().SetRangeUser(0,max(l_max)*1.8)
            hs.SetMinimum(0); hs.SetMaximum(max(l_max)*1.8)
            if VarDic[var][0] :
                h_data.GetYaxis().SetRangeUser(0.01,max(l_max)*100000)
                hs.SetMinimum(0.01); hs.SetMaximum(max(l_max)*100000)
                pad_up.SetLogy()
            hs.Draw("hist"); h_stackerr.Draw("e2&f&same") # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")
            if "SignalRegion" not in region : h_data.Draw("hist&e1&p&same"); # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")


            l2 = TLegend(0.52,0.525,0.865,0.685)
            l2_str = "(m_{W_{R}},m_{N})="

            textSize = 0.625*gStyle.GetPadTopMargin()
            latex.SetTextFont(61)
            latex.SetTextSize(textSize)
            latex.DrawLatex(0.15, 0.815,"CMS")

            latex.SetTextFont(52)
            latex.SetTextSize(0.6*textSize)
            latex.DrawLatex(0.15, 0.78,"Work In Progress")

            latex.SetTextFont(42)
            latex.SetTextSize(0.6*textSize)
            lumi = str(getLumi(str(args.era)))
            latex.DrawLatex(0.6, 0.9175,lumi+" fb^{-1} (13 TeV, "+f"{str(args.era)})")

            latex.SetTextFont(42)
            latex.SetTextSize(0.5*textSize)
            if "Preselection" in region : 
                region_latex = region.split("Preselection")[0]+" Preselection"
            elif "LowMassControlRegion" in region :
                if "Boosted" in region : region_latex = "Boosted Low Mass CR"
                elif "Resolved" in region : region_latex = "Resolved Low Mass CR"
            elif "SignalRegion" in region :
                SRdesc = ""
                if args.userflags == "" : SRdesc = ""
                elif args.userflags == "inverseMETcut" : SRdesc = " (Inverse #slash{E}_{T})"
                elif args.userflags == "NbGt0" : SRdesc = " (N_{b}#geq1)"
                if "Boosted" in region : region_latex = f"Boosted SR{SRdesc}"
                elif "Resolved" in region : region_latex = f"Resolved SR{SRdesc}"
            latex.DrawLatex(0.15, 0.7,f"{region_latex}")

            metdesc = ""
            if "MET" in region : 
                cutval = region.split("MET")[1].split("_")[0]
                metdesc += "(#slash{E}_{T}>"+cutval+"GeV)"

            latex.SetTextSize(0.5*textSize)
            latex.DrawLatex(0.15, 0.67,f"{channel} Channel {metdesc}")

            latex.SetTextSize(0.5*textSize)
            latex.DrawLatex(0.125, 0.9175,f"{TauID}")

            l.Draw()

            if debug : print("flag")

            pad_down.cd()

            ratio.Draw("p&hist")
            ratio_syst.Draw("e2&f&same")
            c.cd()
            pad_down.Draw()
            pad_up.Draw()
            if willBlind and hastobeBlinded : 
                c.SaveAs(f"{savedir}/{VarDic[var][3]}_Blinded.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}_Blinded.pdf")
            else : 
                c.SaveAs(f"{savedir}/{VarDic[var][3]}.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}.pdf")   

            pad_up.cd()
            l2.SetFillStyle(0)
            l2.SetBorderSize(0)
            l2.Draw()
            if len(d_signals) > 0 :
                ind = 0
                for mwr in d_signals :
                    if "Boosted" in region : mn = 200
                    elif "Resolved" in region : mn = mwr-100    
                    f_signal = TFile(f"{os.getenv('WRTau_Output')}/{args.input}/Signals/{args.analyzername}_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
                    h_signal_tmp = f_signal.Get(f"WRTau_SignalSingleTauTrg/{TauID}/{var}")
                    if h_signal_tmp == None : continue
                    h_signal_tmp.SetDirectory(0)
                    #print(h_signal_tmp)
                    #h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal_{ind}").Rebin(VarDic[var][1])
                    #if len(VarDic[var]) > 6 : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal_{ind}").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    #else : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal_{ind}").Rebin(VarDic[var][1])
                    if len(VarDic[var]) <= 6 : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal_{ind}").Rebin(VarDic[var][1],f"{ind}signal")
                    else : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal_{ind}").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    
                    h_signal.SetDirectory(0)
                    h_signal.SetStats(0)
                    h_signal.Scale(getNormalization(args.era,mwr,mn))
                    h_signal.SetLineColor(d_signals[mwr][1])
                    h_signal.SetLineWidth(3)
                    l2.AddEntry(h_signal,f"{l2_str}({mwr},{mn})GeV","lf")
                    #l2.AddEntry(h_signal,f"{l2_str}({mwr},{mn})GeV#times{d_signals[mwr][0]}","lf")
                    pad_up.cd()
                    #print(h_signal)
                    #print(len(VarDic[var]))
                    #print(VarDic[var])
                    h_signal.Draw("hist&same")
                    ind += 1


            
            c.cd()
            pad_up.Draw()
            if willBlind and hastobeBlinded :
                c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals_Blinded.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals_Blinded.pdf")
            else : 
                c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals.pdf")

            c.Close()
