import os
from ROOT import *

rebins = [0,50,100,150,200,500,1000,1500,2000,2500,3000,3500,4000,5000,6000,7000,8000,9000,10000,15000]

d_mass = {
    2000 : [200,400,600,1000,1400,1800,1900],
    2400 : [100,400,600,800,1000,1400,1800,2200,2300],
    2800 : [200,400,600,800,1400,1800,2200,2600,2700],
    3200 : [200,400,600,800,1000,1400,1800,3000,3100],
    3600 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3500],
    4000 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,3900],
    4400 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3400,3800,4200,4300],
    4800 : [200,400,600,800,1000,1400,1800,2200,2600,3000,3800,4200,4600,4700],
}

def getXsec(mWR,mN) :
    with open(f"{os.getenv('WRTau_Data')}/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def GetSignalScale(mwr) :
    signal_scale = 1.0
    if mwr < 800.1 : signal_scale *= 0.1; 
    elif mwr < 3600.1 : signal_scale *= 50
    else : signal_scale *= 500
    return signal_scale


def GetSystList(stamp,samplename,era) :
    systDir  = f"{os.getenv('WRTau_Output')}/{stamp}/{era}/RunSyst"
    systFile = TFile(f"{systDir}/WRTau_Analyzer_{samplename}.root")
    
    systList = []

    for key in systFile.GetListOfKeys():
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            systName = obj.GetName()
            systList.append(systName)

    systFile.Close()
    return systList

def check(root_file, histogram_name):

    if not root_file or root_file.IsZombie():
        print("Error: Unable to open file:", file_name)
        return False

    histogram = root_file.Get(histogram_name)

    if histogram:
        #print("Histogram", histogram_name, "exists in the file.")
        return True
    else:
        #print("Histogram", histogram_name, "does not exist in the file.")
        return False


def round_histogram(histogram):
    rounded_histogram = histogram.Clone()
    for bin in range(1, histogram.GetNbinsX() + 1):
        bin_content = histogram.GetBinContent(bin)
        rounded_content = int(round(bin_content))
        rounded_histogram.SetBinContent(bin, rounded_content)
        rounded_histogram.SetBinError(bin, 0)
    return rounded_histogram

def getSystString(systname) :
    if systname == "Central" : return ""
    elif "Syst_" in systname :
        return f"_{systname.replace('Syst_','')}"
    elif "Central_" in systname:
        return f"_{systname.replace('Central_','')}"