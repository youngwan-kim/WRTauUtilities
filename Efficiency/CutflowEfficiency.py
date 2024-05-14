import ROOT
import array,os

savedir = "../Plots/SignalEfficiency/"
os.system(f"mkdir -p {savedir}")

d = {}
# mWR : [mN array , eff1e , eff1mu , eff2e, eff2mu]
with open('EffCutflow_Resolved.txt') as f :
    for line in f :
        mWR = int(line.split(",")[0])
        mN = float(line.split(",")[1])/1000
        effTrigger = float(line.split(",")[2])
        effTauID = float(line.split(",")[3])
        effSafePt = float(line.split(",")[4])
        effLep = float(line.split(",")[5])
        effPre = float(line.split(",")[6])
        effSig = float(line.split(",")[7].rstrip())

        if mWR not in d : 
            mnarr       =  array.array('d');  mnarr.append(mN)
            effTrigger_arr   =  array.array('d');  effTrigger_arr.append(effTrigger)
            effTauID_arr  =  array.array('d');  effTauID_arr.append(effTauID)
            effSafePt_arr   =  array.array('d');  effSafePt_arr.append(effSafePt)
            effLep_arr   =  array.array('d');  effLep_arr.append(effLep)
            effPre_arr   =  array.array('d');  effPre_arr.append(effPre)
            effSig_arr   =  array.array('d');  effSig_arr.append(effSig)

            d[mWR] = [mnarr,effTrigger_arr,effTauID_arr,effSafePt_arr,effLep_arr,effPre_arr,effSig_arr]
        
        else :
            d[mWR][0].append(mN)
            d[mWR][1].append(effTrigger)
            d[mWR][2].append(effTauID)
            d[mWR][3].append(effSafePt)
            d[mWR][4].append(effLep)
            d[mWR][5].append(effPre)
            d[mWR][6].append(effSig)

    for mWR in d :

        c = ROOT.TCanvas(f"{mWR}_Eff","",1000,1000)
        l = ROOT.TLegend(0.45,0.715,0.85,0.875)
        l.SetFillStyle(0)
        l.SetNColumns(2)
        l.SetBorderSize(0)

        mineff = min(effSig_arr)

        h = ROOT.TH1D("","",1,0.,mWR)
        h.SetBinContent(0,1)
        h.SetLineStyle(2)
        h.SetLineColor(ROOT.kBlack)
        h.SetLineWidth(1)
        h.SetStats(0)

        graph_effTrigger  = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][1]) 
        graph_effTauID    = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][2]) 
        graph_effSafePt   = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][3]) 
        graph_effLep      = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][4]) 
        graph_effPre      = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][5]) 
        graph_effSig      = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][6]) 

        d_graphs = { graph_effTrigger : [ROOT.kRed,"Trigger"],
                     graph_effTauID   : [ROOT.kOrange+7,"n_{#tau_{h}}^{Tight} > 0"],
                     graph_effSafePt  : [ROOT.kOrange,"p_{T}^{#tau_{h}} > 190 GeV"],
                     graph_effLep     : [ROOT.kGreen+1,"Lepton ID"], 
                     graph_effPre     : [ROOT.kBlue,"Preselection"],
                     graph_effSig     : [ROOT.kViolet,"Signal"]}

        mg = ROOT.TMultiGraph()

        for g in d_graphs :
            g.SetLineColor(d_graphs[g][0])
            g.SetMarkerStyle(20)
            g.SetMarkerSize(1.5)
            g.SetMarkerColor(d_graphs[g][0])
            g.SetTitle(d_graphs[g][1])
            l.AddEntry(g,d_graphs[g][1])
            g.SetLineWidth(5)
            mg.Add(g,"lp")
        
        mg.GetYaxis().SetTitle("Acceptance #times Efficiency")
        mg.GetYaxis().SetTitleSize(0.05)
        mg.GetYaxis().SetRangeUser(mineff*0.5,30)
        mg.GetXaxis().SetTitle("m_{N} [TeV]")
        mg.GetXaxis().SetTitleSize(0.04)

        latex = ROOT.TLatex()
        latex.SetNDC()
        c.SetLeftMargin(0.15)
        c.SetLogy()
        c.cd()  
        h.Draw()
        mg.Draw("a")
        
        c.cd()
        textSize = 0.675*ROOT.gStyle.GetPadTopMargin()
        latex.SetTextFont(61)
        latex.SetTextSize(textSize)
        latex.DrawLatex(0.2, 0.815,"CMS")
        latex.SetTextFont(52)
        latex.SetTextSize(0.65*textSize)
        latex.DrawLatex(0.2, 0.775,"Simulation")
        latex.SetTextFont(42)
        latex.SetTextSize(0.45*textSize)
        latex.DrawLatex(0.2, 0.725,f"m(W_{{R}}) = {mWR/1000.} TeV")
        l.Draw()

        c.SaveAs(f"{savedir}/mWR{mWR}_CutEff.pdf")
        c.SaveAs(f"{savedir}/mWR{mWR}_CutEff.png")

        #print(d[mWR])