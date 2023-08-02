import os
from ROOT import TH2D,TCanvas

# mWR 1000~5000 (20)
xsec_hist = TH2D("xsec","",21,900,5100,50,100.,5000.) 
xsec_hist.SetStats(0)

with open("xsec.csv") as xsec :
    for line in xsec :
        mWR = float(line.split(",")[0])
        mN = float(line.split(",")[1])
        xsec = float(line.split(",")[2])
        xsec_hist.Fill(mWR,mN,xsec)
    
xsec_hist.SetMinimum(1e-07)
xsec_hist.GetXaxis().SetTitle("m_{W_{R}} [GeV]")
xsec_hist.GetYaxis().SetTitle("m_{N} [GeV]")
xsec_hist.GetZaxis().SetTitle("#sigma(pp#rightarrowW_{R})#timesB(W_{R}#rightarrow#font[12]{ll}qq) [pb]")
xsec_hist.GetZaxis().SetTitleOffset(1.75)
c = TCanvas("c","c",1000,1000)
c.SetLeftMargin(0.15)
c.SetRightMargin(0.19)
xsec_hist.Draw("colz")
c.SetLogz()
c.Draw()
c.SaveAs("xsec.png")

