from ROOT import *
import array


filename = "TauFake_20231221_143606"
savestr = filename.split("_")[1]
f_fake = TFile(f"{filename}.root")

d_geoTag = {"All" : "#eta Inclusive",
            "B"   : "#eta Inclusive",
            "EC"  : "#eta Inclusive"}

def drawLatex(region,x1=0.175,y1=0.8,x2=0.575,y2=0.925):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, y1 ,"CMS") # 0.85

    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, y1-0.04,"Work In Progress")
    latex.DrawLatex(x1, y1-0.075,"Simulation")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = 41.5
    latex.DrawLatex(x2, y2-0.01,f"{lumi} fb^{{-1}} (13 TeV, 2017)")

    latex.SetTextFont(42)
    latex.SetTextSize(0.5*textSize)
    if region == 0    : region_latex = "Boosted #mu#tau_{h} Fake CR"
    elif region == 1  : region_latex = "Resolved #mu#tau_{h} Fake CR"
    elif region == 2  : region_latex = "Inclusive #mu#tau_{h} Fake CR"
    latex.DrawLatex(x2+0.045, y1-0.055,f"{region_latex}")
    latex.SetTextSize(0.45*textSize)
    latex.DrawLatex(x2+0.145, y1-0.095,"(#slash{E}_{T} < 100 GeV)")
    latex.SetTextSize(0.65*textSize)
    latex.DrawLatex(x2-0.075, y1+0.015 , "FR(#tau_{h}) = #scale[0.7]{#frac{VVVLoose && Tight}{VVVLoose}}")


c = TCanvas("","",1000,1000)
ptbins = [0,190,300,400,500,600,1000,2000]
#ptbins = [0,190,400,2000]
ptbins = [0,190,250,350,450,600,2000]

for i,r in enumerate(["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]) :
    c = TCanvas("","",1000,1000)
    h_loose = f_fake.Get(f"WRTauFake/{r}/TauPt_Loose_All_All").Rebin(len(ptbins)-1,f"loose{r}",array.array('d',ptbins))
    h_tight = f_fake.Get(f"WRTauFake/{r}/TauPt_Tight_All_All").Rebin(len(ptbins)-1,f"tight{r}",array.array('d',ptbins))
    h_fr = h_tight.Clone(f"{r}_FR")
    h_fr.Divide(h_loose)
    h_fr.GetYaxis().SetRangeUser(0,1.75)
    h_fr.SetStats(0)
    h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
    h_fr.GetYaxis().SetTitleSize(0.05)
    h_fr.GetYaxis().SetTitle("FR(#tau_{h})")
    h_fr.GetYaxis().SetTitleOffset(0.9)
    h_fr.GetXaxis().SetNdivisions(509)
    h_fr.SetLineColor(kRed)
    h_fr.SetLineWidth(3)
    h_fr.GetXaxis().SetTitleSize(0.05)
    h_err = h_fr.Clone(f"{r}_FR_err")
    h_err.SetLineWidth(2)
    h_err.SetLineColor(kBlack)


    c.cd()
    c.SetLeftMargin(0.125)
    c.SetRightMargin(0.085)
    c.SetBottomMargin(0.125)
    #h_fr.Draw("hist")
    h_err.Draw("e0")
    h_fr.Draw("hist&same")
    drawLatex(i)
    c.SaveAs(f"TauFE_{savestr}_{r}.png")

h_loose = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/TauPt_Loose_All_All").Rebin(len(ptbins)-1,f"loose{r}",array.array('d',ptbins))+f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/TauPt_Loose_All_All").Rebin(len(ptbins)-1,f"loose{r}",array.array('d',ptbins))
h_tight = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/TauPt_Tight_All_All").Rebin(len(ptbins)-1,f"tight{r}",array.array('d',ptbins))+f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/TauPt_Tight_All_All").Rebin(len(ptbins)-1,f"tight{r}",array.array('d',ptbins))
h_fr = h_tight.Clone(f"Inclusive_FR")
h_fr.Divide(h_loose)
h_fr.GetYaxis().SetRangeUser(0,1.75)
h_fr.SetStats(0)
h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
h_fr.GetYaxis().SetTitleSize(0.05)
h_fr.GetYaxis().SetTitle("FR(#tau_{h})")
h_fr.GetYaxis().SetTitleOffset(0.9)
h_fr.GetXaxis().SetNdivisions(509)
h_fr.SetLineColor(kRed)
h_fr.SetLineWidth(3)
h_fr.GetXaxis().SetTitleSize(0.05)
h_err = h_fr.Clone(f"{r}_FR_err")
h_err.SetLineWidth(2)
h_err.SetLineColor(kBlack)


c.cd()
c.SetLeftMargin(0.125)
c.SetRightMargin(0.085)
c.SetBottomMargin(0.125)
#h_fr.Draw("hist")
h_err.Draw("e0")
h_fr.Draw("hist&same")
drawLatex(2)
c.SaveAs(f"TauFR_{savestr}_Inclusive.png")