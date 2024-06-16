import ROOT

# Create a canvas with margins
canvas = ROOT.TCanvas("canvas", "Axes with Arrows and Dashed Lines", 800, 800)
canvas.SetLeftMargin(0.2)
canvas.SetBottomMargin(0.2)

# Create a TArrow object for the x-axis
arrow_x = ROOT.TArrow(0.1, 0.1, 1, 0.1, 0.03, "|>")
arrow_x.SetLineWidth(3)
arrow_x.SetLineColor(ROOT.kBlack)
arrow_x.Draw()

# Create a TArrow object for the y-axis
arrow_y = ROOT.TArrow(0.1, 0.1, 0.1, 1, 0.03, "|>")
arrow_y.SetLineWidth(3)
arrow_y.SetLineColor(ROOT.kBlack)
arrow_y.Draw()

label_x = ROOT.TLatex(0.75, 0.025, "#slash{E}_{T} [GeV]")
label_x.SetTextSize(0.055)
label_x.SetTextFont(42)
label_x.Draw()

label_y = ROOT.TLatex(0.05, 0.775, "m_{Eff} [GeV]")
label_y.SetTextAngle(90)
label_y.SetTextSize(0.055)
label_y.SetTextFont(42)
label_y.Draw()

cut_y = ROOT.TLatex(0.02, 0.585, "900")
#cut_y.SetTextAngle(90)
cut_y.SetTextSize(0.045)
cut_y.SetTextFont(42)
cut_y.Draw()

cut_x = ROOT.TLatex(0.42, 0.05, "100")
#cut_y.SetTextAngle(90)
cut_x.SetTextSize(0.045)
cut_x.SetTextFont(42)
cut_x.Draw()

# Create a dashed line for the horizontal axis
line_horizontal = ROOT.TLine(0.1, 0.6, 1, 0.6)
line_horizontal.SetLineStyle(2)
line_horizontal.SetLineWidth(2)
line_horizontal.SetLineColor(ROOT.kBlack)
line_horizontal.Draw()

# Create a dashed line for the vertical axis
line_vertical = ROOT.TLine(0.45, 0.1, 0.45, 1)
line_vertical.SetLineStyle(2)
line_vertical.SetLineWidth(2)
line_vertical.SetLineColor(ROOT.kBlack)
line_vertical.Draw()

rectangle = ROOT.TPad("SR", "SR", 0.45, 0.6, 1.0, 1.0)
rectangle.SetFillColorAlpha(ROOT.kGreen, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
label_SR = ROOT.TLatex(0.575, 0.775, "Signal Region")
label_SR.SetTextSize(0.055)
label_SR.SetTextFont(61)
label_SR.SetTextColor(ROOT.kGreen+2)
label_SR.Draw()

rectangle = ROOT.TPad("LMCR", "LMCR", 0.1, 0.6, 0.45, 1.0)
rectangle.SetFillColorAlpha(ROOT.kRed, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
label_LMCR = ROOT.TLatex(0.195, 0.825, "Tau Fake")
label_LMCR.SetTextSize(0.045)
label_LMCR.SetTextFont(61)
label_LMCR.SetTextColor(ROOT.kRed+2)
label_LMCR.Draw()
label_LMCR2 = ROOT.TLatex(0.15, 0.775, "Measurement")
label_LMCR2.SetTextSize(0.045)
label_LMCR2.SetTextFont(61)
label_LMCR2.SetTextColor(ROOT.kRed+2)
label_LMCR2.Draw()
label_LMCR3 = ROOT.TLatex(0.215, 0.725, "Region")
label_LMCR3.SetTextSize(0.045)
label_LMCR3.SetTextFont(61)
label_LMCR3.SetTextColor(ROOT.kRed+2)
label_LMCR3.Draw()

rectangle = ROOT.TPad("FM", "FM", 0.45, 0.1, 1.0, 0.6)
rectangle.SetFillColorAlpha(ROOT.kBlue, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
label_FM = ROOT.TLatex(0.63, 0.375, "Low Mass")
label_FM.SetTextSize(0.05)
label_FM.SetTextFont(61)
label_FM.SetTextColor(ROOT.kBlue+2)
label_FM.Draw()
label_FM2 = ROOT.TLatex(0.565, 0.325, "Control Region")
label_FM2.SetTextSize(0.05)
label_FM2.SetTextFont(61)
label_FM2.SetTextColor(ROOT.kBlue+2)
label_FM2.Draw()

# Draw the canvas
canvas.Draw()
canvas.SaveAs("RegionDefinition.png")
canvas.SaveAs("RegionDefinition.pdf")
# Run the event loop
#ROOT.gApplication.Run()
