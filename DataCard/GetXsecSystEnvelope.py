#!/usr/bin/env python3
from ROOT import *
from utils import *
import os, argparse, array
from datetime import datetime

default_outputdir = f"Plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

parser = argparse.ArgumentParser(description='xsec systematic envelope extractor')
parser.add_argument('-e', dest='era'  , type=str, help='Era to plot', default=2017)
parser.add_argument('-o', dest='out'  , type=str, help='Output directory name',default=default_outputdir)
args = parser.parse_args()

era, out = args.era, args.out 

os.system(f"mkdir -p XsecSyst/{out}/{era}")
os.system(f"mkdir -p XsecSyst/{out}/{era}/Signals")

samplestr = "WRtoTauNtoTauTauJets"

if era == "2018" : 
    d_mass_ = d_mass_2018
    samplestr = "WRtoNTautoTauTauJJ"
else : d_mass_ = d_mass
'''
for bkg in ["Top","Boson_noVJets"] :
    outfile = TFile.Open(f"XsecSyst/{out}/{era}/{bkg}.root","RECREATE")
    inputfile = TFile.Open(f"{os.getenv('WRTau_Output')}/{stamp}/{era}/RunXsecSyst/WRTau_Analyzer_{bkg}.root")
    print(inputfile)
    for p in ["__PromptTau__NonPromptLepton","__PromptTau__PromptLepton"] :
        outfile.cd()
        dir1_obj = outfile.mkdir(p)
        dir1_obj.cd()
        for r1 in ["Boosted","Resolved"] :
            for r2 in ["SignalRegion","SignalRegionMETInvertMTSame","LowMassControlRegion"] :
                if r2 == "LowMassControlRegion" : 
                    rebins_ = rebins_LMCR
                elif r2 == "SignalRegionMETInvertMTSame" :
                    rebins_ = rebins_QCDMR
                else : rebins_ = rebins
                for r3 in ["_ElTau","_MuTau"] :
                    dir2_obj = dir1_obj.mkdir(f"{r1}{r2}{r3}")
                    dir2_obj.cd()
                    l_PDF ,l_scale, l_AlphaS = [] , [] , []
                    for i in [0,1,2,3,4,6,8] :
                        if check(inputfile,f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_Scale_{i}") :
                            h_tmp = inputfile.Get(f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_Scale_{i}").Clone()
                            h = h_tmp.Rebin(len(rebins_)-1,f"{p}_{r1}{r2}{r3}_MeffWR_Scale_{i}",array.array('d',rebins_))
                            l_scale.append(h)
                        else : continue
                    for i in range(0,100) : 
                        if check(inputfile,f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_{i}") :
                            h_tmp = inputfile.Get(f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_{i}").Clone()
                            h = h_tmp.Rebin(len(rebins_)-1,f"{p}_{r1}{r2}{r3}_MeffWR_PDFWeight_{i}",array.array('d',rebins_))
                            l_PDF.append(h)
                        else : continue
                    for i in range(0,2) : 
                        if check(inputfile,f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_PDFAlphaS_{i}") :
                            h_tmp = inputfile.Get(f"Central/{p}/{r1}{r2}{r3}/ProperMeffWR_PDFAlphaS_{i}").Clone()
                            h = h_tmp.Rebin(len(rebins_)-1,f"{p}_{r1}{r2}{r3}_MeffWR_PDFAlphaS_{i}",array.array('d',rebins_))
                            l_AlphaS.append(h)
                        else : continue 
                    if len(l_scale) > 0 : 
                        l_envelope_scale = GetEnvelope(l_scale,f"ScaleUp","",f"ScaleDown","")
                        l_envelope_scale[0].Write()
                        l_envelope_scale[1].Write()
                    if len(l_PDF) > 0 : 
                        l_envelope_PDF = GetEnvelope(l_PDF,f"PDFWeightUp","",f"PDFWeightDown","")
                        l_envelope_PDF[0].Write()
                        l_envelope_PDF[1].Write()
                    if len(l_AlphaS) > 0 : 
                        l_envelope_AlphaS = GetEnvelope(l_AlphaS,f"PDFAlphaSUp","",f"PDFAlphaSDown","")
                        l_envelope_AlphaS[0].Write()
                        l_envelope_AlphaS[1].Write()
    outfile.Close()
'''
outfile_txt = open(f"XsecSyst/{out}/{era}/PDFerr.txt",'w')
for mWR in d_mass_ :
    for mN in d_mass_[mWR] : 
        outfile = TFile.Open(f"XsecSyst/{out}/{era}/Signals/WR{mWR}_N{mN}.root","RECREATE")
        filename = f"{os.getenv('SKFlatOutputDir')}/Run2UltraLegacy_v3/WRTau_Analyzer/{era}/RunXsecSyst__/WRTau_Analyzer_WRtoNTautoTauTauJJ_WR{mWR}_N{mN}.root"
        inputfile = TFile.Open(filename)
        if not inputfile or inputfile.IsZombie() : 
            print(f"Skip {mWR},{mN} ...")
            continue
        #print(inputfile)
        if check(inputfile,f"Central/SignalRegion/Nevents_PDFWeight_MCWeight_0") :
            h_nominal = inputfile.Get("Central/SignalRegion/Nevents_PDFWeight_MCWeight_0")
            nominal = h_nominal.GetBinContent(1)
            diff = 0 
            
            '''
            for i in range(0,100) : 
                if check(inputfile,f"Central/SignalRegion/Nevents_PDFWeight_MCWeight_{i}") :
                    h_tmp = inputfile.Get(f"Central/SignalRegion/Nevents_PDFWeight_MCWeight_{i}").Clone()
                    this_diff = h_tmp.GetBinContent(1) - nominal
                    print(i,abs(this_diff)/nominal)
                    if abs(this_diff)/nominal < 1.0 : diff += this_diff**2 
                else : continue
            '''
            #PDFerr = sqrt(diff)
            #print(f"{mWR},{mN},{PDFerr}/{nominal*100}={PDFerr/nominal*100:.2f}")
            #outfile_txt.write(f"{mWR},{mN},{PDFerr/nominal*100:.2f}\n")
        else : continue
        for r1 in ["Boosted","Resolved"] :
            for r2 in ["SignalRegion","SignalRegionMETInvertMTSame","LowMassControlRegion"] :
                if r2 == "LowMassControlRegion" : 
                    rebins_ = rebins_LMCR
                elif r2 == "SignalRegionMETInvertMTSame" :
                    rebins_ = rebins_QCDMR
                else : rebins_ = rebins
                #print(r1,r2,rebins_,len(rebins_))
                for r3 in ["_ElTau","_MuTau"] :
                    if not check(inputfile,f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_MCWeight_0") : continue
                    outfile.cd()
                    dir1_obj = outfile.mkdir(f"{r1}{r2}{r3}")
                    dir1_obj.cd()
                    l_PDF ,l_scale, l_AlphaS = [] , [] , []
                    #print(f"{r1}{r2}{r3}")
                    d_Scale = {}
                    h_central_ = inputfile.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_MCWeight_0").Clone()
                    h_central  = h_central_.Rebin(len(rebins_)-1,f"Central",array.array('d',rebins_))
                    PDFerr_regional = -999.
                    #l_central = []
                    #for i in range(1,h_central.GetNbinsX()+1) : l_central.append(h_central.GetBinContent(i))
                    #d_Scale["Central"] = l_central
                    for i in [0,1,2,3,4,6,8] :
                        l_tmp = []
                        if check(inputfile,f"Central/{r1}{r2}{r3}/ProperMeffWR_Scale_MCWeight_{i}") :
                            h_tmp = inputfile.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_Scale_MCWeight_{i}").Clone()
                            h = h_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_Scale_MCWeight_{i}",array.array('d',rebins_))
                            l_scale.append(h)
                            for j in range(1,h.GetNbinsX()+1) : l_tmp.append(h.GetBinContent(j))
                            #print(f"\t ScaleVar{i} = [{l_tmp}]")
                            d_Scale[i] = l_tmp
                        else : continue
                    
                    if check(inputfile,f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_MCWeight_0") :
                        h_PDFError = h_central_.Clone("RawPDFCentral")
                        h_PDFErrorUp = h_central_.Clone("RawPDFUp")
                        h_PDFErrorDown = h_central_.Clone("RawPDFDown")
                        d_PDFbins = {}
                        for i in range(0,100) : 
                            h = inputfile.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_MCWeight_{i}").Clone(f"{r1}{r2}{r3}PDF{i}")
                            #h = h_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_PDFWeight_MCWeight_{i}",array.array('d',rebins_))
                            if h.Integral() < 0 : continue
                            val = []
                            for j in range(1,h.GetNbinsX()+1) : 
                                val.append(h.GetBinContent(j))
                            isOK = True 
                            if i != 0 : 
                                iBinMax = len(val) - 1 
                                yMax_tmp = -9999.
                                for i2 in range(0,len(val)) :
                                    if val[i2] > yMax_tmp :
                                        iBinMax = i2 
                                        yMax_tmp = val[i2]
                                yNominal = d_PDFbins[0][iBinMax]
                                yPDFErr = val[iBinMax]
                                if yPDFErr < 0 : isOK = False
                                if yNominal <= 0. : isOK = False 
                                elif abs(yNominal - yPDFErr)/yNominal > 1.0 : isOK = False
                            if not isOK :
                                val = []
                                for k in range(0,len(d_PDFbins[0])) :
                                    val.append(d_PDFbins[0][k])
                            d_PDFbins[i] = val
                            #print(d_PDFbins)
                        for i in range(1,h_central_.GetNbinsX()) :
                            j = i-1
                            bin_central = d_PDFbins[0][j]
                            diff = 0
                            for k in d_PDFbins :
                                this_diff = d_PDFbins[k][j] - bin_central
                                diff += this_diff**2
                            diff = diff/100
                            #print(i,diff)
                            h_PDFError.SetBinContent(i,bin_central)
                            h_PDFError.SetBinError(i,sqrt(diff))
                            if bin_central != 0 : 
                                h_PDFErrorUp.SetBinContent(i,(bin_central+sqrt(diff)))
                                h_PDFErrorDown.SetBinContent(i,max(1e-7, (bin_central-sqrt(diff))))
                            else : 
                                h_PDFErrorUp.SetBinContent(i,0)
                                h_PDFErrorDown.SetBinContent(i,0)
                        h_PDFError.Write()
                        h_PDFErrorUp.Write()
                        h_PDFErrorDown.Write()
                        h_PDFError_Rebin = h_PDFError.Clone("PDFnominal").Rebin(len(rebins_)-1,f"PDFCentral",array.array('d',rebins_))
                        h_PDFErrorUp_Rebin = h_PDFErrorUp.Clone("PDFUp").Rebin(len(rebins_)-1,f"PDFUp",array.array('d',rebins_))
                        h_PDFErrorDown_Rebin = h_PDFErrorDown.Clone("PDFDown").Rebin(len(rebins_)-1,f"PDFDown",array.array('d',rebins_))
                        h_PDFError_Rebin.Write()
                        h_PDFErrorUp_Rebin.Write()
                        h_PDFErrorDown_Rebin.Write()
                        #PDFerr_regional = sqrt(diff)
                        #print(f"\t\t{r1}{r2}{r3} PDF unc = {PDFerr_regional/nominal*100:.2f}")
                    #    h_nominal = inputfile.Get(f"Central/{r1}{r2}{r3}/Nevents_PDFWeight_MCWeight_0")
                    #    nominal = h_nominal.GetBinContent(1)
                    #    diff = 0 
                    #    for i in range(0,100) : 
                    #        if check(inputfile,f"Central/{r1}{r2}{r3}/Nevents_PDFWeight_MCWeight_{i}") :
                    #            h_tmp = inputfile.Get(f"Central/{r1}{r2}{r3}/Nevents_PDFWeight_MCWeight_{i}").Clone()
                    #            this_diff = h_tmp.GetBinContent(1) - nominal
                    #            diff += this_diff**2 
                    #        else : continue
                    #    PDFerr_regional = sqrt(diff)
                    #    #print(f"\t\t{r1}{r2}{r3} PDF unc = {PDFerr_regional/nominal*100:.2f}")
                    if len(l_scale) > 0 : 
                        #print(f"\t\tGetEnvelope...")
                        l_envelope_scale = GetEnvelope(d_Scale,h_central,f"ScaleUp","",f"ScaleDown","")
                        l_envelope_scale[0].Write()
                        l_envelope_scale[1].Write()
                        h_central.Write()
        outfile.Close()
        print(f"{mWR},{mN} done")
outfile_txt.close()