from ROOT import *
from . import variables
import array,os

def drawLatex_Fitter(region,era,genmatch,x1=0.175,y1=0.8,x2=0.575,y2=0.925):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, y1 ,"CMS") # 0.85

    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, y1-0.05,"Work In Progress")
    latex.DrawLatex(x1, y1-0.08,"Preliminary")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = getLumi(era)
    latex.DrawLatex(x2, y2-0.01,f"{lumi} fb^{{-1}} (13 TeV, {era})")

    latex.SetTextFont(42)
    if   region == "BoostedSignalRegionMETInvert"   : region_latex = "Boosted Fake CR"
    elif region == "ResolvedSignalRegionMETInvert"  : region_latex = "Resolved Fake CR"
    elif region == "Inclusive"                      : region_latex = "Inclusive Fake CR"
    latex.SetTextSize(0.5*textSize)
    latex.DrawLatex(x1, y1-0.125,f"{region_latex}")
    latex.SetTextSize(0.425*textSize)
    latex.DrawLatex(x1, y1-0.15,"(#eta Inclusive , #AK4 Inclusive)")


def drawTagLatex(eta,nj,x=.875,y=.815) :
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextSize(0.425*textSize)
    latex.DrawLatex(x, y-0.095,f"({variables.d_geoTag[eta]} , {variables.d_njtag[nj]})")


def drawLatex(region,era,genmatch,x1=0.175,y1=0.8,x2=0.575,y2=0.925):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, y1 ,"CMS") # 0.85

    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, y1-0.06,"Work In Progress")
    if genmatch != "Data" : latex.DrawLatex(x1, y1-0.09,"Simulation")
    else                  : latex.DrawLatex(x1, y1-0.09,"Preliminary")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = getLumi(era)
    latex.DrawLatex(x2, y2-0.01,f"{lumi} fb^{{-1}} (13 TeV, {era})")

    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    if   region == 0    : region_latex = "Boosted Fake CR"
    elif region == 1    : region_latex = "Resolved Fake CR"
    elif region == 2    : region_latex = "Inclusive Fake CR"
    latex.SetTextSize(0.65*textSize)
    
    genstring = ""; genstring2 = ""
    if   genmatch == "Fake"   : genstring = "#scale[0.85]{FR(#tau_{h})}" ; genstring2 = "Nonprompt Gen"
    elif genmatch == "Prompt" : genstring = "#scale[0.85]{PR(#tau_{h})}" ; genstring2 = "Prompt Gen"
    elif genmatch == "Data"   : genstring = "#scale[0.85]{FR(#tau_{h})}" 
    if genmatch == "Fake" or genmatch == "Prompt" : 
        latex.DrawLatex(x2+0.3, y1+0.015 , genstring+" = #scale[0.55]{#frac{ "+genstring2+" && (VVVLoose && Tight)}{ "+genstring2+" && VVVLoose}}")
    else : 
        latex.DrawLatex(x2+0.3, y1+0.015 , genstring+" = #scale[0.55]{#frac{ N_{Data}^{VVVLoose && Tight} - N_{Prompt MC}^{VVVLoose && Tight} }{  N_{Data}^{VVVLoose} - N_{Prompt MC}^{VVVLoose} }}")
    latex.SetTextSize(0.5*textSize)
    latex.DrawLatex(x2+0.3, y1-0.055,f"{region_latex}")


def getLumi(era) :
    era = str(era)
    if era == "2016preVFP" or era ==  "2016a" : return "19.5"
    elif era == "2016postVFP" or era ==  "2016b" : return "16.8"
    elif era == "2017" : return "41.5"
    elif era == "2018" : return "60"
    else : return "error"

def drawLine(histogram):
    line = TLine(histogram.GetXaxis().GetXmin(), 1.0, histogram.GetXaxis().GetXmax(), 0.)
    #line = TLine(0.0, y_value, 2000, y_value)
    print(histogram.GetXaxis().GetXmax())
    line.SetNDC(True)
    line.SetLineStyle(2)  # Set line style to dotted
    line.SetLineWidth(5)
    line.SetLineColor(kBlack)  # Set line color (black in this case)
    line.Draw("same")
