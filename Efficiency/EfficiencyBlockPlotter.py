from ROOT import * 
from array import array
import numpy as np


xbins = [2000-1,2400-1,2800-1,3200-1,3600-1,4000-1,4400-1,4800-1]
ybins = [0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.7,0.8,0.9,0.95,0.975,1.0]

h_eff = TH2D("", "", len(xbins)-1, array('d', xbins), len(ybins)-1, array('d', ybins))

def rebin_TH2D_for_fixed_x(hist2d, fixed_x_bin):
    num_y_bins = hist2d.GetNbinsY()
    y_bin_edges = [hist2d.GetYaxis().GetBinLowEdge(i + 1) for i in range(num_y_bins)]
    y_bin_edges.append(hist2d.GetYaxis().GetBinUpEdge(num_y_bins))

    proj_y = ROOT.TH1D("projY", "Projection along Y-axis", num_y_bins, array('d', y_bin_edges))

    for i in range(1, num_y_bins + 1):
        proj_y.SetBinContent(i, hist2d.GetBinContent(fixed_x_bin, i))

    return proj_y



with open("SREff.txt",'r') as eff :
    for line in eff :
        mWR = float(line.split(",")[0])
        mN = float(line.split(",")[1])
        eff = float(line.split(",")[4])
        ratio = mN/mWR
        print(mWR,ratio,eff)
        h_eff.Fill(mWR,ratio,eff)

for i in range(1, h_eff.GetNbinsX() + 1):
    for j in range(1, h_eff.GetNbinsY() + 1):
        bin_content = h_eff.GetBinContent(i, j)
        print(i,j,bin_content)

conts = [0.0,4.5,10.0,25.0,100.]


c = TCanvas("","",1000,1000)
h_eff.SetStats(0)
c.cd()
#c.SetRightMargin(0.1)
#h_eff.Smooth(2,"k5a")
h_eff.Draw("colz")
h_eff.Draw("text&same")
h_eff.GetXaxis().SetTitle("m(W_{R}) [GeV]")
h_eff.GetYaxis().SetTitle("m(N)/m(W_{R})")
#h_eff.GetZaxis().SetTitle("SR Efficiency (%)")
#h_eff.Smooth()
#h_eff.SetContour(5,array('d',conts))
#h_eff.Draw("cont3&same")

c.SaveAs("2d_nosmooth.png")
c.Close()