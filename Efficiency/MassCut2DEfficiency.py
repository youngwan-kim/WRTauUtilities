import os,array,math
import ROOT
from itertools import product

l_mWR = [2000,2400,2800,3200,3600,4000,4400,4800]
l_RecoCut = [500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
l_EffCut = [500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
l_TransCut = [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700]
l_lep = ['NonPromptLepton','PromptLepton']
l_tau = ['NonPromptTau','PromptTau']

combinations = product(l_tau, l_lep)
nonprompts = [f"__{A}__{B}" for A, B in combinations]

strpath = "WRTau_SignalSingleTauTrg/vJetTight_vElTight_vMuTight"

#def FoM(sig, bkg):
#    if bkg == 0 : return float('inf')
#    else : return math.sqrt( 2.*((sig+bkg)*math.log(1+(sig/bkg)) - sig))

def FoM(sig, bkg): 
    return math.sqrt( 2.*((sig+bkg)*math.log(1+(sig/max(bkg,1e-20))) - sig))


d_save = f"{os.environ['WRTau_Output']}/20231218_231113__MassOpt/"
d_signal = f"{d_save}/Signal"
for mWR in l_mWR :
    
    c = ROOT.TCanvas(f"{mWR}","",6000,4000)
    c.Divide(3, 2)
    pad00 = c.cd(1) ; pad01 = c.cd(2) ; pad02 = c.cd(3)
    pad10 = c.cd(4) ; pad11 = c.cd(5) ; pad12 = c.cd(6)

    l_mN = [int(file.split("_")[4].split(".")[0].split("N")[1]) for file in os.listdir(d_signal) if file.endswith(".root") and f"WR{mWR}" in file]
    l_mN.sort()
    l_mN = l_mN[:-1] 
    print(l_mN)
    h2d_BstEff   = ROOT.TH2D(f"{mWR}BstEff"   , "" , len(l_EffCut)   , l_EffCut[0]   , l_EffCut[len(l_EffCut)-1]    , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    h2d_ResEff   = ROOT.TH2D(f"{mWR}ResEff"   , "" , len(l_EffCut)   , l_EffCut[0]   , l_EffCut[len(l_EffCut)-1]    , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    h2d_BstTrans = ROOT.TH2D(f"{mWR}BstTrans" , "" , len(l_TransCut) , l_TransCut[0] , l_TransCut[len(l_TransCut)-1]  , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    h2d_ResTrans = ROOT.TH2D(f"{mWR}ResTrans" , "" , len(l_TransCut) , l_TransCut[0] , l_TransCut[len(l_TransCut)-1]  , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    h2d_BstReco  = ROOT.TH2D(f"{mWR}BstReco"  , "" , len(l_RecoCut)  , l_RecoCut[0] , l_RecoCut[len(l_RecoCut)-1]  , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    h2d_ResReco  = ROOT.TH2D(f"{mWR}ResReco"  , "" , len(l_RecoCut)  , l_RecoCut[0] , l_RecoCut[len(l_RecoCut)-1]  , len(l_mN), l_mN[0], l_mN[len(l_mN)-1])
    

    for h in [h2d_BstEff,h2d_BstTrans,h2d_ResEff,h2d_ResTrans,h2d_BstReco,h2d_ResReco] :
        h.SetDirectory(0)
        h.SetStats(0)
    
    h2d_BstEff.SetDirectory(0)
    h2d_ResEff.SetDirectory(0)
    h2d_BstTrans.SetDirectory(0)
    h2d_ResTrans.SetDirectory(0)
    
    f_bkg = ROOT.TFile(f"{d_save}/WRTau_Analyzer_Bkg.root")
    
    for region in ["BoostedMassOptSel","ResolvedMassOptSel"] :
        for j,mN in enumerate(l_mN) : 
            f_sig = ROOT.TFile(f"{d_signal}/WRTau_Analyzer_WRtoTauNtoTauTauJets_WR{mWR}_N{mN}.root")
            for i,EffCut in enumerate(l_EffCut) :
                h_sig = f_sig.Get(f"{strpath}/{region}_EffMass{EffCut}p00_MuTau/Nevents")
                if h_sig == None : s = 0
                else : s = h_sig.Integral()
                b = 0
                for np in nonprompts :
                    h_bkg = f_bkg.Get(f"WRTau_SignalSingleTauTrg{np}/vJetTight_vElTight_vMuTight/{region}_EffMass{EffCut}p00_MuTau/Nevents")
                    #print(h_bkg)
                    if h_bkg == None : continue
                    else : b += h_bkg.Integral()
                #print(f"{s},{b}")
                if region == "BoostedMassOptSel" : 
                    h2d_BstEff.SetBinContent(i + 1, j + 1, FoM(s,b))
                elif region == "ResolvedMassOptSel" : h2d_ResEff.SetBinContent(i + 1, j + 1, FoM(s,b))

            for i,TransCut in enumerate(l_TransCut) :
                h_sig = f_sig.Get(f"{strpath}/{region}_TransMass{TransCut}p00_MuTau/Nevents")
                if h_sig == None : s = 0
                else : s = h_sig.Integral()
                b = 0 
                for np in nonprompts :
                    h_bkg = f_bkg.Get(f"WRTau_SignalSingleTauTrg{np}/vJetTight_vElTight_vMuTight/{region}_TransMass{TransCut}p00_MuTau/Nevents")
                    if h_bkg == None : continue
                    else : b += h_bkg.Integral()
                if region == "BoostedMassOptSel" : h2d_BstTrans.SetBinContent(i + 1, j + 1, FoM(s,b))
                elif region == "ResolvedMassOptSel" : h2d_ResTrans.SetBinContent(i + 1, j + 1, FoM(s,b))

            for i,RecoCut in enumerate(l_RecoCut) :
                h_sig = f_sig.Get(f"{strpath}/{region}_RecoNuMass{RecoCut}p00_MuTau/Nevents")
                if h_sig == None : s = 0
                else : s = h_sig.Integral()
                b = 0 
                for np in nonprompts :
                    h_bkg = f_bkg.Get(f"WRTau_SignalSingleTauTrg{np}/vJetTight_vElTight_vMuTight/{region}_RecoNuMass{RecoCut}p00_MuTau/Nevents")
                    if h_bkg == None : continue
                    else : b += h_bkg.Integral()
                if region == "BoostedMassOptSel" : h2d_BstReco.SetBinContent(i + 1, j + 1, FoM(s,b))
                elif region == "ResolvedMassOptSel" : h2d_ResReco.SetBinContent(i + 1, j + 1, FoM(s,b))


    for p in [pad00,pad01,pad02,pad10,pad11,pad12] :
        p.SetLogz()

    c.cd()
    c.SetLogz()
    pad00.cd()
    h2d_BstEff.Draw("colz")
    pad01.cd()
    h2d_BstTrans.Draw("colz")
    pad02.cd()
    h2d_BstReco.Draw("colz")
    pad10.cd()
    h2d_ResEff.Draw("colz")
    pad11.cd()
    h2d_ResTrans.Draw("colz")
    pad12.cd()
    h2d_ResReco.Draw("colz")
    c.cd()
    pad00.Draw(); pad01.Draw() ; pad02.Draw()
    pad10.Draw(); pad11.Draw() ; pad12.Draw()

    c.SaveAs(f"{os.environ['WRTau_Plots']}/Efficiency/MassCut/WR{mWR}.png")
    c.SaveAs(f"{os.environ['WRTau_Plots']}/Efficiency/MassCut/WR{mWR}.pdf")
    c.Close()
