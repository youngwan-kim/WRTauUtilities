import ROOT
from ROOT import TCanvas, TPolyLine3D, TPolyMarker3D, TAxis3D, TArrow3D

# Create a canvas
canvas = TCanvas("canvas", "3D Octet with Orthogonal Planes", 800, 600)

# Create and draw the coordinate axes with arrows
arrows = []

# X-axis
arrow_x = TArrow3D(0, 0, 0, 1, 0, 0, 0.02, "|>")
arrows.append(arrow_x)

# Y-axis
arrow_y = TArrow3D(0, 0, 0, 0, 1, 0, 0.02, "|>")
arrows.append(arrow_y)

# Z-axis
arrow_z = TArrow3D(0, 0, 0, 0, 0, 1, 0.02, "|>")
arrows.append(arrow_z)

# Draw the arrows
for arrow in arrows:
    arrow.SetLineColor(ROOT.kBlack)
    arrow.SetFillColor(ROOT.kBlack)
    arrow.SetLineWidth(2)
    arrow.Draw()

# Create two orthogonal planes in the first octant
plane1 = TPolyLine3D()
plane1.SetNextPoint(0, 0, 0)
plane1.SetNextPoint(1, 0, 0)
plane1.SetNextPoint(1, 1, 0)
plane1.SetNextPoint(0, 1, 0)
plane1.SetNextPoint(0, 0, 0)
plane1.SetNextPoint(0, 0, 1)
plane1.SetNextPoint(1, 0, 1)
plane1.SetNextPoint(1, 1, 1)
plane1.SetNextPoint(0, 1, 1)
plane1.SetNextPoint(0, 0, 1)

plane2 = TPolyLine3D()
plane2.SetNextPoint(0, 0, 0)
plane2.SetNextPoint(0, 1, 0)
plane2.SetNextPoint(0, 1, 1)
plane2.SetNextPoint(0, 0, 1)
plane2.SetNextPoint(0, 0, 0)
plane2.SetNextPoint(1, 0, 0)
plane2.SetNextPoint(1, 0, 1)
plane2.SetNextPoint(1, 1, 1)
plane2.SetNextPoint(0, 1, 1)

# Draw the planes
plane1.SetLineColor(ROOT.kBlack)
plane1.SetLineWidth(1)
plane1.Draw()

plane2.SetLineColor(ROOT.kBlack)
plane2.SetLineWidth(1)
plane2.Draw()

# Set up 3D axes (hidden in this case, as we use arrows)
axis3D = TAxis3D()
axis3D.SetAxisColor(ROOT.kWhite)  # Hide the default axis
axis3D.Draw()

# Update the canvas
canvas.Update()

# Save the canvas to a file
canvas.SaveAs("3D_Octet_Orthogonal_Planes_Black.png")


