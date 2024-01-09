from ROOT import *
import os
gStyle.SetOptFit(1100)

filestr = "20240109_140142BinOpt2"
os.system(f"mkdir -p FitResults/{filestr}")
os.system(f" > FitResults/{filestr}/FitParam.txt")

f = TFile(f"Files/{filestr}.root")
hist = f.Get("Inclusive_FR_All_All")

polynomial_formula = "[0] + [1]*x + [2]*x**2 + [3]*x**3 + [4]*x**4 "
params = [0, 0, 0,0,0]

constant = "[0]"

boundary = 1000

polynomial_func = TF1("polynomial_func", polynomial_formula, 190, boundary)
tailconstant_func = TF1("const_func",constant,boundary-200,1500)

for i, value in enumerate(params):
    polynomial_func.SetParameter(i, value)

hist.Fit("polynomial_func", "R")
fit_results = hist.GetFunction("polynomial_func")


print("Fit Results:")
with open(f"FitResults/{filestr}/FitParam.txt",'w') as file :
    file.write("Fitting Function 1 \n")
    file.write(f"{polynomial_formula} from 190 to {boundary} \n")
    for i in range(len(params)):
        print("Parameter {}: {} +/- {}".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))
        file.write("Parameter {}: {} +/- {} \n".format(i, fit_results.GetParameter(i), fit_results.GetParError(i)))


tailconstant_func.SetParameter(0,polynomial_func(boundary))
hist.Fit("const_func", "R")
fit_results_tail = hist.GetFunction("const_func")


with open(f"FitResults/{filestr}/FitParam.txt",'a') as file :
    file.write("\n Fitting Function 2 \n")
    file.write(f"{constant} from {boundary-200} to 1500 \n")
    file.write("Parameter : {} +/- {} \n".format(fit_results_tail.GetParameter(0), fit_results_tail.GetParError(0)))

#print("Fit Results:")
#print("Parameter {}: {:.3f} +/- {:.3f}".format(0, fit_results_tail.GetParameter(0), fit_results.GetParError(0)))
# Draw the histogram and the fit function
canvas = TCanvas("canvas", "Fitted Histogram",1000,1000)
hist.SetStats(1)
histerr = hist.Clone("err")
histerr.SetLineColor(kBlack)
histerr.SetLineWidth(2)
histerr.Draw("e0")
hist.Draw("hist&same")
polynomial_func.SetLineColor(kMagenta)
polynomial_func.Draw("same")
tailconstant_func.SetLineColor(kMagenta)
tailconstant_func.Draw("same")


# Show the canvas
canvas.Update()
canvas.Draw()
canvas.SaveAs(f"FitResults/{filestr}/FitPlot.png")
canvas.SaveAs(f"FitResults/{filestr}/FitPlot.pdf")

