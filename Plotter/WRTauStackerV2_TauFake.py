#!/usr/bin/env python3
import os, sys, argparse, itertools, array, argparse
from ROOT import *
from utils import *
from math import sqrt
from datetime import datetime 
gROOT.SetBatch(True)

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


parser = argparse.ArgumentParser(description='The really not proud stupid effin plotter (2024) v2.22')
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
args = parser.parse_args()

print("====== Plotter Initialization ======")
print(f"Analyzer : {args.analyzername} ({args.era}) , will be saved in {args.outputdir}")
print(f"Userflags : {args.userflags} ")
print(f"Divide Fakes : {args.dividefakes}")

bst_remove = ["Tight","Jets/Jet","AK4"]
rsv_remove = ["Loose","FatJet"]

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

SampleDir  = f"{os.getenv('WRTau_Output')}/{args.input}"
HistmapDir = f"{os.getcwd()}/histCSVs"
plotsavedirname = f"{args.outputdir}{savedirsuffix}"  

l_regions = GetRegionList(HistmapDir)

# Multiboson+jet : blue
# Multitop : Red/Orange
# Fake : green

SampleDic = {

    "QCD"   : ["QCD", TColor.GetColor("#000000")],
    "Boson" : ["Multiboson",TColor.GetColor("#576CBC")],
    "ST" : ["Single Top", TColor.GetColor("#DE1A1A")],
    "TT" : ["Top Pair", TColor.GetColor("#FF5800")],
    "MCLeptonFake" :  ["",TColor.GetColor("#326e2b")],
    "DataDrivenTau":  ["Fake #tau (Data)", TColor.GetColor("#5FAD56")]   

}

os.system(f"mkdir -p ../Plots/{plotsavedirname}/{args.era}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}")
os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{args.era}")

for region in l_regions :

    lep = LeptonString(region)
    lep_ex = LeptonString_Explicit(region)

    SampleDic["MCLeptonFake"][0] = f"Fake {lep} (MC)"

    os.system(f"mkdir -p ../Plots/{plotsavedirname}/{args.era}/{region}")
    os.system(f"cp ../Data/index.php ../Plots/{plotsavedirname}/{args.era}/{region}")
    
    for (vJ,vEl,vMu) in IDcomb :

        TauID = f"vJet{vJ}_vEl{vEl}_vMu{vMu}"

        # Dictionary structure [bool:Logy , int:rebin , string:xaxislabel , string:outputfilename , double:xmin , double:xmax , list(double):rebinningarray , bool:hastobeblind ]
        VarDic = csv2dict(f"{HistmapDir}/{args.era}/{region}/hists.csv",region)
        
        if "ElTau" in region : channel = "e#tau_{h}"
        elif "MuTau" in region : channel = "#mu#tau_{h}"
        else : channel = "e#tau_{h}+#mu#tau_{h}"

        #print(SampleDic)

        for var in VarDic : 

            hastobeBlinded = len(VarDic[var]) == 8 
            blindbins =[]
            if hastobeBlinded : blindbins = VarDic[var][6][:len(VarDic[var][6])//2]

            if debug : print(f"var : {var} {VarDic[var]}")
            savedir = f"../Plots/{plotsavedirname}/{args.era}/{region}/{TauID}"
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
                f = TFile(f"{SampleDir}/{args.era}/{args.analyzername}_{samplename}.root")
                if debug : print(f"{samplename} file : {f}")
                if samplename == "DataDrivenTau" :
                    h = f.Get(f"WRTau_SignalSingleTauTrg/vJetVVVLoose_vEl{vEl}_vMu{vMu}/{var}") 
                    if not h == None : h.Scale(getTauFakeNormalization(args.era))
                elif samplename == "MCLeptonFake"  :
                    h = f.Get(f"WRTau_SignalSingleTauTrg__PromptTau__NonPromptLepton/{TauID}/{var}") 
                else : h = f.Get(f"WRTau_SignalSingleTauTrg__PromptTau__PromptLepton/{TauID}/{var}")
                if h == None : continue
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

            # hs          : THStack
            # h_stack     : envelope TH1D of hs 
            # h_tmp_HS    : temp TH1D for calling h_stack
            # h_tmp_ratio : temp TH1D for ratio derivation (=hist of h_stack) 
            
            h_stackerr = h_stack.Clone(f"{region}_{TauID}_{var}_hserr")
            h_stackerr.SetStats(0)
            h_stackerr.SetFillStyle(3144)
            h_stackerr.SetFillColorAlpha(12,0.6)
            h_stackerr.GetXaxis().SetLimits(VarDic[var][4],VarDic[var][5])
            h_stackerr.GetXaxis().SetLabelSize()
            f_data = TFile(f"{SampleDir}/{args.era}/DATA/{args.analyzername}_DATA.root")
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
                if "Invert" not in region :
                    for i in range(1,h_data.GetNbinsX()+1):
                        h_data.SetBinContent(i,0.0)
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
                if "METInvert" in region : 
                    if "Boosted" in region : region_latex = f"Boosted #tau Fake CR"
                    elif "Resolved" in region : region_latex = f"Resolved #tau Fake CR"
                elif "LSFInvert" in region : region_latex = "Boosted Muon Fake CR"
                else :
                    if "Boosted" in region : region_latex = f"Boosted SR{SRdesc}"
                    elif "Resolved" in region : region_latex = f"Resolved SR{SRdesc}"
            latex.DrawLatex(0.15, 0.7,f"{region_latex}")

            metdesc = ""
            #if "MET" in region : 
            #    cutval = region.split("MET")[1].split("_")[0]
            #    metdesc += "(#slash{E}_{T}>"+cutval+"GeV)"

            latex.SetTextSize(0.5*textSize)
            latex.DrawLatex(0.15, 0.67,f"{channel} Channel {metdesc}")

            latex.SetTextSize(0.5*textSize)
            latex.DrawLatex(0.125, 0.9175,f"{TauID}")

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
                    scalelabel = "{:.2f}".format(getNormalization(args.era,mwr,mn))
                    h_signal.SetLineColor(d_signals[mwr][1])
                    h_signal.SetLineWidth(3)
                    l2.AddEntry(h_signal,f"{l2_str}({mwr},{mn})GeV #times {scalelabel}","lf")
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
