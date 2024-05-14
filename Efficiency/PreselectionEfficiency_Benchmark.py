import ROOT
import array,os

savedir = "../Plots/SignalEfficiency/"
os.system(f"mkdir -p {savedir}")

d = {}
# mWR : [mN array , eff1e , eff1mu , eff2e, eff2mu]
with open('Benchmark_Mu.txt') as f :
    for line in f :
        mWR = int(line.split(",")[0])
        mN = float(line.split(",")[1])
        eff_Res = float(line.split(",")[2])
        eff_Bst = float(line.split(",")[3])
        eff_Incl = float(line.split(",")[4])
        eff_Bench = float(line.split(",")[5].rstrip())
        ratio = eff_Incl/eff_Bench
        ratio_boosted = eff_Bst/eff_Bench
        ratio_resolved = eff_Res/eff_Bench

        if mWR not in d : 
            mnarr       =  array.array('d');  mnarr.append(mN/1000)
            eff_Res_arr   =  array.array('d');  eff_Res_arr.append(eff_Res)
            eff_Bst_arr  =  array.array('d');  eff_Bst_arr.append(eff_Bst)
            eff_Incl_arr   =  array.array('d');  eff_Incl_arr.append(eff_Incl)
            eff_Bench_arr  =  array.array('d');  eff_Bench_arr.append(eff_Bench)
            ratio_arr      =  array.array('d');  ratio_arr.append(ratio)
            ratio_boosted_arr = array.array('d');  ratio_boosted_arr.append(ratio_boosted)
            ratio_resolved_arr =array.array('d');  ratio_resolved_arr.append(ratio_resolved)

            d[mWR] = [mnarr,eff_Res_arr,eff_Bst_arr,
                      eff_Incl_arr,eff_Bench_arr,ratio_arr,
                      ratio_boosted_arr,ratio_resolved_arr]
        
        else :
            d[mWR][0].append(mN/1000)
            d[mWR][1].append(eff_Res)
            d[mWR][2].append(eff_Bst)
            d[mWR][3].append(eff_Incl)
            d[mWR][4].append(eff_Bench)
            d[mWR][5].append(ratio)
            d[mWR][6].append(ratio_boosted)
            d[mWR][7].append(ratio_resolved)

    for mWR in d :

        c = ROOT.TCanvas(f"{mWR}_PreselBenchmark","",1000,1250)
        pad_up = ROOT.TPad(f"{mWR}u",f"{mWR}u",0,0.35,1,1)
        pad_up.SetBottomMargin(0.03)
        pad_down = ROOT.TPad(f"{mWR}d",f"{mWR}d",0,0,1,0.35)
        pad_down.SetGrid(1)
        pad_down.SetTopMargin(0.0315)
        pad_down.SetBottomMargin(0.3)
        
        l = ROOT.TLegend(0.475,0.585,0.95,0.875)
        l.SetFillStyle(0)
        #l.SetNColumns(2)
        l.SetBorderSize(0)
        

        l2 = ROOT.TLegend(0.35,0.785,0.9,0.97)
        l2.SetNColumns(3)
        #l2.SetFillStyle(0)
        #l2.SetBorderSize(0)

        #c1.GetYaxis().SetRangeUser(0,1)
        #c2.GetYaxis().SetRangeUser(0,1)


        graph_eff1mu          = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][1]) ; graph_eff1mu.SetLineColor(ROOT.kRed) ; graph_eff1mu.SetLineWidth(4)     ; graph_eff1mu.SetMarkerStyle(20) 
        graph_eff2mu          = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][2]) ; graph_eff2mu.SetLineColor(ROOT.kBlue) ; graph_eff2mu.SetLineWidth(4)     ; graph_eff2mu.SetMarkerStyle(20) 
        graph_effmuinc        = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][3]) ; graph_effmuinc.SetLineColor(ROOT.kGreen+2) ; graph_effmuinc.SetLineWidth(4)     ; graph_effmuinc.SetMarkerStyle(20)  
        graph_effbench        = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][4]) ; graph_effbench.SetLineColor(ROOT.kBlack) ; graph_effbench.SetLineWidth(3)     ; graph_effbench.SetMarkerStyle(0)  
        graph_ratio           = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][5]) ; graph_ratio.SetLineColor(ROOT.kGreen+2) ; graph_ratio.SetLineWidth(3)     ; graph_ratio.SetMarkerStyle(0)  
        graph_ratio_boosted   = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][6]) ; graph_ratio_boosted.SetLineColor(ROOT.kBlue) ; graph_ratio_boosted.SetLineWidth(3)     ; graph_ratio_boosted.SetMarkerStyle(0)  
        graph_ratio_resolved  = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][7]) ; graph_ratio_resolved.SetLineColor(ROOT.kRed) ; graph_ratio_resolved.SetLineWidth(3)     ; graph_ratio_resolved.SetMarkerStyle(0)  


        graph_eff1mu.SetTitle("Boosted")
        graph_eff2mu.SetTitle("Resolved")
        graph_effmuinc.SetTitle('Boosted + Resolved')
        graph_effbench.SetTitle('EXO-16-023 Presel.')
        graph_effbench.SetLineStyle(2)
        graph_ratio.SetTitle('ratio')

        graph_eff1mu.SetMarkerColor(ROOT.kRed) 
        graph_eff2mu.SetMarkerColor(ROOT.kBlue) 
        graph_effmuinc.SetMarkerColor(ROOT.kGreen+2)  

        l.AddEntry(graph_effbench,"EXO-16-023")
        l.AddEntry(graph_eff1mu,"Resolved Presel.")
        l.AddEntry(graph_eff2mu,"Boosted Presel.")
        l.AddEntry(graph_effmuinc,"Boosted + Resolved")
        

        l2.AddEntry(graph_ratio,"#frac{Boosted + Resolved}{EXO-16-023}  ")
        #l2.AddEntry(graph_ratio_boosted,"#frac{Boosted}{EXO-16-023}  ")
        l2.AddEntry(graph_ratio_resolved,"#frac{Resolved}{EXO-16-023}")
        

        mg_mutau = ROOT.TMultiGraph()
        mg_mutau.Add(graph_eff1mu,"pl") 
        mg_mutau.Add(graph_eff2mu,"pl") 
        mg_mutau.Add(graph_effmuinc,"pl") 
        mg_mutau.Add(graph_effbench,"l")

        mg_ratio = ROOT.TMultiGraph()
        mg_ratio.Add(graph_ratio,"pc")
        #mg_ratio.Add(graph_ratio_boosted,"pc")
        mg_ratio.Add(graph_ratio_resolved,"pc")

        mg_mutau.GetYaxis().SetTitle("Acceptance #times Efficiency [%]")
        mg_mutau.GetYaxis().SetTitleOffset(0.95)
        mg_mutau.GetYaxis().SetTitleSize(0.05)
        mg_mutau.GetYaxis().SetRangeUser(0.00,max(d[mWR][3])*1.8)
        mg_mutau.GetXaxis().SetTitle("m_{N} [GeV]")

        latex = ROOT.TLatex()
        latex.SetNDC()
        c.SetLeftMargin(0.15)

        c.cd()
        pad_up.cd()
        mg_mutau.GetYaxis().SetLabelSize(0.05)
        mg_mutau.GetXaxis().SetLabelSize(0)
        mg_mutau.Draw("a")
        textSize = 1.0*ROOT.gStyle.GetPadTopMargin()
        latex.SetTextFont(61)
        latex.SetTextSize(textSize)
        latex.DrawLatex(0.15, 0.775,"CMS")
        latex.SetTextFont(52)
        latex.SetTextSize(0.6*textSize)
        latex.DrawLatex(0.15, 0.72,"Simulation")
        latex.SetTextFont(42)
        latex.SetTextSize(0.4*textSize)

        latex.DrawLatex(0.15, 0.6,"#mu#tau_{h} Channel")
        latex.DrawLatex(0.15, 0.65,f"m(W_{{R}}) = {mWR/1000} TeV")
        l.Draw()
        
        pad_down.cd()
        mg_ratio.GetXaxis().SetTitle("m_{N} [TeV]")
        mg_ratio.GetXaxis().SetTitleSize(0.12)
        mg_ratio.GetXaxis().SetNdivisions(5)
        #mg_ratio.GetYaxis().SetNdivisions(301)
        mg_ratio.GetYaxis().SetRangeUser(0.95,max(d[mWR][5])*1.2)
        mg_ratio.GetYaxis().SetLabelSize(0.1)
        mg_ratio.GetXaxis().SetLabelSize(0.1)
        pad_down.SetLogy()
        #mg_ratio.GetYaxis().SetLabelSize(1)
        mg_ratio.Draw("ac")
        l2.Draw()

        c.cd()
        pad_up.Draw()
        pad_down.Draw()
        #c1.SaveAs(f"{savedir}/mWR{mWR}_ElTau_PreselEff.pdf")
        c.SaveAs(f"{savedir}/mWR{mWR}_MuTau_PreselCompare_MuFinal.pdf")
        c.SaveAs(f"{savedir}/mWR{mWR}_MuTau_PreselCompare_MuFinal.png")
        #print(d[mWR])