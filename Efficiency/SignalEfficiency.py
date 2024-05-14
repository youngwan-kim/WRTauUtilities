import ROOT
import array,os

savedir = "../Plots/SignalEfficiency/"
os.system(f"mkdir -p {savedir}")

d = {}
# mWR : [mN array , eff1e , eff1mu , eff2e, eff2mu]
with open('eff_signal.txt') as f :
    for line in f :
        mWR = int(line.split(",")[0])
        mN = float(line.split(",")[1])
        eff_SR1el = float(line.split(",")[2])
        eff_SR1mu = float(line.split(",")[3])
        eff_SR2el = float(line.split(",")[4])
        eff_SR2mu = float(line.split(",")[5].rstrip())
        eff_Pre1el = float(line.split(",")[6])
        eff_Pre1mu = float(line.split(",")[7])
        eff_Pre2el = float(line.split(",")[8])
        eff_Pre2mu = float(line.split(",")[9].rstrip())

        if mWR not in d : 
            mnarr       =  array.array('d');  mnarr.append(mN)
            eff1e_arr   =  array.array('d');  eff1e_arr.append(eff_SR1el)
            eff1mu_arr  =  array.array('d');  eff1mu_arr.append(eff_SR1mu)
            eff2e_arr   =  array.array('d');  eff2e_arr.append(eff_SR2el)
            eff2mu_arr  =  array.array('d');  eff2mu_arr.append(eff_SR2mu)
            effelinc_arr =  array.array('d');  effelinc_arr.append(eff_SR1el+eff_SR2el)
            effmuinc_arr =  array.array('d');  effmuinc_arr.append(eff_SR1mu+eff_SR2mu)
            effPre1e_arr   =  array.array('d');  effPre1e_arr.append(eff_Pre1el)
            effPre1mu_arr  =  array.array('d');  effPre1mu_arr.append(eff_Pre1mu)
            effPre2e_arr   =  array.array('d');  effPre2e_arr.append(eff_Pre2el)
            effPre2mu_arr  =  array.array('d');  effPre2mu_arr.append(eff_Pre2mu)
            effPreelinc_arr =  array.array('d');  effPreelinc_arr.append(eff_Pre1el+eff_Pre2el)
            effPremuinc_arr =  array.array('d');  effPremuinc_arr.append(eff_Pre1mu+eff_Pre2mu)



            d[mWR] = [mnarr,eff1e_arr,eff1mu_arr,eff2e_arr,eff2mu_arr,effelinc_arr,effmuinc_arr,effPre1e_arr,effPre1mu_arr,effPre2e_arr,effPre2mu_arr,effPreelinc_arr,effPremuinc_arr]
        
        else :
            d[mWR][0].append(mN)
            d[mWR][1].append(eff_SR1el)
            d[mWR][2].append(eff_SR1mu)
            d[mWR][3].append(eff_SR2el)
            d[mWR][4].append(eff_SR2mu)
            d[mWR][5].append(eff_SR1el+eff_SR2el)
            d[mWR][6].append(eff_SR1mu+eff_SR2mu)
            d[mWR][7].append(eff_Pre1el)
            d[mWR][8].append(eff_Pre1mu)
            d[mWR][9].append(eff_Pre2el)
            d[mWR][10].append(eff_Pre2mu)
            d[mWR][11].append(eff_Pre1el+eff_Pre2el)
            d[mWR][12].append(eff_Pre1mu+eff_Pre2mu)

    for mWR in d :

        c1 = ROOT.TCanvas(f"{mWR}_BoostedSR","",1000,1000)
        c2 = ROOT.TCanvas(f"{mWR}_ResolvedSR","",1000,1000)
        l1 = ROOT.TLegend(0.425,0.685,0.925,0.875)
        l1.SetFillStyle(0)
        l1.SetNColumns(2)
        l1.SetBorderSize(0)
        l2 = ROOT.TLegend(0.55,0.685,0.925,0.875)
        l2.SetFillStyle(0)
        l2.SetBorderSize(0)


        #c1.GetYaxis().SetRangeUser(0,1)
        #c2.GetYaxis().SetRangeUser(0,1)

        graph_eff1e   = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][1]) ; graph_eff1e.SetLineColor(ROOT.kRed)       ; graph_eff1e.SetLineWidth(3)    ; graph_eff1e.SetMarkerStyle(20) 
        graph_eff2e   = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][3]) ; graph_eff2e.SetLineColor(ROOT.kBlue)      ; graph_eff2e.SetLineWidth(3)    ; graph_eff2e.SetMarkerStyle(20) 
        graph_effelinc = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][5]) ; graph_effelinc.SetLineColor(ROOT.kBlack) ; graph_effelinc.SetLineWidth(3) ; graph_effelinc.SetMarkerStyle(20)  

        graph_effPre1e    = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][7]) ; graph_effPre1e.SetLineColor(ROOT.kRed)       ; graph_effPre1e.SetLineWidth(3)    ; graph_effPre1e.SetMarkerStyle(20) 
        graph_effPre2e    = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][9]) ; graph_effPre2e.SetLineColor(ROOT.kBlue)      ; graph_effPre2e.SetLineWidth(3)    ; graph_effPre2e.SetMarkerStyle(20) 
        graph_effPreelinc = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][11]) ; graph_effPreelinc.SetLineColor(ROOT.kBlack) ; graph_effPreelinc.SetLineWidth(3) ; graph_effPreelinc.SetMarkerStyle(20)  


        graph_eff1e.SetMarkerColor(ROOT.kRed) 
        graph_eff2e.SetMarkerColor(ROOT.kBlue) 
        graph_effelinc.SetMarkerColor(ROOT.kBlack)  

        graph_effPre1e.SetMarkerColor(ROOT.kRed) 
        graph_effPre2e.SetMarkerColor(ROOT.kBlue) 
        graph_effPreelinc.SetMarkerColor(ROOT.kBlack)  

        graph_effPre1e.SetLineStyle(2) 
        graph_effPre2e.SetLineStyle(2) 
        graph_effPreelinc.SetLineStyle(2) 


        graph_eff1e.SetTitle("Boosted SR")
        graph_eff2e.SetTitle("Resolved SR")
        graph_effelinc.SetTitle('Total')

        l1.AddEntry(graph_eff1e,"Boosted SR")
        l1.AddEntry(graph_effPre1e,"Boosted Presel.")
        l1.AddEntry(graph_eff2e,"Resolved SR")
        l1.AddEntry(graph_effPre2e,"Resolved Presel.")
        l1.AddEntry(graph_effelinc,"Total")
        l1.AddEntry(graph_effPreelinc,"Total Presel.")
        

        graph_eff1mu  = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][2]) ; graph_eff1mu.SetLineColor(ROOT.kRed) ; graph_eff1mu.SetLineWidth(3)     ; graph_eff1mu.SetMarkerStyle(20) 
        graph_eff2mu  = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][4]) ; graph_eff2mu.SetLineColor(ROOT.kBlue) ; graph_eff2mu.SetLineWidth(3)     ; graph_eff2mu.SetMarkerStyle(20) 
        graph_effmuinc = ROOT.TGraph(len(d[mWR][0]),d[mWR][0],d[mWR][6]) ; graph_effmuinc.SetLineColor(ROOT.kBlack) ; graph_effmuinc.SetLineWidth(3)     ; graph_effmuinc.SetMarkerStyle(20)  

        graph_eff1mu.SetTitle("Boosted SR")
        graph_eff2mu.SetTitle("Resolved SR")
        graph_effmuinc.SetTitle('Total')

        graph_eff1mu.SetMarkerColor(ROOT.kRed) 
        graph_eff2mu.SetMarkerColor(ROOT.kBlue) 
        graph_effmuinc.SetMarkerColor(ROOT.kBlack)  

        l2.AddEntry(graph_eff1mu,"Boosted SR")
        l2.AddEntry(graph_eff2mu,"Resolved SR")
        l2.AddEntry(graph_effmuinc,"Total")


        mg_etau = ROOT.TMultiGraph()
        mg_etau.Add(graph_eff1e,"lp") ; mg_etau.Add(graph_eff2e,"lp") ; mg_etau.Add(graph_effelinc,"lp") 
        mg_etau.Add(graph_effPre1e,"lp") ; mg_etau.Add(graph_effPre2e,"lp") ; mg_etau.Add(graph_effPreelinc,"lp")
        mg_etau.GetYaxis().SetTitle("Acceptance #times Efficiency [%]")
        mg_etau.GetYaxis().SetRangeUser(0.00,10)
        mg_etau.GetXaxis().SetTitle("m_{N} [GeV]")

        mg_mutau = ROOT.TMultiGraph()
        mg_mutau.Add(graph_eff1mu,"lp") ; mg_mutau.Add(graph_eff2mu,"lp") ; mg_mutau.Add(graph_effmuinc,"lp") 
        mg_mutau.GetYaxis().SetTitle("Acceptance #times Efficiency [%]")
        mg_mutau.GetYaxis().SetTitleOffset(0)
        mg_mutau.GetYaxis().SetRangeUser(0.00,10)
        mg_mutau.GetXaxis().SetTitle("m_{N} [GeV]")

        latex = ROOT.TLatex()
        latex.SetNDC()
        c1.SetLeftMargin(0.15)
        c2.SetLeftMargin(0.15)
        c1.cd() ; mg_etau.Draw("a")
        c2.cd() ; mg_mutau.Draw("a")
        
        i=0
        for c in [c1,c2] :
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
            if i == 0 : 
                latex.DrawLatex(0.2, 0.685,"e#tau_{h} Channel")
                latex.DrawLatex(0.2, 0.715,f"m(W_{{R}}) = {mWR/1000.} TeV")
                l1.Draw()
            else : 
                latex.DrawLatex(0.2, 0.685,"#mu#tau_{h} Channel")
                latex.DrawLatex(0.2, 0.715,f"m(W_{{R}}) = {mWR/1000.} TeV")
                l2.Draw()
            i += 1


        c1.SaveAs(f"{savedir}/mWR{mWR}_ElTau_Eff.pdf")
        c2.SaveAs(f"{savedir}/mWR{mWR}_MuTau_Eff.pdf")

        #print(d[mWR])