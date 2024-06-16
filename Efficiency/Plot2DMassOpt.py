from ROOT import *
from array import array
gStyle.SetPalette(kBlackBody)
l_cut = range(300,2050,50)

d_mass = {
    2000 : [200-0.1,400-0.1,600-0.1,1000-0.1,1400-0.1,1800-0.1]
}

h_b_el = TH2D("b_el","b_el",len(l_cut)-1,array('d',l_cut),len(d_mass[2000])-1,array('d',d_mass[2000]))
h_b_mu = h_b_el.Clone("b_mu")
h_r_el = h_b_el.Clone("r_el")
h_r_mu = h_b_el.Clone("r_mu")

d_h2d = {

    "Boosted_ElTau" : h_b_el, "Boosted_MuTau" : h_b_mu,
    "Resolved_ElTau" : h_r_el,"Resolved_MuTau" : h_r_mu,

}

d_l = {

    "Boosted_ElTau" : [], "Boosted_MuTau" : [],
    "Resolved_ElTau" : [],"Resolved_MuTau" : [],

}



def drawLatex(region,lep,mwr,x1=0.125,x2=0.575):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    #latex.SetTextColor(kWhite)
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, 0.85,"CMS")
    
    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, 0.81,"Work In Progress")
    latex.DrawLatex(x1, 0.775,"Simulation")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = 41.5
    latex.DrawLatex(x2, 0.97,f"{lumi} fb^{{-1}} (13 TeV, 2017)")

    latex.SetTextFont(42)
    latex.SetTextSize(0.525*textSize)

    if lep == 0 : lep_latex = "e#tau_{h} SR"
    elif lep == 1 : lep_latex = "#mu#tau_{h} SR"

    if region == 0 : region_latex = "Boosted "+lep_latex
    elif region == 1  : region_latex = "Resolved "+lep_latex
    latex.DrawLatex(x1, 0.715,f"{region_latex}")
    latex.DrawLatex(x1, 0.675,f"(m_{{W_{{R}}}}={mwr} GeV)")

with open('WR2000_STwithMET.log', 'r') as file:
    for line in file :
        region = f"{line.split(',')[1]}_{line.split(',')[2]}"
        cut = float(line.split(',')[3])
        mN  = float(line.split(',')[5])
        fom = float(line.strip().split(',')[-1])

        bin_cut  = d_h2d[region].GetXaxis().FindBin(cut)
        bin_mN   = d_h2d[region].GetYaxis().FindBin(mN)
        d_h2d[region].SetBinContent(bin_cut,bin_mN,fom)
        d_l[region].append(fom)

for region in d_h2d :
    d_h2d[region].SetStats(0)
    d_h2d[region].SetTitle("")
    d_h2d[region].GetZaxis().SetTitle("#sqrt{2[(s+b)ln(1+#frac{s}{b})-s]}")
    d_h2d[region].GetZaxis().SetTitleOffset(1.5)
    d_h2d[region].GetYaxis().SetTitle("m_{N} [GeV]")
    d_h2d[region].GetYaxis().SetTitleSize(0.05)
    d_h2d[region].GetZaxis().SetTitleSize(0.035)
    d_h2d[region].GetZaxis().SetRangeUser(-1e-20,max(d_l[region]))
    if "El" in region : l = "e"
    elif "Mu" in region : l = "#mu"
    d_h2d[region].GetXaxis().SetTitle("S_{T} Cut [GeV]")
    #if "Boosted" in region : 
    #    d_h2d[region].GetXaxis().SetTitle("m(#tau_{h}J) Cut [GeV]")
    #elif "Resolved" in region :
    #    d_h2d[region].GetXaxis().SetTitle(f"m(#tau_{{h}}{l}jj) Cut [GeV]")
    d_h2d[region].SetTitleSize(0.0475)


x1 = 0.185 ; x2 = 0.525 ; mWR = 2000
c = TCanvas("","",2000,2000)
c.Divide(2, 2)

for i in range(1, 5):
    # Select the pad
    pad = c.cd(i)

    pad.SetLeftMargin(0.15)
    pad.SetRightMargin(0.165)
    pad.SetBottomMargin(0.15)
    pad.SetTopMargin(0.05)

line = TLine(800,200-0.1,800,1800-0.1)
line.SetLineStyle(7)
line.SetLineWidth(2)

c.cd(1)
h_b_el.Draw("colz")
drawLatex(0,0,mWR,x1,x2)
#line.Draw("same")
c.cd(2)
h_b_mu.Draw("colz")
drawLatex(0,1,mWR,x1,x2)
#line.Draw("same")
c.cd(3)
h_r_el.Draw("colz")
drawLatex(1,0,mWR,x1,x2)
#line.Draw("same")
c.cd(4)
h_r_mu.Draw("colz")
drawLatex(1,1,mWR,x1,x2)
#line.Draw("same")
c.SaveAs("WR2000_MassOpt_STwithMET.png")