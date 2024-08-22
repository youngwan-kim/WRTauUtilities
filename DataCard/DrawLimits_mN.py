from ROOT import *
from utils import *
import os
from array import array

inputDir = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/DataCard/Limits/"
WP = "240808"

l_mn = [200]

inputDir += WP

for era in ["2017"] :
    os.system(f"mkdir -p Plots/{WP}/{era}")
    for mn in l_mn :
        c = TCanvas(f"{era}_N{mn}",f"{era}_N{mn}",1000,1000)
        c.SetLeftMargin(0.125)
        c.SetRightMargin(0.05)
        l_mass = [] ; l_twoSigmaL = [] ; l_oneSigmaL = [] ; l_limit = [] ; l_oneSigmaR = [] ; l_twoSigmaR = []

        l_theory = []
        
        for mwr_lines in open(f"{inputDir}/{era}/N{mn}.txt").readlines() :
            
            mass      = float(mwr_lines.split()[0])
            scale = GetSignalScale(mass)
            obs       = float(mwr_lines.split()[1])
            twoSigmaL = float(mwr_lines.split()[2]) * scale
            oneSigmaL = float(mwr_lines.split()[3]) * scale  
            limit     = float(mwr_lines.split()[4]) * scale 
            oneSigmaR = float(mwr_lines.split()[5]) * scale 
            twoSigmaR = float(mwr_lines.split()[6]) * scale 

            if limit <= 0 : continue

            oneSigmaL = limit - oneSigmaL
            oneSigmaR = oneSigmaR - limit
            twoSigmaL = limit - twoSigmaL
            twoSigmaR = twoSigmaR - limit

            l_mass.append(mass)
            l_limit.append(limit)
            l_twoSigmaL.append(twoSigmaL)
            l_oneSigmaL.append(oneSigmaL)
            l_oneSigmaR.append(oneSigmaR)
            l_twoSigmaR.append(twoSigmaR)
            l_theory.append(getXsec(mass,mn)*1000)


        min_mass = min(l_mass)
        max_mass = max(l_mass)

        min_limit = min(l_limit)
        max_limit = max(max(l_limit),max(l_theory))

        gr_13TeV_exp = TGraphAsymmErrors(len(l_limit),array('d',l_mass),array('d',l_limit),0,0,0,0)
        gr_13TeV_exp.SetLineColor(kBlack)
        gr_13TeV_exp.SetLineStyle(2)
        gr_13TeV_exp.SetLineWidth(3)

        gr_theory = TGraphAsymmErrors(len(l_limit),array('d',l_mass),array('d',l_theory),0,0,0,0)
        gr_theory.SetLineColor(kRed)
        #gr_theory.SetLineStyle(2)
        gr_theory.SetLineWidth(3)

        gr_band_oneSigma = TGraphAsymmErrors(len(l_limit),array('d',l_mass),array('d',l_limit),0,0,array('d',l_oneSigmaL),array('d',l_oneSigmaR))
        gr_band_oneSigma.SetFillColor(kGreen+1)
        gr_band_oneSigma.SetLineColor(kGreen+1)
        gr_band_oneSigma.SetMarkerColor(kGreen+1)

        gr_band_twoSigma = TGraphAsymmErrors(len(l_limit),array('d',l_mass),array('d',l_limit),0,0,array('d',l_twoSigmaL),array('d',l_twoSigmaR))
        gr_band_twoSigma.SetFillColor(kOrange)
        gr_band_twoSigma.SetLineColor(kOrange)
        gr_band_twoSigma.SetMarkerColor(kOrange)

        lg = TLegend(0.6, 0.55, 0.95, 0.875)
        lg.SetBorderSize(0)
        lg.SetFillStyle(0)
        hist_empty = TH1D("","",1,0.,1.)
        hist_empty.SetLineColor(0)

        lg.AddEntry(gr_theory,"Theory","l")
        lg.AddEntry(gr_13TeV_exp,"Expected","l")
        lg.AddEntry(gr_band_oneSigma,"68% Expected","f")
        lg.AddEntry(gr_band_twoSigma,"95% Expected","f")
        
        lg.AddEntry(hist_empty,"","l")
        
        c.cd()
        c.Draw()
        c.SetLogy()
        dummy = TH1D("d","d",int(round(max_mass-min_mass))+200,min_mass-100,max_mass+100)
        dummy.GetXaxis().SetTitle("m_{WR} [GeV]")
        dummy.GetYaxis().SetRangeUser(min_limit*0.01,max_limit*300)
        dummy.GetYaxis().SetTitle("#sigma(pp #rightarrow W_{R})#times BR(W_{R} #rightarrow N_{#tau}#tau) [fb]")
        dummy.SetTitle("")
        dummy.SetStats(0)
        dummy.Draw("hist")

        gr_band_twoSigma.Draw("3same")
        gr_band_oneSigma.Draw("3same")
        gr_13TeV_exp.Draw("lpsame")
        gr_theory.Draw("lsame")
        lg.Draw()

        latex = TLatex()
        latex.SetNDC()

        textSize = 0.625*gStyle.GetPadTopMargin()
        latex.SetTextFont(61)
        latex.SetTextSize(textSize*1.5)
        latex.DrawLatex(0.175, 0.785,"CMS")

        latex.SetTextFont(52)
        latex.SetTextSize(0.7*textSize)
        latex.DrawLatex(0.175, 0.74,"Work In Progress")

        latex.SetTextFont(42)
        latex.SetTextSize(0.6*textSize)
        latex.DrawLatex(0.175, 0.675,"m_{N} = "+str(mn/1000.)+" TeV")

        latex.SetTextFont(42)
        latex.SetTextSize(0.6*textSize)
        latex.DrawLatex(0.575, 0.9175,f"{GetLumi(era)} fb^{{-1}} (13 TeV)")


        c.SaveAs(f"Plots/{WP}/{era}/N{mn}_limit.png")
        c.SaveAs(f"Plots/{WP}/{era}/N{mn}_limit.pdf")