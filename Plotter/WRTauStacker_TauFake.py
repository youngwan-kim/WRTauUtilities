#!/usr/bin/env python3
import os, sys, argparse, itertools, array, argparse
from ROOT import *
from utils import *
from math import sqrt
from datetime import datetime 
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2023) v2.213345661')
parser.add_argument('-a', dest='analyzername', type=str, help='Analyzer name',default="WRTau_Analyzer")
parser.add_argument('-i', dest='input', type=str, help='Input directory timestamp')
parser.add_argument('-e', dest='era', type=str, help='Era to plot', default=2017)
parser.add_argument('--userflags', type=str, help='user flag used', default="")
parser.add_argument('--WJGen', type=str, help='Wjets generator', default="MG")
parser.add_argument('--outputdir', type=str, help='Output directory name',default=default_outputdir)
parser.add_argument('--blind', action='store_true', help='Blind sensitive datapoints')
parser.add_argument('--debugmode', action='store_true', help='debug flag')
parser.add_argument('--onlypng', action='store_true', help='Only save in png')
parser.add_argument('--dividefakes', action='store_true', help='Divide fake contributions')
parser.add_argument('--fakevar', action='store_true', help='variation of fake fit')
args = parser.parse_args()

print("====== Plotter Initialization ======")
print(f"Analyzer : {args.analyzername} ({args.era}) , will be saved in {args.outputdir}")
print(f"Userflags : {args.userflags} ")
print(f"Divide Fakes : {args.dividefakes}")

bst_remove = ["Tight","Jets/Jet","AK4"]
rsv_remove = ["Loose","FatJet"]
presel_remove = ["ProperMTWR","ProperMeffWR","HighPt"]

debug = args.debugmode
willBlind = args.blind
onlyPNG = args.onlypng
wjgen = args.WJGen
fakev = args.fakevar
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

l_SignalRegions = ["ResolvedSignalRegion_ElTau","ResolvedSignalRegion_MuTau",
                   "BoostedSignalRegion_ElTau", "BoostedSignalRegion_MuTau"]


userflag = ""; savedirsuffix = ""
if args.userflags != "" : 
    userflag = f"{args.userflags}__"
    savedirsuffix = f"_{args.userflags}"

branchlist = ["__PromptTau__NonPromptLepton"]
SampleDir = f"{os.getenv('WRTau_Output')}/{args.input}"

# Multiboson+jet : Red~Orange 
# Multitop : Greenish
# QCD : Blue

# prompt_prompt

SampleDic = {

    "Boson" : ["Others",TColor.GetColor("#576CBC")],
    "Top" : ["t#bar{t}+tX", TColor.GetColor("#DE1A1A")],
    "Fakes" : ["Nonprompt",TColor.GetColor("#5FAD56")]

}

# regions to be plotted
l_regions_presels = ["ResolvedSignalRegionMETInvert",
                     "ResolvedLowMassControlRegion"]

l_regions_presels = ["BoostedPreselection"]#,"ResolvedPreselection"]

l_regions_presels = ["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion"]

l_regions_presels = ["BoostedSignalRegion","ResolvedSignalRegion"]
l_regions_presels = ["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert",
                     "BoostedLowMassControlRegion","ResolvedLowMassControlRegion"]

#l_regions_presels = ["BoostedSignalRegion","ResolvedSignalRegion"]

l_regions = [f"{region}{suffix}" for region in l_regions_presels for suffix in ["_ElTau","_MuTau"]] # ,"_ElTau", "_MuTau"

print(l_regions)

plotsavedirname = f"{args.outputdir}{savedirsuffix}"  

os.system(f"mkdir -p ../Plots/{plotsavedirname}/{args.era}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{args.era}")

