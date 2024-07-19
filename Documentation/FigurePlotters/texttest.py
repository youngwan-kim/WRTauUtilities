import ROOT

def draw_multiline_text(x, y, lines, text_size=0.04, line_spacing=1.2):
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
    
    n_lines = len(lines)
    total_height = (n_lines - 1) * text_size * line_spacing
    
    for i, line in enumerate(lines):
        y_offset = (total_height / 2.0) - (i * text_size * line_spacing)
        latex.DrawLatexNDC(x, y + y_offset, line)

# Create a canvas
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

# Define the text lines
lines = ["AR-Like", "QCD Fake", "Measurement","Region"]

# Draw the multiline text at the center of the canvas
draw_multiline_text(0.5, 0.5, lines)

# Update the canvas to display the text
canvas.Update()

# Save the canvas to a file
canvas.SaveAs("central_text.png")