import os,ROOT,array

d = {}
color = [ROOT.kRed,ROOT.kOrange+8,ROOT.kGreen+3,ROOT.kBlue+2,ROOT.kMagenta,ROOT.kMagenta+1,ROOT.kPink+7]
xaxis = array.array('d',[0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85])
# WR2000_N100 : [fom1,fom2,...]
with open(f"{os.getenv('WRTau_Data')}/LSF_Eff.txt") as f :
    for line in f :
        signal = line.split(",")[0]
        cut = float(line.split(",")[1])
        fom = float(line.split(",")[4])
        #print(f"{signal},{fom}")
        if signal not in d :
            fomarr = array.array('d'); fomarr.append(fom)
            d[signal] = fomarr
        else : d[signal].append(fom)

    del d["WR3600_N100"] ; del d["WR4000_N100"] ; del d["WR4400_N100"] ; del d["WR4800_N200"]
    print(d)
    c = ROOT.TCanvas("lsf","",1000,1000)
    #c.SetLogy()
    l = ROOT.TLegend(0.55,0.685,0.925,0.875)
    l.SetFillStyle(0)
    l.SetBorderSize(0)

    mg = ROOT.TMultiGraph()
    i_c=0
    for signal in d :
        graph = ROOT.TGraph(len(xaxis),xaxis,d[signal]) 
        graph.SetLineColor(color[i_c])
        graph.SetLineWidth(3)
        graph.SetMarkerColor(color[i_c])
        graph.SetMarkerStyle(20)
        l.AddEntry(graph,signal)
        mg.Add(graph,"lp")
        i_c += 1

    mg.GetYaxis().SetTitle("S/#sqrt{B}")
    mg.GetYaxis().SetRangeUser(0,10)
    mg.GetXaxis().SetTitle("LSF Cut")

    latex = ROOT.TLatex()
    latex.SetNDC()
    c.SetLeftMargin(0.15)
    c.cd() 
    mg.Draw("a")
    l.Draw()
    c.SaveAs(f"test.pdf")