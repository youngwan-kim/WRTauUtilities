import ROOT

def draw_multiline_text(x, y, color,lines, text_size=0.0425, line_spacing=1.2):
    """
    Draw multiline text centered at (x, y) using TLatex.
    
    Args:
        x (float): x-coordinate (NDC) for the center of the text block.
        y (float): y-coordinate (NDC) for the center of the text block.
        lines (list of str): List of lines of text to display.
        text_size (float): Size of the text.
        line_spacing (float): Spacing between lines (as a multiple of text size).
    """
    latex = ROOT.TLatex()
    latex.SetTextAlign(22)  # Center align horizontally and vertically
    latex.SetTextSize(text_size)
    latex.SetTextColor(color)
    
    n_lines = len(lines)
    total_height = (n_lines - 1) * text_size * line_spacing
    
    for i, line in enumerate(lines):
        y_offset = (total_height / 2.0) - (i * text_size * line_spacing)
        latex.DrawLatexNDC(x, y + y_offset, line)

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

label_y1 = ROOT.TLatex(0.055, 0.65, "#splitline{DeepTau vsJet}{Tight}")
label_y1.SetTextAngle(90)
label_y1.SetTextSize(0.035)
label_y1.SetTextFont(42)
label_y1.Draw()

label_y2 = ROOT.TLatex(0.055, 0.15, "#splitline{DeepTau vsJet}{VVVLoose & !Tight}")
label_y2.SetTextAngle(90)
label_y2.SetTextSize(0.035)
label_y2.SetTextFont(42)
label_y2.Draw()

cut_x = ROOT.TLatex(0.42, 0.05, "100")
#cut_y.SetTextAngle(90)
cut_x.SetTextSize(0.045)
cut_x.SetTextFont(42)
cut_x.Draw()

# Create a dashed line for the horizontal axis
line_horizontal = ROOT.TLine(0.1, 0.5, 1, 0.5)
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

rectangle = ROOT.TPad("SR", "SR", 0.45, 0.5, 1.0, 1.0)
rectangle.SetFillColorAlpha(ROOT.kGreen, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
label_SR = ROOT.TLatex(0.575, 0.725, "Signal Region")
label_SR.SetTextSize(0.055)
label_SR.SetTextFont(61)
label_SR.SetTextColor(ROOT.kGreen+2)
label_SR.Draw()


label_SR3 = ROOT.TLatex(0.5, 0.285, "Application Region")
label_SR3.SetTextSize(0.055)
label_SR3.SetTextFont(61)
label_SR3.SetTextColor(ROOT.kGreen+2)
label_SR3.Draw()

rectangle = ROOT.TPad("SRloose", "SRloose", 0.45, 0.1, 1.0, 0.5)
rectangle.SetFillColorAlpha(ROOT.kGreen, 0.1)  # Set blue color with 50% transparency
rectangle.Draw()



rectangle = ROOT.TPad("LMCR", "LMCR", 0.1, 0.5, 0.45, 1.0)
rectangle.SetFillColorAlpha(ROOT.kRed, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
rectangle = ROOT.TPad("LMCR", "LMCR", 0.1, 0.1, 0.45, 0.5)
rectangle.SetFillColorAlpha(ROOT.kRed, 0.1)  # Set blue color with 50% transparency
rectangle.Draw()
lines = ["QCD Fake", "Measurement","Region","(SR-Like)"]
draw_multiline_text(0.28, 0.75, ROOT.kRed+2, lines)
'''label_LMCR = ROOT.TLatex(0.195, 0.775, "QCD Fake")
label_LMCR.SetTextSize(0.04)
label_LMCR.SetTextFont(61)
label_LMCR.SetTextColor(ROOT.kRed+2)
label_LMCR.Draw()
label_LMCR2 = ROOT.TLatex(0.21, 0.725, "Measurement")
label_LMCR2.SetTextSize(0.04)
label_LMCR2.SetTextFont(61)
label_LMCR2.SetTextColor(ROOT.kRed+2)
label_LMCR2.Draw()
label_LMCR3 = ROOT.TLatex(0.215, 0.675, "Region")
label_LMCR3.SetTextSize(0.04)
label_LMCR3.SetTextFont(61)
label_LMCR3.SetTextColor(ROOT.kRed+2)
label_LMCR3.Draw()
'''
#label_LMCR00 = ROOT.TLatex(0.225, 0.375, "Loose")
#label_LMCR00.SetTextSize(0.045)
#label_LMCR00.SetTextFont(61)
#label_LMCR00.SetTextColor(ROOT.kRed+2)
#label_LMCR00.Draw()
lines = ["QCD Fake", "Measurement","Region","(AR-Like)",]
draw_multiline_text(0.28, 0.3, ROOT.kRed+2, lines)

'''
rectangle = ROOT.TPad("FM", "FM", 0.1, 0.1, 1.0, 0.6)
rectangle.SetFillColorAlpha(ROOT.kBlue, 0.25)  # Set blue color with 50% transparency
rectangle.Draw()
label_FM = ROOT.TLatex(0.45, 0.375, "Low Mass")
label_FM.SetTextSize(0.05)
label_FM.SetTextFont(61)
label_FM.SetTextColor(ROOT.kBlue+2)
label_FM.Draw()
label_FM2 = ROOT.TLatex(0.385, 0.325, "Control Region")
label_FM2.SetTextSize(0.05)
label_FM2.SetTextFont(61)
label_FM2.SetTextColor(ROOT.kBlue+2)
label_FM2.Draw()
'''
# Draw the canvas
canvas.Draw()
canvas.SaveAs("VVVLooseDefinition.png")
canvas.SaveAs("VVVLooseDefinition.pdf")
# Run the event loop
#ROOT.gApplication.Run()
