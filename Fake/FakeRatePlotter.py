from ROOT import *
import array,os


filename = "TauFake_20231222_102503"
savestr = filename.split("_")[1]
f_fake = TFile(f"{filename}.root")

d_geoTag = {"All" : "#eta Inclusive",
            "B"   : "|#eta|<1.479",
            "EC"  : "|#eta|>1.479"}

d_njtag = {"All" : "#AK4 Inclusive",
           "0"   : "#AK4 = 0",
           "1"   : "#AK4 = 1",
           "2"   : "#AK4 = 2",
           "3"   : "#AK4 = 3",
           "4"   : "#AK4#geq 4"
}

os.system(f"mkdir -p Plots/{savestr}")

def drawLatex(region,x1=0.175,y1=0.8,x2=0.575,y2=0.925):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, y1 ,"CMS") # 0.85

    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, y1-0.06,"Work In Progress")
    latex.DrawLatex(x1, y1-0.09,"Simulation")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = 41.5
    latex.DrawLatex(x2, y2-0.01,f"{lumi} fb^{{-1}} (13 TeV, 2017)")

    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    if region == 0    : region_latex = "Boosted Fake CR"
    elif region == 1  : region_latex = "Resolved Fake CR"
    elif region == 2  : region_latex = "Inclusive Fake CR"
    latex.SetTextSize(0.65*textSize)
    latex.DrawLatex(x2+0.3, y1+0.015 , "FR(#tau_{h}) = #scale[0.7]{#frac{VVVLoose && Tight}{VVVLoose}}")
    latex.SetTextSize(0.5*textSize)
    latex.DrawLatex(x2+0.3, y1-0.055,f"{region_latex}")

def drawTagLatex(eta,nj,x=.875,y=.815) :
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextSize(0.425*textSize)
    latex.DrawLatex(x, y-0.095,f"({d_geoTag[eta]} , {d_njtag[nj]})")

def drawLine(histogram):
    line = TLine(histogram.GetXaxis().GetXmin(), 1.0, histogram.GetXaxis().GetXmax(), 0.)
    #line = TLine(0.0, y_value, 2000, y_value)
    print(histogram.GetXaxis().GetXmax())
    line.SetNDC(True)
    line.SetLineStyle(2)  # Set line style to dotted
    line.SetLineWidth(5)
    line.SetLineColor(kBlack)  # Set line color (black in this case)
    line.Draw("same")


c = TCanvas("","",1000,1000)
ptbins = [0,190,300,400,500,600,1000,2000]
#ptbins = [0,190,400,2000]
ptbins = [0,190,220,250,300,350,400,450,600,800,1200,2000]

for eta in d_geoTag :
    for nj in d_njtag :
        for i,r in enumerate(["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]) :
            c = TCanvas("","",1000,1000)
            h_loose_tmp = f_fake.Get(f"WRTauFake/{r}/TauPt_Loose_{eta}_{nj}")
            #print(h_loose_tmp)
            if h_loose_tmp :
                h_loose = h_loose_tmp.Rebin(len(ptbins)-1,f"loose{r}",array.array('d',ptbins))
                h_loose.SetDirectory(0)
            else : continue
            h_tight_tmp = f_fake.Get(f"WRTauFake/{r}/TauPt_Tight_{eta}_{nj}")
            if h_tight_tmp :
                h_tight = h_tight_tmp.Rebin(len(ptbins)-1,f"tight{r}",array.array('d',ptbins))
                h_tight.SetDirectory(0)
            else : continue
            h_fr = h_tight.Clone(f"{r}_FR")
            h_fr.Divide(h_tight,h_loose,1,1,'B')
            h_fr.GetYaxis().SetRangeUser(0,1.5)
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
            drawTagLatex(eta,nj)
            c.Update()
            drawLine(h_fr)
            c.Update()
            c.SaveAs(f"Plots/{savestr}/TauFR_{r}_{eta}_{nj}.png")


        h_loose_1 = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/TauPt_Loose_{eta}_{nj}")
        h_loose_2 = f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/TauPt_Loose_{eta}_{nj}")
        h_tight_1 = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/TauPt_Tight_{eta}_{nj}")
        h_tight_2 = f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/TauPt_Tight_{eta}_{nj}")
        if h_loose_1 and h_loose_2  :
            if h_tight_1 and h_tight_2  :
                h_loose_tmp = h_loose_1+h_loose_2
                h_loose = h_loose_tmp.Rebin(len(ptbins)-1,f"Inclusive_{eta}_{nj}_Loose",array.array('d',ptbins))
                h_tight_tmp = h_tight_1+h_tight_2
                h_tight = h_tight_tmp.Rebin(len(ptbins)-1,f"Inclusive_{eta}_{nj}_Tight",array.array('d',ptbins))
                h_fr = h_tight.Clone(f"Inclusive_FR")
                h_fr.Divide(h_tight,h_loose,1,1,'B')
                h_fr.GetYaxis().SetRangeUser(0,1.5)
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
                drawTagLatex(eta,nj)
                drawLine(h_fr)
                c.Update()
                c.SaveAs(f"Plots/{savestr}/TauFR_Inclusive_{eta}_{nj}.png")
                c.Close()