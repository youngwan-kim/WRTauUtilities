from ROOT import *
from ROOT import TMath
from utils import *
import os
gStyle.SetOptFit(1100)
gROOT.SetBatch(True)

filestr = "20240415_160115_BinOptv2_FlavourSplit"
os.system(f"mkdir -p FitResults/{filestr}/LinearGauss")

'''
                f.SetParameter(0,0.1) # gaussian amplitude
                f.SetParameter(1,250)       # gaussian mean
                f.SetParameter(2,50)      # gaussian resol.
                f.SetParameter(3,0.)      # linear slope
                f.SetParameter(4,0.)       # linear offset        
'''

d_region = {#"Inclusive":[600,100],
            #"ResolvedSignalRegionMETInvert"       : [[],[],[],[450,70],[525,45]],
            #"BoostedSignalRegionMETInvert"        : [[],[],[],[450,70],[550,100]],
            "ResolvedSignalRegionMETInvert_ElTau" : [[],[],[],[],[0.15,350,20,0.001,0.2]],
            #"BoostedSignalRegionMETInvert_ElTau"  : [[],[],[],[0.1,250,50,0,0],[0.1,250,50,0,0]],
            #"ResolvedSignalRegionMETInvert_MuTau" : [[],[],[0.1,250,50,0,0],[0.1,250,50,-0.001,0.2],[0.1,250,50,0,0]],
            "BoostedSignalRegionMETInvert_MuTau"  : [[],[],[],[0.1,250,50,0,0],[]],
}

l_region = {}

def combinedFit(x,p):
    x0 = p[0]
    if x < x0:
        return f(x)
    else:
        return g(x)

output_file_test = TFile(f"FitResults/{filestr}/LinearGauss/FitResults.root", "RECREATE")

