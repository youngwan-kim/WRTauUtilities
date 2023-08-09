#!/usr/bin/env python3

import os, sys, argparse, itertools, array, argparse
from ROOT import *
from datetime import datetime 
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2023) v2.213345661')
parser.add_argument('-a', dest='analyzername', type=str, help='Analyzer name',default="WRTau_SR_Test")
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


def getXsec(mwr,mn) :
    return 1

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

l_vJetID = ["Loose","Medium","Tight"] 
l_vElID = ["VVLoose","Tight"]
l_vMuID = ["VLoose","Tight"]

l_vElID = ["Tight"]
l_vMuID = ["Tight"]


l_vJetID = ["Medium","Tight"] 
l_vElID = ["Tight"]
l_vMuID = ["Tight"]


l_ID = [l_vJetID,l_vElID,l_vMuID]
IDcomb = list(itertools.product(*l_ID))


d_signals = {
    2000 : [500,TColor.GetColor("#FF008E")],
    4000 : [50000,TColor.GetColor("#94FC13")],
}

userflag = ""; savedirsuffix = ""
if args.userflags != "" : 
    userflag = f"{args.userflags}__"
    savedirsuffix = f"_{args.userflags}"

key = "20230807_135454__DeltaTest"

SampleDir = f"{os.getenv('WRTau_Output')}/{key}"

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

l_regions = ["Baseline_MuTau"]
print(l_regions)

plotsavedirname = f"{args.outputdir}{savedirsuffix}" # "PreselectionStudy_Blinded"

os.system(f"mkdir -p ../Plots/{plotsavedirname}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}")

for region in l_regions :

    lep = LeptonString(region)
    lep_ex = LeptonString_Explicit(region)

    if not divfake : SampleDic["Nonprompt"] = ["Nonprompt(#tau_{h},"+lep+")",TColor.GetColor("#0B2447")]
    else : 
        SampleDic["PromptLepton__NonpromptTau__"] = ["Nonprompt #tau_{h}",TColor.GetColor("#19376D")]
        SampleDic["NonpromptLepton__PromptTau__"] = [f"Nonprompt {lep}",TColor.GetColor("#576CBC")]
        SampleDic["NonpromptLepton__NonpromptTau__"] = ["Nonprompt (Both)",TColor.GetColor("#A5D7E8")]

    os.system(f"mkdir -p ../Plots/{plotsavedirname}/{region}")
    os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{region}")
    for (vJ,vEl,vMu) in IDcomb :
        TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"

        # Dictionary structure [bool:Logy , int:rebin , string:xaxislabel , string:outputfilename , double:xmin , double:xmax , list(double):rebinningarray , bool:hastobeblind ]
        VarDic = {
            f"{region}/dPhiMETmu"  : [True,25,"#Delta#phi(#slash{E}_{T},#mu)","dPhiMETmu",0.,6.5],
            f"{region}/dPhiMETtau" : [True,25,"#Delta#phi(#slash{E}_{T},#tau_{h})","dPhiMETtau",0.,6.5],
            f"{region}/dPhimutau"  : [True,25,"#Delta#phi(#mu,#tau_{h})","dPhimutau",0.,6.5],
            f"{region}/dRMETmu"    : [True,25,"#DeltaR(#slash{E}_{T},#mu)","dRMETmu",0.,6.5],
            f"{region}/dRMETtau"   : [True,25,"#DeltaR(#slash{E}_{T},#tau_{h})","dRMETtau",0.,6.5],
            f"{region}/dRmutau"    : [True,25,"#DeltaR(#mu,#tau_{h})","dRmutau",0.,6.5],
        }

        channel = ""

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
            l = TLegend(0.385,0.75,0.865,0.875)
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
            hs.Draw("hist"); h_stackerr.Draw("e2&f&same"); h_data.Draw("hist&e1&p&same"); # h_data_error.Draw("e1&f&same"); # h_stack.Draw("hist&same")

            l2 = TLegend(0.52,0.55,0.865,0.725)
            l2_str = "(m_{W_{R}},m_{N})="

            textSize = 0.625*gStyle.GetPadTopMargin()
            latex.SetTextFont(61)
            latex.SetTextSize(textSize)
            latex.DrawLatex(0.15, 0.815,"CMS")

            latex.SetTextFont(52)
            latex.SetTextSize(0.75*textSize)
            latex.DrawLatex(0.15, 0.765,"Preliminary")

            latex.SetTextFont(42)
            latex.SetTextSize(0.6*textSize)
            lumi = str(getLumi(args.era))
            latex.DrawLatex(0.68, 0.9175,lumi+" fb^{-1} (13 TeV)")

            latex.SetTextFont(42)
            latex.SetTextSize(0.5*textSize)
            latex.DrawLatex(0.15, 0.7,"Baseline Selection")

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
                for mwr in d_signals :
                    l_mn = [100,mwr-100]
                    for mn in l_mn :
                        f_signal = TFile(f"{os.getenv('WRTau_Output')}/{key}/Signals/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mwr}_N{mn}.root")
                        #print(f_signal)
                        h_signal_tmp = f_signal.Get(f"WRTau_SignalSingleTauTrg/{TauID}/{var}")
                        if h_signal_tmp == None : continue
                        h_signal_tmp.SetDirectory(0)
                        if len(VarDic[var]) > 6 : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal").Rebin(len(VarDic[var][6])-1,"",array.array('d',VarDic[var][6]))
                        else : h_signal = h_signal_tmp.Clone(f"{region}_{TauID}_{var}_{mwr}_signal").Rebin(VarDic[var][1])
                        h_signal.SetDirectory(0)
                        h_signal.SetStats(0)
                        h_signal.Scale(d_signals[mwr][0])
                        h_signal.SetLineColor(d_signals[mwr][1])
                        if mn == 100 : h_signal.SetLineStyle(4)
                        h_signal.SetLineWidth(3)
                        l2.AddEntry(h_signal,f"{l2_str}({mwr},{mn})GeV","lf")
                        pad_up.cd()
                        h_signal.Draw("hist&same")


            
            c.cd()
            pad_up.Draw()
            if willBlind and hastobeBlinded :
                c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals_Blinded.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals_Blinded.pdf")
            else : 
                c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals.png")
                if not onlyPNG : c.SaveAs(f"{savedir}/{VarDic[var][3]}_withSignals.pdf")

            c.Close()
