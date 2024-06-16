from ROOT import *
from utils import *
import array,os

stamp = "20240520_103147"
filename = f"TauFake_{stamp}"
savestr = filename.split("_",1)[1]
#f_fake = TFile(f"Inputs/{stamp}/{filename}.root")

c = TCanvas("","",1000,1000)



d_ptbins  = {

    "tag"                                      : "BinOptv2_FlavourSplit",
    "Inclusive_2016"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_2016"        : [0,190,210,230,270,310,335,400,450,550,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvert_2016"       : [0,190,230,270,320,360,400,480,525,1000],
    "Inclusive_2017"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_2017"        : [0,190,210,230,270,300,330,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_2017"       : [0,190,210,230,270,300,320,350,380,450,1000],#[0,190,230,270,320,360,400,480,1000],
    "Inclusive_2018"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_2018"        : [0,190,210,230,270,310,335,400,450,550,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvert_2018"       : [0,190,230,270,320,360,400,480,525,1000],
    "Inclusive_ElTau_2016"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_ElTau_2016"  : [0,190,200,210,220,240,280,320,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_ElTau_2016" : [0,190,210,230,250,270,300,350,400,500,1000],
    "Inclusive_ElTau_2017"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_ElTau_2017"  : [0,190,200,210,220,240,280,320,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_ElTau_2017" : [0,190,210,230,250,270,300,350,400,1000],
    "Inclusive_ElTau_2018"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_ElTau_2018"  : [0,190,210,230,270,310,350,400,500,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvert_ElTau_2018" : [0,190,210,230,250,270,290,310,330,350,375,400,1000],
    "Inclusive_MuTau_2016"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_MuTau_2016"  : [0,190,200,210,220,230,240,310,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_MuTau_2016" : [0,190,210,230,250,270,290,310,350,400,550,1000],
    "Inclusive_MuTau_2017"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_MuTau_2017"  : [0,190,200,210,220,230,240,310,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_MuTau_2017" : [0,190,210,230,250,270,290,310,330,350,400,450,550,1000],#[0,190,230,270,320,360,400,480,1000],
    "Inclusive_MuTau_2018"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_MuTau_2018"  : [0,190,200,210,220,230,250,270,290,310,330,350,375,400,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvert_MuTau_2018" : [0,190,210,230,250,270,290,310,330,350,370,390,410,450,550,1000]#[0,190,230,270,320,360,400,480,525,1000]
    # [0,190,210,230,250,270,300,320,340,360,400,480,525,1500]

}


# [0,190,210,230,250,270,320,800] 
d_ptbins_PR = {

    "tag"                                      : "BinOptv2_FlavourSplit",
    "Inclusive_2016"                           : [0,190,220,250,350,1000],
    "Inclusive_2017"                           : [0,190,220,250,350,1000],
    "Inclusive_2018"                           : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2018"                     : [0,190,220,250,350,1000], 
    "Inclusive_MuTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2018"                     : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvert_2016"        : [0,190,220,250,350,1000], 
    "ResolvedSignalRegionMETInvert_2016"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvert_2017"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_2017"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvert_2018"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_2018"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvert_ElTau_2016"  : [0,190,220,270,1000],
    "ResolvedSignalRegionMETInvert_ElTau_2016" : [0,190,210,250,1000],
    "BoostedSignalRegionMETInvert_ElTau_2017"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_ElTau_2017" : [0,190,210,250,350,1000],
    "BoostedSignalRegionMETInvert_ElTau_2018"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_ElTau_2018" : [0,190,210,270,300,1000],
    "BoostedSignalRegionMETInvert_MuTau_2016"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_MuTau_2016" : [0,190,220,300,1000],
    "BoostedSignalRegionMETInvert_MuTau_2017"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_MuTau_2017" : [0,190,220,300,1000],
    "BoostedSignalRegionMETInvert_MuTau_2018"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvert_MuTau_2018" : [0,190,220,250,350,1000],
    # [0,190,210,230,250,270,300,320,340,360,400,480,525,1500]

}


d_ptbins = {

    "tag"                                : "TailFatBinning",
    "Inclusive_2016"                     : [0] + list(range(190, 400, 50)) + list(range(500, 1500, 100)),
    "BoostedSignalRegionMETInvert_2016"  : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "ResolvedSignalRegionMETInvert_2016" : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "Inclusive_2017"                     : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "BoostedSignalRegionMETInvert_2017"  : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "ResolvedSignalRegionMETInvert_2017" : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "Inclusive_2018"                     : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "BoostedSignalRegionMETInvert_2018"  : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50)),
    "ResolvedSignalRegionMETInvert_2018" : [0] + list(range(190, 400, 10)) + list(range(400, 1500, 50))


}