for region in l_regions :

    lep = LeptonString(region)
    lep_ex = LeptonString_Explicit(region)

    if divfake :
        del SampleDic["Fakes"]
        SampleDic["MCLeptonFake"]  =  [f"Fake {lep} (MC)",TColor.GetColor("#326e2b")]
        SampleDic["DataDrivenTau"] =  ["Fake #tau (Data)", TColor.GetColor("#5FAD56")]   

    os.system(f"mkdir -p ../Plots/{plotsavedirname}/{args.era}/{region}")
    os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{args.era}/{region}")
    for (vJ,vEl,vMu) in IDcomb :
        TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"

        # Dictionary structure [bool:Logy , int:rebin , string:xaxislabel , string:outputfilename , double:xmin , double:xmax , list(double):rebinningarray , bool:hastobeblind ]
        VarDic = {
            f"{region}/Nevents" : [True,1,"nEvents","nEvents",0,1],
            #f"{region}/Cutflow" : [True,1,"Cutflow","Cutflow",0,10],
            f"{region}/MET" : [True,50,"#slash{E}_{T} (GeV)","MET",0.,1000.,[0,50,100,150,225,1000],True],
            f"{region}/Tauh_pT" : [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,800.,[0,190,210,230,250,270,320,800],True],
            f"{region}/Tauh_eta" : [True,4,"Leading Hadronic Tau #eta (GeV)","Tauh_Eta",-3.,3.,[-3.,-2.4,-1.6,-1.0,-0.6,-0.3,0.,0.3,0.6,1.0,1.6,2.4,3.0],False],
            #f"{region}/Jets/FatJet_0_Pt" : [True,100,"Leading AK8 Jet Pt (GeV)","AK8J0_Pt",0.,2500.,[0,100,200,300,400,500,600,700,800,900,1000,2500],True],
            #f"{region}/Jets/FatJet_0_Eta" : [True,2,"Leading AK8 Jet #eta","AK8J0_Eta",-3.,3.],
            #f"{region}/Jets/FatJet_0_LSF" : [True,5,"Leading AK8 Jet LSF_{3}","AK8J0_LSF",0.,1.],
            f"{region}/Jets/Jet_0_Pt" : [True,100,"Leading AK4 Jet Pt (GeV)","AK4j0_Pt",0.,1000.,[0,40,100,200,300,400,1000],True],
            f"{region}/Jets/Jet_0_Eta" : [True,2,"Leading AK4 Jet #eta","AK4j0_Eta",-3.,3.,[-3.,-2.4,-1.6,-1.0,-0.6,-0.3,0.,0.3,0.6,1.0,1.6,2.4,3.0],False],
            f"{region}/Jets/Jet_1_Pt" : [True,50,"Subleading AK4 Jet Pt (GeV)","AK4j1_Pt",0.,1000.,[0,40,80,120,180,300,1000],True],
            f"{region}/Jets/Jet_1_Eta" : [True,5,"Subleading AK4 Jet #eta","AK4j1_Eta",-3.,3.,[-3.,-2.4,-1.6,-1.0,-0.4,0.,0.4,1.0,1.6,2.4,3.0],False],
            f"{region}/HighPtTight/Lepton_0_Pt" : [True,50,f"Leading {lep_ex} Pt (GeV)","TightLep0_Pt",0.,1000.,[0,50,100,150,200,250,350,500,1000],True],
            f"{region}/HighPtTight/Lepton_0_Eta" : [True,2,f"Leading {lep_ex} #eta","TightLep0_Eta",-3.,3.,[-3.0,-2.4,-2.0,-1.6,-1.2,-0.6,0.,0.6,1.2,1.6,2.0,2.4,3.0],False],
            f"{region}/HighPtLoose/Lepton_0_Pt" : [True,50,f"Leading {lep_ex} Pt (GeV)","LooseLep0_Pt",0.,1000.,[0,50,100,150,200,250,400,1000],True],
            f"{region}/HighPtLoose/Lepton_0_Eta" : [True,2,f"Leading {lep_ex} #eta","LooseLep0_Eta",-3.,3.,[-3.0,-2.4,-2.0,-1.6,-1.2,-0.6,0.,0.6,1.2,1.6,2.0,2.4,3.0],False],
            f"{region}/nFatJet" : [True,1,"Number of AK8 Jets","nAK8",0.,10.],
            f"{region}/nJets" : [True,1,"Number of AK4 Jets","nAK4",0.,10.],
            f"{region}/nBJets" : [True,1,"Number of b-Tagged AK4 Jets","nbAK4",0.,10.],
            f"{region}/nLooseLeptons" : [True,1,f"Number of Boosted ID {lep_ex}","nBoostedIDLeps",0.,3.,[0,1,2,3],True],
            f"{region}/nTightLeptons" : [True,1,f"Number of Resolved ID {lep_ex}","nResolvedIDLeps",0.,3.,[0,1,2,3],True],
        }

        channel = ""

        if "Boosted" in region :
            jetstring = "J"
            VarDic = remove_keys_containing_strings(VarDic,bst_remove)
            VarDic[f"{region}/Mthll"]             = [True,200,f"m_{{eff}}(#tau_{{h}}{lep}) [GeV]","Mtl",0.,1500.,[0,50,100,150,250,300,350,400,450,500,550,600,650,700,1000,1500],True]
            VarDic[f"{region}/Mthllmet"]          = [True,200,f"m_{{eff}}(#tau_{{h}}{lep}+#slash{{E}}_{{T}}) [GeV]","Mtl_MET",0.,1500.,[0,50,100,150,300,350,400,450,500,550,750,1000,1500],True]
            #VarDic[f"{region}/BoostedWR_withMET"] = [True,200,f"m_{{eff}}(#tau_{{h}}{lep}J+#slash{{E}}_{{T}}) [GeV]","ProperMeffWR_withMET",0.,5000.,[0,250,500,750,1000,1250,1750,5000],True]
            VarDic[f"{region}/ProperMeffWR"]      = [True,200,f"m_{{eff}}(#tau_{{h}}J+#slash{{E}}_{{T}}) [GeV]","ProperMeffWR",0.,5000.,[0,250,500,750,1000,1250,1750,5000],True]
            VarDic[f"{region}/ProperMTWR"]        = [True,200,f"m_{{T}}(#tau_{{h}}J) [GeV]","ProperMTWR",0.,1000.,[0,50,100,150,250,1000],True]
            #VarDic[f"{region}/dRl0tau"]           = [True,3,"#DeltaR(l,#tau_{h})","dRl0tau",0.,6.]
            VarDic[f"{region}/FatJet/Pt"]         = [True,100,"Leading AK8 Jet Pt (GeV)","AK8J0_Pt",0.,1000.,[0,200,250,300,350,400,550,1000],True]
            VarDic[f"{region}/FatJet/Mass"]       = [True,1,"Leading AK8 Jet Mass [GeV]","AK8J0_Mass",0.,500.,[0,25,50,75,100,150,500],True]
            VarDic[f"{region}/FatJet/SDMass"]     = [True,1,"Leading AK8 Jet Soft Drop Mass [GeV]","AK8J0_SDMass",0.,500.,[0,40,90,150,500],True]
            VarDic[f"{region}/FatJet/Eta"]        = [True,1,"Leading AK8 Jet #eta","AK8J0_Eta",-3.,3.,[-3.0,-2.4,-2.0,-1.6,-1.2,-0.6,0.,0.6,1.2,1.6,2.0,2.4,3.0],False]
            VarDic[f"{region}/FatJet/LSF"]        = [True,5,"Leading AK8 Jet LSF_{3}","AK8J0_LSF",0.,1.]
            VarDic[f"{region}/FatJet/dRJtau"]     = [True,3,"#DeltaR(J_{lead},#tau_{h})","dRtauAK8",0.,6.]
            if "LowMassControlRegion" in region : 
                #VarDic[f"{region}/MET"] = [True,50,"#slash{E}_{T} (GeV)","MET",0.,1000.,[0,50,100,150,200,250,1000],True]
                #VarDic[f"{region}/FatJet/Mass"] = [True,1,"Leading AK8 Jet Mass [GeV]","AK8J0_Mass",0.,500.,[0,25,50,75,100,125,150,500],True]
                #VarDic[f"{region}/FatJet/Pt"] = [True,100,"Leading AK8 Jet Pt (GeV)","AK8J0_Pt",0.,1000.,[0,200,250,300,350,400,450,500,550,600,800,1000],True]
                #VarDic[f"{region}/HighPtLoose/Lepton_0_Pt"] = [True,50,f"Leading {lep_ex} Pt (GeV)","LooseLep0_Pt",0.,1000.,[0,50,150,175,200,300,400,1000],True]
                VarDic[f"{region}/Tauh_pT"] = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,800.,[0,190,210,230,250,270,320,450,800],True]
            if "METInvert" in region :
                VarDic[f"{region}/MET"] = [True,50,"#slash{E}_{T} (GeV)","MET",0.,100.,[0,20,30,40,50,60,70,80,90,100],True]

        if "Resolved" in region : 
            jetstring = "jj"
            VarDic = remove_keys_containing_strings(VarDic,rsv_remove)
            #VarDic[f"{region}/ResolvedWR"]        = [True,50,f"m_{{eff}}(#tau_{{h}}{lep}jj) [GeV]","WRnoMET",0.,4000.,[0,250,300,500,750,1000,1250,1500,1750,2000,2500,3000,4000],True]
            VarDic[f"{region}/Mthlt"]             = [True,50,f"m_{{eff}}(#tau_{{h}}{lep}) [GeV]","Mtl",0.,1500.,[0,100,200,300,400,500,600,1500],True]
            VarDic[f"{region}/Mthltmet"]          = [True,50,f"m_{{eff}}(#tau_{{h}}{lep}+#slash{{E}}_{{T}}) [GeV]","Mtl_MET",0.,1500.,[0,150,250,350,450,550,650,750,850,1500],True]
            #VarDic[f"{region}/BoostedWR_withMET"] = [True,200,f"m_{{eff}}(#tau_{{h}}{lep}J+#slash{{E}}_{{T}}) [GeV]","ProperMeffWR_withMET",0.,5000.,[0,250,500,750,1000,1250,1750,5000],True]
            VarDic[f"{region}/ProperMeffWR"]      = [True,200,f"m_{{eff}}(#tau_{{h}}{lep}jj+#slash{{E}}_{{T}}) [GeV]","ProperMeffWR",0.,5000.,[0,250,500,750,1000,1250,1750,5000],True]
            VarDic[f"{region}/ProperMTWR"]        = [True,200,f"m_{{T}}(#tau_{{h}}{lep}jj) [GeV]","ProperMTWR",0.,800.,[0,50,100,150,200,500],True]
            VarDic[f"{region}/dRtj0"]             = [True,3,"#DeltaR(j_{lead},#tau_{h})","dRtauj0",0.,6.]
            VarDic[f"{region}/dRtj1"]             = [True,3,"#DeltaR(j_{sublead},#tau_{h})","dRtauj1",0.,6.]
            VarDic[f"{region}/Tauh_pT"]           = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,800.,[0,190,210,230,250,270,320,370,450,600,800],True]
            if "METInvert" in region :
                VarDic[f"{region}/MET"]           = [True,50,"#slash{E}_{T} (GeV)","MET",0.,100.,[0,20,30,40,50,60,70,80,90,100],True]
            if "ElTau" in region :
                VarDic[f"{region}/Tauh_pT"]                 = [True,50,"Leading Hadronic Tau Pt (GeV)","Tauh_pT",0.,800.,[0,190,210,230,250,270,320,370,800],True]
                VarDic[f"{region}/HighPtTight/Lepton_0_Pt"] = [True,50,f"Leading {lep_ex} Pt (GeV)","TightLep0_Pt",0.,1000.,[0,50,100,150,200,250,300,350,400,600],True]

        if "LowMassControlRegion" in region : # ProperMTWR < 450
            VarDic[f"{region}/ProperMTWR"] = [True,10,f"m_{{T}}(#tau_{{h}}{lep}{jetstring}) [GeV]","ProperMTWR",0.,450.,[0,50,100,150,200,250,300,350,400,450],True]

        if "ElTau" in region : channel = "e#tau_{h}"
        elif "MuTau" in region : channel = "#mu#tau_{h}"
        else : channel = "e#tau_{h}+#mu#tau_{h}"

        #print(SampleDic)
        if "Preselection" in region : 
            VarDic = remove_keys_containing_strings(VarDic,presel_remove)
            if "Boosted" in region :
                VarDic[f"{region}/Jets/FatJet_0_LSF"] = [True,5,"Leading AK8 Jet LSF_{3}","AK8J0_LSF",0.,1.]

        for var in VarDic : 

            print(var)
            hastobeBlinded = (len(VarDic[var]) == 8) and VarDic[var][7]
            blindbins =[]
            if hastobeBlinded : blindbins = VarDic[var][6][:len(VarDic[var][6])//2]

            print(blindbins)

            if debug : print(f"var : {var} {VarDic[var]}")
            savedir = f"../Plots/{plotsavedirname}/{args.era}/{region}/{TauID}"
            os.system(f"mkdir -p {savedir}")
            os.system(f"cp ../Data/index.php {savedir}")
            c = TCanvas(f"c_{region}_{TauID}_{var}",f"c_{region}_{TauID}_{var}",720,800)
            if debug : print(f"canvas : {c}")
            #l = TLegend(0.415,0.75,0.875,0.875)
            l = TLegend(0.675,0.575,0.875,0.875)
            l.SetNColumns(1)
            latex = TLatex()
            latex.SetNDC()
            l.SetFillStyle(0)
            l.SetBorderSize(0)
            #.SetLegendTextSize(0.1)
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
                f = TFile(f"{SampleDir}/{args.era}/{args.analyzername}_{samplename}.root")
                if debug : print(f"{samplename} file : {f}")
                if divfake :
                    if samplename == "DataDrivenTau" :
                        if fakev : 
                            h = f.Get(f"Central_TauFRWtVarDeg3/{var}")
                            TauFakeNormalization = TauFakeNormalization_deg3 
                        else : h = f.Get(f"Central/{var}") 
                        if not h == None and region not in l_SignalRegions: 
                            h.Scale(getTauFakeNormalization(args.era,region))
                    elif samplename == "MCLeptonFake"  :
                        h = f.Get(f"Central/__PromptTau__NonPromptLepton/{var}") 
                    else : h = f.Get(f"Central/__PromptTau__PromptLepton/{var}")
                else :
                    if samplename == "Fakes" :
                        h1 = f.Get(f"Central/{var}") 
                        if not h1 == None and region not in l_SignalRegions : 
                            #print(f"Fake : {h1.Integral()}")
                            h1.Scale(getTauFakeNormalization(args.era,region))
                            #print(f"Fake : {h1.Integral()}")
                        h2 = f.Get(f"Central/__PromptTau__NonPromptLepton/{var}") 
                        h = h1 + h2 if h1 is not None and h2 is not None else h1 if h1 is not None else h2 if h2 is not None else None
                    else : h = f.Get(f"Central/__PromptTau__PromptLepton/{var}")
                if h == None : continue
                if debug : print(f"{samplename} hist : {h}")
                gROOT.cd()
                if len(VarDic[var]) == 8 : 
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
                if samplename == "Fakes" :
                    for i in range(1,h_tmp_HS.GetNbinsX()) :
                        err0 = h_tmp_HS.GetBinError(i)
                        err1 = GetFakeFitErr(args.input,args.era,var,VarDic,i)
                        err = sqrt(err0**2 + err1**2)
                        h_tmp_HS.SetBinError(i,err)
                if i == 0 :
                    h_stack = h_tmp_ratio.Clone()
                else : h_stack.Add(h_tmp_ratio)
                h_tmp_HS.SetStats(0); h_tmp_HS.SetFillColorAlpha(SampleDic[samplename][1],0.95); h_tmp_HS.SetLineColor(kBlack)
                hs.Add(h_tmp_HS)
                l.AddEntry(h_tmp_HS,SampleDic[samplename][0],"f")
                #print(f"{i} {h_stack.Integral()}")
                i += 1
                #if "Nevents" in var : print(f"{samplename} : {h.Integral()}")

            if "Nevents" in var : print(f"Total : {h_stack.Integral()}")
            # hs          : THStack
            # h_stack     : envelope TH1D of hs 
            # h_tmp_HS    : temp TH1D for calling h_stack
            # h_tmp_ratio : temp TH1D for ratio derivation (=hist of h_stack) 
            '''
            for branch in branchlist :
                j = 0 ; k = 0 
                for samplename in SampleDic : 
                    f = TFile(f"{SampleDir}/{args.era}/{args.analyzername}_{samplename}.root")
                    h = f.Get(f"WRTau_SignalSingleTauTrg{branch}/{TauID}/{var}")
                    if h == None :
                        k += 1
                        continue
                    gROOT.cd()
                    print(f"{samplename} : {h.Integral()}")
                    if len(VarDic[var]) == 7 : 
                        h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                        h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    elif hastobeBlinded :
                        h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                        h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                    else : 
                        h_tmp_HS = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(VarDic[var][1])
                        h_tmp_ratio = h.Clone(f"{region}_{TauID}_{var}_{samplename}{branch}_hist_clone").Rebin(VarDic[var][1])
                    h_tmp_ratio.GetYaxis().SetMaxDigits(2)
                    h_tmp_ratio.GetXaxis().SetLabelSize(0)
                    h_tmp_ratio.Scale(1.08)
                    h_tmp_ratio.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
                    h_tmp_HS.SetFillColorAlpha(SampleDic_NP[branch][1],0.95); h_tmp_HS.SetLineColor(kBlack)
                    #print(f"{j} {branch} {samplename} {SampleDic_NP[branch][1]}")
                    if j == 0 :
                        h_tmp_HS_NP = h_tmp_HS.Clone(f"HS_{region}_{TauID}_{var}_{samplename}{branch}_hist_clone")
                    else :
                        h_tmp_HS_NP += h_tmp_HS
                    h_stack.Add(h_tmp_ratio)
                    j += 1
                #print(f"{branch} loop , h_tmp_HS_NP : {h_tmp_HS_NP}")
                if k == len(SampleDic) : continue
                else :  
                    h_tmp_HS_NP.GetYaxis().SetMaxDigits(2)
                    h_tmp_HS_NP.GetXaxis().SetLabelSize(0) 
                    h_tmp_HS_NP.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
                    h_tmp_HS_NP.Scale(1.08)
                    hs.Add(h_tmp_HS_NP)
                    l.AddEntry(h_tmp_HS_NP,SampleDic_NP[branch][0],"lf")
                    h_stack.GetXaxis().SetLabelSize(0)
                    h_stack.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
                if debug : print(f"THStack : {h_stack}")
            '''
            
            h_stackerr = h_stack.Clone(f"{region}_{TauID}_{var}_hserr")
            h_stackerr.SetStats(0)
            h_stackerr.SetFillStyle(3144)
            h_stackerr.SetFillColorAlpha(12,0.6)
            h_stackerr.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            h_stackerr.GetXaxis().SetLabelSize()
            f_data = TFile(f"{SampleDir}/{args.era}/DATA/{args.analyzername}_DATA.root")
            h_data_tmp = f_data.Get(f"Central/{var}")
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
                h_data_tmp.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][6][:len(VarDic[var][6])//2][-1]) #TEST
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
            #if hastobeBlinded : h_data.GetXaxis().SetRangeUser(VarDic[var][4],VarDic[var][6][:len(VarDic[var][6])//2][-1]) #TEST
            h_data.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            l.AddEntry(h_stackerr,"Pred. Stat.","f")
            l.AddEntry(h_data,"Obs.+Stat.","lp")
            h_data_error = h_data.Clone(f"{region}_{TauID}_{var}_DATA_err_clone")
            h_data_error.SetFillColorAlpha(12,0.6)
            h_data_error.SetFillStyle(3144)
            h_data_error.GetXaxis().SetLabelSize(0)
            h_data_error.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            #if "SignalRegion" in region or "Preselection" in region :
            #    if "Invert" not in region :
            #        for i in range(1,h_data.GetNbinsX()+1):
            #            h_data.SetBinContent(i,0.0)
            ratio = h_data.Clone(f"{region}_{TauID}_{var}_ratio")
            data = h_stack.Clone(f"{region}_{TauID}_{var}_datapoints") #swap
            ratio.Divide(data)
            ratio.SetStats(0)
            if debug : print(ratio)
            ratio_stat = ratio.Clone(f"{region}_{TauID}_{var}_ratio_stat")
            ratio_syst = ratio.Clone(f"{region}_{TauID}_{var}_ratio_syst")

            for r in [ratio,ratio_stat,ratio_syst] :
                r.SetTitle("")
                r.GetXaxis().SetTitle(VarDic[var][2])
                r.GetXaxis().SetTitleSize(0.15)
                r.GetXaxis().SetLabelSize(0.125)
                r.GetXaxis().SetTitleOffset(0.85)
                r.GetYaxis().SetRangeUser(0,2)
                r.GetYaxis().SetLabelSize(0.1)
                r.GetYaxis().SetTitle("Obs./Pred.")
                r.GetYaxis().SetTitleSize(0.125)
                r.GetYaxis().SetTitleOffset(0.35)
                r.GetYaxis().CenterTitle(True)
                r.GetYaxis().SetNdivisions(204)
                r.SetMarkerStyle(8)   
      

            if hastobeBlinded and willBlind : 
                for ibin in range(0,len(VarDic[var][6])) :
                    if not ibin < len(blindbins)+1 : 
                        ratio.SetBinContent(ibin,-99.)
                        ratio_syst.SetBinContent(ibin,-99.)
                        ratio_syst.SetBinError(ibin,0.)
            
            
            ratio.GetXaxis().UnZoom();ratio_syst.GetXaxis().UnZoom()
   
            for i in range(1, ratio_syst.GetNbinsX() + 1):
                ratio_syst.SetBinContent(i, 1.0)

            # Systematic Errors
            for i in range(1, ratio_syst.GetNbinsX() + 1):
                ratio_syst.SetBinError(i, sqrt(getLumiSyst(args.era)**2 + 0.3**2 + ratio.GetBinError(i)**2))

            ratio_syst.SetStats(0)
            ratio_syst.SetFillColorAlpha(kAzure-4,0.6)
            ratio_syst.SetFillStyle(1001)
            ratio_syst.SetMarkerStyle(kDot)
            
            l_max = [] ; l_max.append(hs.GetMaximum()) ; l_max.append(h_data.GetMaximum())
            pad_up.cd()
            h_data.GetYaxis().SetRangeUser(0,max(l_max)*1.8)
            hs.SetMinimum(0); hs.SetMaximum(max(l_max)*1.8)
            if VarDic[var][0] :
                h_data.GetYaxis().SetRangeUser(0.01,max(l_max)*100000)
                hs.SetMinimum(0.01); hs.SetMaximum(max(l_max)*100000)
                pad_up.SetLogy()
            hs.Draw("hist"); h_stackerr.Draw("e2&f&same") # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")
            if "SignalRegion" not in region : 
                h_data.Draw("hist&e1&p&same"); # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")
            elif "Invert" in region : 
                h_data.Draw("hist&e1&p&same"); # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")

            #l1 : 0.675,0.575,0.875,0.875
            l2 = TLegend(0.45,0.69,0.675,0.875)
            l2_str = "(m_{W_{R}},m_{N})="

            textSize = 0.625*gStyle.GetPadTopMargin()
            latex.SetTextFont(61)
            latex.SetTextSize(textSize*1.5)
            latex.DrawLatex(0.15, 0.785,"CMS")

            latex.SetTextFont(52)
            latex.SetTextSize(0.7*textSize)
            latex.DrawLatex(0.15, 0.74,"Work In Progress")

            latex.SetTextFont(42)
            latex.SetTextSize(0.6*textSize)
            lumi = str(getLumi(str(args.era)))
            latex.DrawLatex(0.6, 0.9175,lumi+" fb^{-1} (13 TeV, "+f"{str(args.era)})")

            latex.SetTextFont(42)
            latex.SetTextSize(0.575*textSize)
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
                if "METInvert" in region : 
                    if "Boosted" in region : region_latex = f"Boosted #tau Fake CR"
                    elif "Resolved" in region : region_latex = f"Resolved #tau Fake CR"
                elif "LSFInvert" in region : region_latex = "Boosted Muon Fake CR"
                else :
                    if "Boosted" in region : region_latex = f"Boosted SR{SRdesc}"
                    elif "Resolved" in region : region_latex = f"Resolved SR{SRdesc}"
            latex.DrawLatex(0.15, 0.68,f"{region_latex}")

            metdesc = ""
            #if "MET" in region : 
            #    cutval = region.split("MET")[1].split("_")[0]
            #    metdesc += "(#slash{E}_{T}>"+cutval+"GeV)"

            latex.SetTextSize(0.575*textSize)
            latex.DrawLatex(0.15, 0.65,f"{channel} Channel {metdesc}")

            #latex.SetTextSize(0.5*textSize)
            #latex.DrawLatex(0.125, 0.9175,f"{TauID}")

            l.Draw()

            if debug : print("flag")

            pad_down.cd()

            # legend for ratio pad
            l3 = TLegend(0.55,0.85,0.9,0.961)
            l3.SetNColumns(2)
            l3.SetFillStyle(1001)
            #l3.SetBorderSize(0)
            l3.AddEntry(ratio,"Obs./Pred.","p")
            l3.AddEntry(ratio_syst,"Stat #oplus Syst. Unc.","lpf")

            #ratio.Draw("p&hist&e1")
            ratio_syst.Draw("e2&f") #test ; not real systematic err yet
            ratio.Draw("p&hist&same")
            l3.Draw()

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
                    f_signal = TFile(f"{os.getenv('WRTau_Output')}/{args.input}/{args.era}/Signals/{args.analyzername}_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
                    h_signal_tmp = f_signal.Get(f"Central/{var}")
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
                    h_signal.Scale(0.01*getNormalization(args.era,mwr,mn))
                    scalelabel = "{:.2f}".format(getNormalization(args.era,mwr,mn))
                    h_signal.SetLineColor(d_signals[mwr][1])
                    h_signal.SetLineWidth(3)
                    #l2.AddEntry(h_signal,f"{l2_str}({mwr},{mn})GeV #times {scalelabel}","lf")
                    l2.AddEntry(h_signal,f"({mwr/1000.}, {mn/1000.}) TeV","lf")
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
