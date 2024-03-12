import glob,itertools,math,array,os
from ROOT import *

def FoM(sig, bkg): 
    return math.sqrt( 2.*((sig+bkg)*math.log(1+(sig/max(bkg,1e-20))) - sig))

def getXsec(mWR,mN) :
    with open("../Data/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

d_isocut = {0.25:"0p25", 0.45:"0p45", 0.50:"0p50", 0.55:"0p55", 0.75:"0p75"}
xaxis = array.array('d',[0.25,0.45,0.50,0.55,0.75])
dir_output = "/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/MuIsoCutOpt__/"
output_file = "/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/Efficiency/muisocut.txt"

file_pattern = dir_output + "WRTau_Analyzer_WRtoTauNtoTauTauJets_WR*_N*.root"
root_files = glob.glob(file_pattern)

f_bkg = TFile("/data9/Users/youngwan/SKFlatOutput/Run2UltraLegacy_v3/WRTau_Analyzer/2017/MuIsoCutOpt__/WRTau_Analyzer_Bkg.root")

nonprompt = [np1 + np2 for np1, np2 in itertools.product(["__NonPromptTau", "__PromptTau"], ["__NonPromptLepton", "__PromptLepton"])]

os.system(f"mkdir -p {os.getenv('WRTau_Plots')}/MuIsoCut/")

with open(output_file, "w") as file:
    for root_file in root_files:
        mwr = int(root_file.rsplit("_",2)[1].split("WR")[1])
        mn = int(root_file.rsplit("_",2)[2].split(".")[0].split("N")[1])

        c = TCanvas(f"muisocutopt_{mwr}_{mn}","",1000,1000)
        #l = ROOT.TLegend(0.55,0.685,0.925,0.875)
        #l.SetFillStyle(0)
        #l.SetBorderSize(0)
        
        mg = TMultiGraph()
        #print(mwr,mn)
        l_fom = []
        for cut, cut_name in d_isocut.items():
            f_sig = TFile(root_file)
            h_sig = f_sig.Get(f"MuIsoCutOpt_{cut_name}/vJetTight_vElTight_vMuTight/BoostedSignalRegion_MuTau/Nevents")
            if h_sig == None:
                s = 0
            else:
                s = h_sig.Integral()
            
            s *= 1/getXsec(mwr,mn)

            b = 0
            for np in nonprompt:
                h_bkg = f_bkg.Get(f"MuIsoCutOpt_{cut_name}{np}/vJetTight_vElTight_vMuTight/BoostedSignalRegion_MuTau/Nevents")
                #print(h_bkg)
                if h_bkg != None:
                    b += h_bkg.Integral()
            
            l_fom.append(FoM(s,b))
            line = f"{mwr},{mn},{cut},{s},{b},{FoM(s,b)}"
            file.write(line + "\n")

        a_fom = array.array('d',l_fom)
        graph = TGraph(len(xaxis),xaxis,a_fom) 
        graph.SetLineColor(kRed)
        graph.SetLineWidth(3)
        graph.SetMarkerColor(kRed)
        graph.SetMarkerStyle(20)
        mg.Add(graph,"lp")

        mg.GetYaxis().SetTitle("#sqrt{2[(s+b)ln(1+#frac{s}{b})-s]}")
        #mg.GetYaxis().SetRangeUser(0.0,1.0)
        mg.GetXaxis().SetTitle("TrkIso/Pt^{TuneP4} Cut")

        #latex = TLatex()
        #latex.SetNDC()
        c.SetLeftMargin(0.15)
        c.cd() 
        mg.Draw("a")
        #l.Draw()
        c.SaveAs(f"{os.getenv('WRTau_Plots')}/MuIsoCut/{mwr}_{mn}.pdf")
        c.SaveAs(f"{os.getenv('WRTau_Plots')}/MuIsoCut/{mwr}_{mn}.png")