for j, era in enumerate(["2016preVFP","2016postVFP","2016","2017","2018"]):
    for r in d_region :
        if len(d_region[r][j]) == 0 : continue
        else :
            output_file_test.mkdir(f"{r}_{era}")
            os.system(f" > FitResults/{filestr}/FitParam_{r}_{era}.txt")
            file = TFile(f"Files/{filestr}/{era}_Data.root")
            hist = file.Get(f"{r}_DataDrivenSubtract_All_All")
 
            polynomial_formula = "[0] * exp(-(x-[1])**2/(2*[2]**2))  + [3]*x + [4]"

            #boundary = d_region[r][j][0] ; interval = d_region[r][j][1]
            #print(f"Boundary: {boundary} Interval: {interval} @ {r} {era} enum {j}")

            f = TF1("f", polynomial_formula, 190, 1000)  # piecewise scenario , lower pT polynomial degree 4
            

            if len(d_region[r][j]) == 5 :
                for i in range(0,5) :
                    f.SetParameter(i,d_region[r][j][i])

            else :
                f.SetParameter(0,0.1) # gaussian amplitude
                f.SetParameter(1,250)       # gaussian mean
                f.SetParameter(2,50)      # gaussian resol.
                f.SetParameter(3,0.)      # linear slope
                f.SetParameter(4,0.)       # linear offset            

            #g = TF1("g",constant,boundary-interval,2000)          # piecewise scenario , higher pT low stat bin constant fit

            hist.Fit("f", "R")

            fit_results = hist.GetFunction("f")  

            hint0 = TH1D(f"hint0{r}",f"confband0{r}",1000-190,190,1000)
            TVirtualFitter.GetFitter().GetConfidenceIntervals(hint0,0.68)
            hint0.SetStats(0)
            hint0.SetFillStyle(1001)

            #logger = "{ "

            #if deg == 2 : logger += f"p[0] = {fit_results.GetParameter(0)} ; p[1] = {fit_results.GetParameter(1)} ; p[2] = {fit_results.GetParameter(2)} ;"
            #elif deg == 3 : logger += f"p[0] = {fit_results.GetParameter(0)} ; p[1] = {fit_results.GetParameter(1)} ; p[2] = {fit_results.GetParameter(2)} ;  p[3] = {fit_results.GetParameter(3)} ;"
            #elif deg == 4 : logger += f"p[0] = {fit_results.GetParameter(0)} ; p[1] = {fit_results.GetParameter(1)} ; p[2] = {fit_results.GetParameter(2)} ;  p[3] = {fit_results.GetParameter(3)} ;  p[4] = {fit_results.GetParameter(4)} ;"
            #for i in range(len(params)):
            #    print(fit_results.GetParameter(i))

            #g.SetParameter(0,f(boundary))
            #hist.Fit("g", "R")
            #fit_results_tail = hist.GetFunction("g")



            #hint = TH1D(f"hint{r}",f"confband{r}",1200,boundary-interval,2000)
            #TVirtualFitter.GetFitter().GetConfidenceIntervals(hint,0.68)
            #hint.SetStats(0)
            #hint.SetFillStyle(3004)

            #logger += f"tail = {fit_results_tail.GetParameter(0)} ;"
            #if deg < 3 : print(logger+"}")

            # Draw the histogram and the fit function
            canvas = TCanvas(f"canvas{r}", "Fitted Histogram",1000,1000)
            l = TLegend(0.55,0.585,0.865,0.785)
            l.SetFillStyle(0)
            l.SetBorderSize(0)
            canvas.cd()
            canvas.SetLeftMargin(0.125)
            canvas.SetRightMargin(0.085)
            canvas.SetBottomMargin(0.125)
            hist.SetStats(0)
            histerr = hist.Clone("err")
            hist.SetLineColor(kBlack)
            hist.SetLineWidth(2)
            hist.GetXaxis().SetRangeUser(0,1000)
            hist.GetXaxis().SetTitle("p_{T}(#tau_{h})")
            hist.GetYaxis().SetTitle("FR(#tau_{h})")
            hist.GetXaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetRangeUser(0,1.0)
            #histerr.Draw("e0")
            hist.Draw("e1")
            drawLatex_Fitter(r,era,"Fake")
            latex = TLatex()
            latex.SetNDC()
            latex.SetTextFont(42)
            textSize = 0.625*gStyle.GetPadTopMargin()
            latex.SetTextSize(0.475*textSize)
            latex.DrawLatex(0.525,0.825,"FR(x) = A_{0}N(#mu,#sigma^{2}) + A_{1}x + A_{2}   ")
            f.SetLineColor(kRed)
            f.SetFillStyle(0)
            f.SetLineWidth(3)
            f.Draw("same")
            f_label = f.Clone("flabel")
            f_label.SetFillStyle(3005)
            f_label.SetFillColor(kRed)
            #g.SetLineColor(kBlue)
            #g.SetFillStyle(0)
            #g.SetLineWidth(3)
            #g.Draw("same")
            #g_label = g.Clone("glabel")
            #g_label.SetFillStyle(3004)
            #g_label.SetFillColor(kBlue)
            #hint.SetFillColor(kBlue)
            #hint.Draw("e3&same")
            hint0.SetFillColorAlpha(kRed,0.2)
            hint0.SetLineWidth(0)
            hint0.Draw("e3&same")
            #h.SetLineColor(kMagenta)
            #h.SetLineWidth(3)
            #h.Draw("same")
            for _h in [hist,hint0] :
                _h.SetDirectory(0)

            chi2_1 =  f.GetChisquare()
            #chi2_2 =  g.GetChisquare()
            #chi2_3 =  h.GetChisquare()
            ndf_1  =  f.GetNDF()
            #ndf_2  =  g.GetNDF()
            #ndf_3  =  h.GetNDF()
            #err_2 = r.ParError(0)

            #print(err_2)

            pol_fitness  = f"{chi2_1:.2f}/{ndf_1}" # = {chi2_1/ndf_1:.2f}"
            #tail_fitness = f"{chi2_2:.2f}/{ndf_2} = {chi2_2/ndf_2:.2f}"
            #whole_fitness = f"{chi2_3:.2f}/{ndf_3} = {chi2_3/ndf_3:.2f}"
            #.SetFillColor(kBlue); #g.SetFillStyle(3004)
            #f.SetFillColor(kRed); #f.SetFillStyle(3005)
            l.AddEntry(f_label,"#splitline{Gaussian + Linear}{#scale[0.75]{( #chi^{2}/ndf = "+pol_fitness+" )}}","l")
            #l.AddEntry(g_label,"#splitline{Constant}{#scale[0.75]{( #chi^{2}/ndf = "+tail_fitness+" )}}","lf")
            l.AddEntry(hint0,"#splitline{Fit Error}{#scale[0.75]{( 68% Confidence Interval )}}","f")
            #l.AddEntry(h,"#splitline{Polynomial (deg=4, whole)}{#scale[0.75]{( #chi^{2}/ndf = "+whole_fitness+" )}}","l")
            l.Draw()


            #output_file = TFile(f"FitResults/{filestr}/LinearGauss/FitFunction_{r}_{era}_LinearGauss.root", "RECREATE")
            output_file_test.cd(f"{r}_{era}")
            f.Write()
            #hint0.SetFillColor(kRed)
            #hint0.SetLineWidth(1)
            hint0.Write("unc")
            #g.Write()
            #combined_func_test = TF1("Combined", "abs(f-g)", 190, 1000, 1)
            #x_intersection = combined_func_test.GetMinimumX(250,2000)
            #logger += f"x0 = {x_intersection} ;"
            #if deg == 3 : print(logger+"}")
            #combined_func = TF1("Combined", combinedFit, 190, 1000, 1)  # Define TF1 with range (-10, 10) and 1 parameter
            #combined_func.SetParameter(0, x_intersection) 
            #print(x_intersection)
            #combined_func = TF1("Combined", lambda x, params: f(x) if x < params[0] else g(x), 190, 1000, 1)
            #combined_func.SetParameter(0, x_intersection) 
            #output_file.Close()

            # Show the canvas
            canvas.Update()
            canvas.Draw()
            canvas.SaveAs(f"FitResults/{filestr}/LinearGauss/FitPlot_{r}_{era}_LinearGauss.png")
            canvas.SaveAs(f"FitResults/{filestr}/LinearGauss/FitPlot_{r}_{era}_LinearGauss.pdf")
            canvas.Close()
output_file_test.Close()