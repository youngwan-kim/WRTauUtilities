import os
import shutil
import ROOT

resolved = "WRTau_ResolvedEE_AJ40_pt_eta_2016_WRTau_ResolvedEE_AJ40_pt_eta"
boosted =  "WRTau_BoostedEE_AJ40_pt_eta_2016_WRTau_BoostedEE_AJ40_pt_eta"

def process_root_file(input_file, output_directory):
    # Open input file
    input_root_file = ROOT.TFile.Open(input_file)
    if not input_root_file:
        print(f"Error: Unable to open file '{input_file}'")
        return

    # Check if the file contains the required histograms
    if not input_root_file.Get(resolved) or not input_root_file.Get(boosted):
        print(f"Error: Input file '{input_file}' does not contain required histograms.")
        input_root_file.Close()
        return

    # Create output file
    output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file))[0] + "_processed.root")
    output_root_file = ROOT.TFile(output_file, "RECREATE")

    # Copy histograms and modify as needed
    histogram_a = input_root_file.Get(resolved).Clone("Resolved")
    histogram_b = input_root_file.Get(boosted).Clone("Boosted")
    histogram_b_test = histogram_b.Clone("Boosted_test")
    
    for bin_x in range(1, histogram_b_test.GetNbinsX() + 1):
           for bin_y in range(1, histogram_b_test.GetNbinsY() + 1):
               histogram_b_test.SetBinContent(bin_x, bin_y, 1)
               histogram_b_test.SetBinError(bin_x, bin_y, 0)
    
    # Write histograms to output file
    output_root_file.cd()
    histogram_a.Write()
    histogram_b.Write()
    histogram_b_test.Write()
    
    # Close files
    input_root_file.Close()
    output_root_file.Close()

def main():
    # Find all FR*.root files in the current directory
    root_files = [file for file in os.listdir() if file.startswith("FR") and file.endswith(".root")]

    # Process each root file
    for root_file in root_files:
        process_root_file(root_file, ".")

if __name__ == "__main__":
    # Initialize PyROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(True)

    # Run main function
    main()
