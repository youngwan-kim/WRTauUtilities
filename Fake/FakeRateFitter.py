from ROOT import *
from ROOT import TMath
import os
gStyle.SetOptFit(1100)

def drawLatex(region,genmatch,x1=0.175,y1=0.8,x2=0.575,y2=0.925):
    latex = TLatex()
    latex.SetNDC()
    textSize = 0.625*gStyle.GetPadTopMargin()
    latex.SetTextFont(61)
    latex.SetTextSize(textSize*1.15)
    latex.DrawLatex(x1, y1 ,"CMS") # 0.85

    latex.SetTextFont(52)
    latex.SetTextSize(0.6*textSize)
    latex.DrawLatex(x1, y1-0.05,"Work In Progress")
    latex.DrawLatex(x1, y1-0.08,"Preliminary")
    latex.SetTextFont(42)
    latex.SetTextSize(0.55*textSize)
    #lumi = str(getLumi(str(args.era)))
    lumi = 41.5
    latex.DrawLatex(x2, y2-0.01,f"{lumi} fb^{{-1}} (13 TeV, 2017)")

    latex.SetTextFont(42)
    if   region == "BoostedSignalRegionMETInvert"   : region_latex = "Boosted Fake CR"
    elif region == "ResolvedSignalRegionMETInvert"  : region_latex = "Resolved Fake CR"
    elif region == "Inclusive"                      : region_latex = "Inclusive Fake CR"
    latex.SetTextSize(0.5*textSize)
    latex.DrawLatex(x1, y1-0.125,f"{region_latex}")
    latex.SetTextSize(0.425*textSize)
    latex.DrawLatex(x1, y1-0.15,"(#eta Inclusive , #AK4 Inclusive)")


filestr = "20240116_163307_MCWeight_BinTest"
os.system(f"mkdir -p FitResults/{filestr}")
os.system(f" > FitResults/{filestr}/FitParam.txt")

file = TFile(f"Files/{filestr}.root")

d_region = {#"Inclusive":[600,100],
            "ResolvedSignalRegionMETInvert":[550,50],
            "BoostedSignalRegionMETInvert":[500,100]}

for r in d_region :
    hist = file.Get(f"{r}_DataDriven_All_All")

    polynomial_formula = "[0] + [1]*x + [2]*x**2 + [3]*x**3  + [4]*x**4 "
    params = [0, 0, 0, 0, 0]
    constant = "[0]"

    boundary = d_region[r][0] ; interval = d_region[r][1]

    f = TF1("f", polynomial_formula, 190, boundary)  # piecewise scenario , lower pT polynomial degree 4
    g = TF1("g",constant,boundary-interval,2000)          # piecewise scenario , higher pT low stat bin constant fit
    #h = TF1("h", polynomial_formula, 190, 2000)     # whole scenario     , single polynomial fit with degree 4

    for i, value in enumerate(params):
        f.SetParameter(i, value)
    #    h.SetParameter(i, value)

    hist.Fit("f", "R")
    fit_results = hist.GetFunction("f")
    print("test")

    hint0 = TH1D(f"hint0{r}",f"confband0{r}",boundary-190,190,boundary)
    TVirtualFitter.GetFitter().GetConfidenceIntervals(hint0,0.68)
    hint0.SetStats(0)
    hint0.SetFillStyle(3005)


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
    drawLatex(r,"Fake")
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
    for h in [hist,hint,hint0] :
        h.SetDirectory(0)

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
    l.AddEntry(f_label,"#splitline{Polynomial (deg="+str(len(params)-1)+")}{#scale[0.75]{( #chi^{2}/ndf = "+pol_fitness+" )}}","lf")
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
    output_file = TFile(f"FitResults/{filestr}/FitFunction_{r}.root", "RECREATE")
    f.Write()
    g.Write()
    combined_func.Write()
    output_file.Close()

    # Show the canvas
    canvas.Update()
    canvas.Draw()
    canvas.SaveAs(f"FitResults/{filestr}/FitPlot_{r}.png")
    canvas.SaveAs(f"FitResults/{filestr}/FitPlot_{r}.pdf")
    canvas.Close()

