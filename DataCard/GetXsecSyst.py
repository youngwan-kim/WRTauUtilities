#!/usr/bin/env python3
from ROOT import *
from datetime import datetime
from math import sqrt
import os,argparse,array
from utils import *

d_mass_New = { }

for key in range(1000,6501,500) :
    d_mass_New[key] = list(range(100,key,100))

#d_mass_New = {5000:[3800]}

def GetTMPDir() :
    return datetime.now().strftime('%Y%m%d_%H%M%S')

# PDFUnc and AlphaS unc to be saved as csv file 
# Scale envelope as root files
def SignalXsecSyst(era, analyzername, outputdir) :
    outfile_txt = open(f"XsecSyst/{outputdir}/{era}/PDFerr.txt",'w')
    for mWR in d_mass_New :
        for mN in d_mass_New[mWR] :
            outfile = TFile.Open(f"XsecSyst/{outputdir}/{era}/Signals/WR{mWR}_N{mN}.root","RECREATE")
            PDFUnc, PDFAlphaSUnc, ScaleUnc = 0,0,0
            l_PDFError, l_PDFAlphaSError, l_ScaleError = [], [], []
            filename = f"{os.getenv('SKFlatOutputDir')}/Run2UltraLegacy_v3/{analyzername}/{era}/RunXsecSyst__/{analyzername}_WRtoNTautoTauTauJJ_WR{mWR}_N{mN}.root"
            f = TFile.Open(filename)
            print(f)
            if not f or f.IsZombie() : 
                print(f"Missing or wrong file : {filename}")
                continue 
            if not check(f,"XsecSyst/PDFWeights_0") : continue
            h_nominal = f.Get("XsecSyst/PDFWeights_0").Clone()
            #print(h_nominal)
            # get nominal PDF error
            denPDFnominal = 0.
            
            for i in range(1,100) :
                h_err = f.Get(f"XsecSyst/PDFWeights_{i}").Clone()
                denPDFnominal += h_err.GetBinContent(1)
            denPDFnominal = denPDFnominal/100
            denPDFnominal = h_nominal.GetBinContent(1)
            #print(f"{mWR},{mN} PDFUnc calc start... denPDFnominal={denPDFnominal}")
            # PDF error set : replica  case shall be implemented later
            for i in range(0,100) :
                h_error = f.Get(f"XsecSyst/PDFWeights_{i}").Clone()
                if check(f,f"XsecSyst/PDFWeights_{i}") : 
                    this_diff = h_error.GetBinContent(1) - denPDFnominal
                    l_PDFError.append(h_error.GetBinContent(1))
                    PDFUnc += this_diff**2
                    #print(f"\t PDFSet{i} err={this_diff} ,total^2 = {PDFUnc}")
                else : continue
            PDFUnc = sqrt(PDFUnc)
            
            # PDF alphaS
            for i in range(0,2) :
                h_error = f.Get(f"XsecSyst/PDFAlphaS_{i}")
                l_PDFAlphaSError.append(h_error.GetBinContent(i))
            PDFAlphaSUnc = abs(l_PDFAlphaSError[0]-l_PDFAlphaSError[1])/2

            # Scale 
            h_ScaleNominal = f.Get(f"XsecSyst/Scale_0").Clone()
            denScaleNominal = h_ScaleNominal.GetBinContent(1)
            for i in [0,1,2,3,4,6,8] :
                h_error = f.Get(f"XsecSyst/Scale_{i}").Clone()
                ScaleUnc = max(ScaleUnc, abs(h_error.GetBinContent(1)-denScaleNominal))
            print(f"{mWR},{mN} in {era} : PDFUnc = {PDFUnc} , ScaleUnc = {ScaleUnc}")
            print(f"\t\t ( PDFUnc = {PDFUnc/denPDFnominal*100:.2f} , ScaleUnc = {ScaleUnc/denScaleNominal*100:.2f} )")
            outfile_txt.write(f"{mWR},{mN},{PDFUnc/denPDFnominal*100:.2f}\n")
            # Template
            for r1 in ["Boosted","Resolved"] :
                for r2 in ["SignalRegion","SignalRegionMETInvertMTSame","LowMassControlRegion"] :
                    if r2 == "LowMassControlRegion" : 
                        rebins_ = rebins_LMCR
                    elif r2 == "SignalRegionMETInvertMTSame" :
                        rebins_ = rebins_QCDMR
                    else : rebins_ = rebins
                    for r3 in ["_ElTau","_MuTau"] :
                        l_scale = []
                        if not check(f,f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_0") : continue
                        outfile.cd()
                        dir1_obj = outfile.mkdir(f"{r1}{r2}{r3}")
                        dir1_obj.cd()
                       
                        h_central_tmp = f.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_0").Clone()
                        h_central = h_central_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_Central",array.array('d',rebins_))
                        h_Nevents = f.Get(f"Central/{r1}{r2}{r3}/Nevents_PDFWeight_0").Clone()
                        ChannelFrac = 1./l_PDFError[0]*h_Nevents.Integral()
                        h_central.Scale(1./l_PDFError[0])
                        h_central.Scale(1./ChannelFrac)
                        #print(f"{r1}{r2}{r3} {h_Nevents.Integral()}*{h_nominal.GetEntries()} = {h_Nevents.Integral()*h_nominal.GetEntries()}")
                        
                        #print("nominalerror=",l_PDFError[0],"")
                        integral_central = h_central_tmp.Integral()/l_PDFError[0]
                        d_ScalesBin = {}
                        
                        # Scale template
                        integralScale_Max, integralScale_Min = -9999999, 99999999
                        #print(f"\t Start building scale template...")
                        for i in [0,1,2,3,4,6,8] :
                            if check(f,f"Central/{r1}{r2}{r3}/ProperMeffWR_Scale_{i}") :
                                h_tmp = f.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_Scale_{i}").Clone()
                                h = h_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_Scale_{i}",array.array('d',rebins_))
                                #print(i,h.Integral())
                                h.Scale(1./l_PDFError[0])
                                l_scale.append(h)
                                #print(i,h.Integral())
                                vals = []
                                for j in range(1,h.GetNbinsX()+1) :
                                    vals.append(h.GetBinContent(j))
                                #print(f"\t\t {i} shape = {vals}")
                                integralScale_Max = max(integralScale_Max, h.Integral())
                                integralScale_Min = min(integralScale_Min, h.Integral())
                                d_ScalesBin[i] = vals
                            else : continue
                        #print(integralScale_Max,integral_central,integralScale_Min)
                        integralScale_Up = abs(integral_central-integralScale_Max)/integral_central
                        integralScale_Down = abs(integral_central-integralScale_Min)/integral_central
                        #print(mWR,mN,f"{r1}{r2}{r3} scale unc integrated : ",max(integralScale_Up,integralScale_Down))
                        if len(l_scale) > 0 : 
                            l_envelope_scale = GetEnvelope(l_scale,f"ScaleUp","",f"ScaleDown","")
                            l_envelope_scale[0].Write()
                            l_envelope_scale[1].Write()
                        # AlphaS template
                        '''
                        h_AlphaS     = h_central.Clone("AlphaSCentral")
                        h_AlphaSUp   = h_central.Clone("AlphaSUp")
                        h_AlphaSDown = h_central.Clone("AlphaSDown")
                        d_AlphaSBin = {}
                        for i in range(0,2) :
                            if check(f,f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFAlphaS_{i}") :
                                h_tmp = f.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFAlphaS_{i}").Clone()
                                h = h_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_PDFAlphaS_{i}",array.array('d',rebins_))
                                h.Scale(1./l_PDFError[0])
                                l_scale.append(h)
                                vals = []
                                for j in range(1,h_central.GetNbinsX()+1) :
                                    vals.append(h.GetBinContent(j)) 
                                d_AlphaSBin[i] = vals
                                #print(f"d_AlphaSBin[{i}] saved {vals}")
                            else : continue 
                        for i in range(1,h_central.GetNbinsX()) :
                            j = i-1
                            bin_central = h_central.GetBinContent(i)
                            alphaSUp   = d_AlphaSBin[0][j] - bin_central
                            alphaSDown = d_AlphaSBin[1][j] - bin_central
                            this_err = abs(alphaSUp-alphaSDown)/2.
                            h_AlphaS.SetBinContent(i,bin_central)
                            h_AlphaS.SetBinError(i,this_err)
                            h_AlphaSUp.SetBinContent(i,bin_central+this_err)
                            h_AlphaSDown.SetBinContent(i,max(1e-20,bin_central-this_err))
                        h_AlphaS.Write()
                        h_AlphaSUp.Write()
                        h_AlphaSDown.Write()
                        '''
                        # PDF template
                        '''
                        h_PDFError = h_central.Clone("PDFCentral")
                        h_PDFErrorUp = h_central.Clone("PDFWeightUp")
                        h_PDFErrorDown = h_central.Clone("PDFWeightDown")
                        d_PDFbins = {}
                        #print(f"\t Start building PDF template ...")
                        for i in range(0,100) : 
                            h_tmp = f.Get(f"Central/{r1}{r2}{r3}/ProperMeffWR_PDFWeight_{i}").Clone()
                            h = h_tmp.Rebin(len(rebins_)-1,f"{r1}{r2}{r3}_MeffWR_PDFWeight_{i}",array.array('d',rebins_))
                            h.Scale(1/l_PDFError[i])
                            if h.Integral() < 0 : 
                                continue
                            val = []
                            for j in range(1,h.GetNbinsX()+1) : 
                                val.append(h.GetBinContent(j))
                            #print(f"\t\t Set {i} shape = {val}")
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
                                #print(f"\t {i} : {yPDFErr} , {abs(yNominal - yPDFErr)/yNominal}")
                                if yPDFErr < 0 : isOK = False
                                if abs(yNominal - yPDFErr)/yNominal > 1.0 : isOK = False
                                #print(f"\t\t = isOK({isOK})")
                            if not isOK :
                                val = []
                                for k in range(0,len(d_PDFbins[0])) :
                                    val.append(d_PDFbins[0][k])
                            d_PDFbins[i] = val
                        
                        #print(d_PDFbins)
                        
                        for i in range(1,h_central.GetNbinsX()) :
                            j = i-1
                            bin_central = d_PDFbins[0][j]
                            diff = 0
                            for k in d_PDFbins :
                                this_diff = d_PDFbins[k][j] - bin_central
                                diff += this_diff**2
                            h_PDFError.SetBinContent(i,bin_central/ChannelFrac)
                            h_PDFError.SetBinError(i,sqrt(diff)/ChannelFrac)
                            h_PDFErrorUp.SetBinContent(i,(bin_central+sqrt(diff))/ChannelFrac)
                            h_PDFErrorDown.SetBinContent(i,max(1e-20, (bin_central-sqrt(diff))/ChannelFrac))
                            if bin_central!=0 : print(f"\t\t\t {r1}{r2}{r3} bin{i} PDF err = {sqrt(diff)/bin_central*100:.2f}%")
                        h_PDFError.Write()
                        h_PDFErrorUp.Write()
                        h_PDFErrorDown.Write()
                        '''
    outfile_txt.close()

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Get Xsec Systematics')
    parser.add_argument('--era'         , type=str , help='Era' , nargs="+")
    parser.add_argument('--outputdir'   , type=str , help='Output directory to store', default = GetTMPDir())
    parser.add_argument('--analyzername', type=str , help='Analyzer name'            , default = 'WRTau_Analyzer' )
    args = parser.parse_args()
    l_era, analyzername, outputdir = args.era, args.analyzername, args.outputdir
    
    
    for era in l_era : 
        os.system(f"mkdir -p XsecSyst/{outputdir}/{era}/Signals")
        SignalXsecSyst(era, analyzername, outputdir)