savestr += f"_{d_ptbins['tag']}"

l_subtract = ["Subtract"]


l_subtract = ["NonSubtract"]
l_subtract = ["Subtract"]

for era in ["2016","2017","2018"]:
    k = 0
    os.system(f"mkdir -p Plots/{savestr}/{era}")
    os.system(f"mkdir -p Files/{savestr}")
    for genmatch in ["Fake"]:
    #for genmatch in ["Prompt"]: # Switch for prompt rate 
        output_file = TFile(f"Files/{savestr}/{era}_{genmatch}.root", "RECREATE")
        isDataDriven = genmatch == "Data"
        isPromptRate = genmatch == "Prompt"
        f_fake = TFile(f"Inputs/{stamp}/{era}/{filename}.root")
        if isDataDriven : 
            f_fake   = TFile(f"Inputs/{stamp}/{era}/Data/{filename}.root")
            f_prompt = TFile(f"Inputs/{stamp}/{era}/{filename}.root")
        for eta in d_geoTag :
            for nj in d_njtag :
                c = TCanvas("","",1000,1000)
                
                rebin = [0,190,220,250,300,400,500,600,750,900,1200,1500]

                h_tight1 = f_fake.Get("WRTauFake/BoostedSignalRegionMETInvert/Fake/TauPt_Tight_All_All") 
                h_tight2 = f_fake.Get("WRTauFake/ResolvedSignalRegionMETInvert/Fake/TauPt_Tight_All_All")
                h_tight3 = f_fake.Get("WRTauFake/BoostedSignalRegionMETInvert/Prompt/TauPt_Tight_All_All") 
                h_tight4 = f_fake.Get("WRTauFake/ResolvedSignalRegionMETInvert/Prompt/TauPt_Tight_All_All")

                h_loose1 = f_fake.Get("WRTauFake/BoostedSignalRegionMETInvert/Fake/TauPt_Loose_All_All")
                h_loose2 = f_fake.Get("WRTauFake/ResolvedSignalRegionMETInvert/Fake/TauPt_Loose_All_All")
                h_loose3 = f_fake.Get("WRTauFake/BoostedSignalRegionMETInvert/Prompt/TauPt_Loose_All_All")
                h_loose4 = f_fake.Get("WRTauFake/ResolvedSignalRegionMETInvert/Prompt/TauPt_Loose_All_All")

                h_tight_ = h_tight1 + h_tight2 + h_tight3 + h_tight4
                h_loose_ = h_loose1 + h_loose2 + h_loose3 + h_loose4
                h_tight = h_tight_.Rebin(len(rebin)-1,"tightRebin",array.array('d',rebin))
                h_loose = h_loose_.Rebin(len(rebin)-1,"looseRebin",array.array('d',rebin))

                h_fr = h_tight.Clone(f"FakeRate")
                h_fr.Divide(h_tight,h_loose,1,1,'B')
                original_directory = gDirectory.GetPath()
                output_file.cd()
                h_fr.Write()
                gDirectory.cd(original_directory)
                if isPromptRate : h_fr.GetYaxis().SetRangeUser(0,1.5) 
                else : h_fr.GetYaxis().SetRangeUser(0,1.5) 
                h_fr.SetStats(0)
                h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
                h_fr.GetYaxis().SetTitleSize(0.05)
                h_fr.GetYaxis().SetTitle(d_genmatch[genmatch]+"(#tau_{h})")
                if isDataDriven : h_fr.GetYaxis().SetTitle("FR(#tau_{h})")
                h_fr.GetYaxis().SetTitleOffset(0.9)
                h_fr.GetXaxis().SetNdivisions(509)
                h_fr.SetLineColor(kRed)
                h_fr.SetLineWidth(3)
                h_fr.GetXaxis().SetTitleSize(0.05)
                h_err = h_fr.Clone(f"_FR_err")
                h_err.SetLineWidth(2)
                h_err.SetLineColor(kBlack)

                c.cd()
                c.SetLeftMargin(0.125)
                c.SetRightMargin(0.085)
                c.SetBottomMargin(0.125)
                #h_fr.Draw("hist")
                h_err.Draw("e0")
                h_fr.Draw("hist&same")
                drawLatex("Inclusive",era,genmatch)
                drawTagLatex(eta,nj)
                c.Update()
                drawLine(h_fr)
                c.Update()
                c.SaveAs(f"Plots/{savestr}/{era}/TauFR.png")
                c.SaveAs(f"Plots/{savestr}/{era}/TauFR.pdf")

    output_file.Close()