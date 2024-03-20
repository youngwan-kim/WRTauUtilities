from ROOT import *
from ROOT import TMath
from utils import *
import os
gStyle.SetOptFit(1100)

filestr = "20240318_145423_MCWeight_BinOptv1"
os.system(f"mkdir -p FitResults/{filestr}")


d_region = {#"Inclusive":[600,100],
            "ResolvedSignalRegionMETInvert":[[],[],[],[450,30],[525,25]],
            "BoostedSignalRegionMETInvert":[[],[],[],[320,40],[550,50]]}

for j, era in enumerate(["2016preVFP","2016postVFP","2016","2017","2018"]):
    os.system(f" > FitResults/{filestr}/FitParam_{era}.txt")
    for r in d_region :
        if len(d_region[r][j]) == 0 : continue
        else :
            file = TFile(f"Files/{filestr}/{era}.root")
            hist = file.Get(f"{r}_DataDrivenSubtract_All_All")

            quadratic = "[0] + [1]*x + [2]*x**2 + [3]*x**3  + [4]*x**4 "
            parabolic = "[0] + [1]*x + [2]*x**2 "
            params = [0, 0, 0, 0, 0]
            params_p = [0, 0, 0]
            constant = "[0]"

            polynomial_formula = parabolic

            boundary = d_region[r][j][0] ; interval = d_region[r][j][1]
            print(f"Boundary: {boundary} Interval: {interval} @ {r} {era} enum {j}")

            f = TF1("f", polynomial_formula, 190, boundary)  # piecewise scenario , lower pT polynomial degree 4
            g = TF1("g",constant,boundary-interval,2000)          # piecewise scenario , higher pT low stat bin constant fit
            #h = TF1("h", polynomial_formula, 190, 2000)     # whole scenario     , single polynomial fit with degree 4
            #h = TF1("h", parabolic, 190, boundary)

            for i, value in enumerate(params):
                f.SetParameter(i, value)
            
            hist.Fit("f", "R")
            fit_results = hist.GetFunction("f")  

            hint0 = TH1D(f"hint0{r}",f"confband0{r}",boundary-190,190,boundary)
            TVirtualFitter.GetFitter().GetConfidenceIntervals(hint0,0.68)
            hint0.SetStats(0)
            hint0.SetFillStyle(3005)

            deg = f.GetNumberFreeParameters() - 1 

            #print("Fit Results:")
            #with open(f"FitResults/{filestr}/FitParam.txt",'w') as file :
            #    print("test1")
            #    file.write("Fitting Function 1 \n")
            #    file.write(f"{polynomial_formula} from 190 to {boundary} \n")
            #    print("test2")
            #    for i in range(len(params)):
            #        print("Parameter {}: {} +/- {}".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))
            #        file.write("Parameter {}: {} +/- {} \n".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))

            g.SetParameter(0,f(boundary))
            #g.SetParameter(0,0.1)
            #g.SetParameter(1,0.1)
            hist.Fit("g", "R")
            fit_results_tail = hist.GetFunction("g")


            hint = TH1D(f"hint{r}",f"confband{r}",1200,boundary-interval,2000)
            TVirtualFitter.GetFitter().GetConfidenceIntervals(hint,0.68)
            hint.SetStats(0)
            hint.SetFillStyle(3004)


            #with open(f"FitResults/{filestr}/FitParam.txt",'a') as file :
            #    file.write("\n Fitting Function 2 \n")
            #    file.write(f"{constant} from {boundary-200} to 1500 \n")
            #    file.write("Parameter : {} +/- {} \n".format(fit_results_tail.GetParameter(0), fit_results_tail.GetParError(0)))

            #hist.Fit("h", "R")
            #fit_results = hist.GetFunction("h")

            #print("Fit Results:")
            #with open(f"FitResults/{filestr}/FitParam.txt",'a') as file :
            #    file.write("\n Fitting Function 3 \n")
            #    file.write(f"{polynomial_formula} from 190 to 1500 \n")
            #    for i in range(len(params)):
            #        print("Parameter {}: {} +/- {}".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))
            #        file.write("Parameter {}: {} +/- {} \n".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))
            #

            #print("Fit Results:")
            #print("Parameter {}: {:.3f} +/- {:.3f}".format(0, fit_results_tail.GetParameter(0), fit_results.GetParError(0)))
            
            # Draw the histogram and the fit function
            canvas = TCanvas(f"canvas{r}", "Fitted Histogram",1000,1000)
            l = TLegend(0.575,0.645,0.865,0.845)
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
            hist.GetYaxis().SetRangeUser(0,0.65)
            #histerr.Draw("e0")
            hist.Draw("e1")
            drawLatex_Fitter(r,era,"Fake")
            f.SetLineColor(kRed)
            f.SetFillStyle(0)
            f.SetLineWidth(3)
            f.Draw("same")
            f_label = f.Clone("flabel")
            f_label.SetFillStyle(3005)
            f_label.SetFillColor(kRed)
            g.SetLineColor(kBlue)
            g.SetFillStyle(0)
            g.SetLineWidth(3)
            g.Draw("same")
            g_label = g.Clone("glabel")
            g_label.SetFillStyle(3004)
            g_label.SetFillColor(kBlue)
            hint.SetFillColor(kBlue)
            hint.Draw("e3&same")
            hint0.SetFillColor(kRed)
            hint0.Draw("e3&same")
            #h.SetLineColor(kMagenta)
            #h.SetLineWidth(3)
            #h.Draw("same")
            for _h in [hist,hint,hint0] :
                _h.SetDirectory(0)

            chi2_1 =  f.GetChisquare()
            chi2_2 =  g.GetChisquare()
            #chi2_3 =  h.GetChisquare()
            ndf_1  =  f.GetNDF()
            ndf_2  =  g.GetNDF()
            #ndf_3  =  h.GetNDF()
            #err_2 = r.ParError(0)

            #print(err_2)

            pol_fitness  = f"{chi2_1:.2f}/{ndf_1} = {chi2_1/ndf_1:.2f}"
            tail_fitness = f"{chi2_2:.2f}/{ndf_2} = {chi2_2/ndf_2:.2f}"
            #whole_fitness = f"{chi2_3:.2f}/{ndf_3} = {chi2_3/ndf_3:.2f}"
            #.SetFillColor(kBlue); #g.SetFillStyle(3004)
            #f.SetFillColor(kRed); #f.SetFillStyle(3005)
            l.AddEntry(f_label,"#splitline{Polynomial (deg="+str(deg)+")}{#scale[0.75]{( #chi^{2}/ndf = "+pol_fitness+" )}}","lf")
            l.AddEntry(g_label,"#splitline{Constant}{#scale[0.75]{( #chi^{2}/ndf = "+tail_fitness+" )}}","lf")
            #l.AddEntry(hint,"#splitline{Constant 68% CI}{#scale[0.75]{( #chi^{2}/ndf = "+tail_fitness+" )}}","f")
            #l.AddEntry(h,"#splitline{Polynomial (deg=4, whole)}{#scale[0.75]{( #chi^{2}/ndf = "+whole_fitness+" )}}","l")
            l.Draw()

            #x_intersection = Math.BrentRootFinder(Math.BrentRootFinderOptions(), 0).Solve(f, tailconstant_func, 0, 1500)
            #combined_func = ROOT.TF1("combined_func", "[0]*x + [1]*(x >= %f)" % x_intersection, 0, 1500)
            #combined_func.SetParameters(f.GetParameter(0), tailconstant_func.GetParameter(1))
            #print(x_intersection)
            #combined_func = TF1("combined_func", "f *(x < %f) + tailconstant_func *(x >= %f)" % (x_intersection, x_intersection), 0, 1500)

            #finter = lambda x: abs(f.EvalPar(x) - tailconstant_func.EvalPar(x))
            #x_int = 
            #combined_func = TF1("combined", "max(f,g)" ,0,2000)
            combined_func = TF1("combined", " g *(f < g) + f * (f >= g) " ,0,2000)
            output_file = TFile(f"FitResults/{filestr}/FitFunction_{r}_{era}_dim{deg}.root", "RECREATE")
            f.Write()
            g.Write()
            combined_func.Write()
            output_file.Close()

            # Show the canvas
            canvas.Update()
            canvas.Draw()
            canvas.SaveAs(f"FitResults/{filestr}/FitPlot_{r}_{era}_dim{deg}.png")
            canvas.SaveAs(f"FitResults/{filestr}/FitPlot_{r}_{era}_dim{deg}.pdf")
            canvas.Close()