from ROOT import *
from utils import *
import array, os

stamp = "20240805_150737_TailFatBinning_TT"

f_2016 = TFile(f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/Fake/Files/{stamp}/2016_Fake.root")
f_2017 = TFile(f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/Fake/Files/{stamp}/2017_Fake.root")
f_2018 = TFile(f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/Fake/Files/{stamp}/2018_Fake.root")

os.system(f"mkdir -p Plots/InclusiveEra/{stamp}")
for dm in ["0","1","10","11"] :
    
    c = TCanvas("","",1000,1000)
    l = TLegend(0.6,0.65,0.9,0.7)
    l.SetNColumns(3)
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    c.SetLeftMargin(0.125)
    c.SetRightMargin(0.085)
    c.SetBottomMargin(0.125)

    h_2016 = f_2016.Get(f"TTFakeMeasureRegion_FRSubtract_All_DM{dm}")
    h_2017 = f_2017.Get(f"TTFakeMeasureRegion_FRSubtract_All_DM{dm}")
    h_2018 = f_2018.Get(f"TTFakeMeasureRegion_FRSubtract_All_DM{dm}")

    h_2016.SetLineColor(kRed)
    h_2017.SetLineColor(kGreen+2)
    h_2018.SetLineColor(kBlue)


    h_2016.SetFillColorAlpha(kRed,0.1)
    h_2017.SetFillColorAlpha(kGreen,0.1)
    h_2018.SetFillColorAlpha(kBlue,0.1)

    l.AddEntry(h_2016,"2016","lf")
    l.AddEntry(h_2017,"2017","lf")
    l.AddEntry(h_2018,"2018","lf")

    for h in [h_2016,h_2017,h_2018] :
        h.SetStats(0)
        h.GetXaxis().SetTitle("p_{T}(#tau_{h})")
        h.GetYaxis().SetTitleSize(0.05)
        h.GetYaxis().SetTitle("FF(#tau_{h})")
        h.GetYaxis().SetTitleOffset(0.9)
        if dm == "0" : h.GetYaxis().SetRangeUser(-0.0,1.0)
        elif dm == "1" : h.GetYaxis().SetRangeUser(-0.0,0.7)
        elif dm == "10" : h.GetYaxis().SetRangeUser(-0.0,0.3)
        elif dm == "11" : h.GetYaxis().SetRangeUser(-0.0,0.3)
        h.GetXaxis().SetNdivisions(509)
        h.SetLineWidth(2)
        h.GetXaxis().SetTitleSize(0.05)
    
    c.cd()
    h_2016.Draw("e2")
    h_2017.Draw("e2&same")
    h_2018.Draw("e2&same")

    h_2016.Draw("e0&e1&same")
    h_2017.Draw("e0&e1&same")
    h_2018.Draw("e0&e1&same")
    drawTagLatexDM("All",dm)
    drawLatex("TTFake","Run2","Fake")
    l.Draw()
    c.Update()
    c.SaveAs(f"Plots/InclusiveEra/{stamp}/{dm}_TT.png")