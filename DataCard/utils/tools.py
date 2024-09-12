import os
from ROOT import *

rebins = [0,50,100,150,200,250,300,350,400,500,600,700,800,900,1000,1250,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500]
rebins = [900,950,1000,1050,1100,1150,1200,1300,1400,1500,1600,1750,2000,3000,5000,8500]
#rebins = [900,1000,1250,1500,2000,3000,5000,8000]
#rebins = [900,1500,2000,3000,4000,5000,6000,7000,8000]
#rebins = [900,1200,1700,3000,5000,8000]
#rebins = [900,1000,1100,1300,1500,1700,3000,5000,8000]
rebins_LMCR = [0,25,50,75,100,150,200,250,300,350,400,450,550,650,750,850,950]
#rebins_LMCR = [0,500,750,900]
rebins_LMCR = [0,400,600,800]
rebins_QCDMR = [900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2400,2600,3000]
rebins_QCDMR = [1200,1400,1600,2500]


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

d_mass_2018 = { }

for key in range(1000,6501,500) :
    d_mass_2018[key] = list(range(100,key,100))


def getXsec(mWR,mN) :
    with open(f"/data9/Users/youngwan/work/SKFlatAnalyzer_Sandbox/WRTauUtilities/Data/xsec_new.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])

def GetPDFUnc(mwr,mn,tag,era) : 
    data_dict = {}
    with open(f"XsecSyst/{tag}/{era}/PDFerr.txt", 'r') as file:
        for line in file:
            line = line.strip()
            a, b, c = line.split(',')
            data_dict[(int(a), int(b))] = float(c)
    return data_dict.get((mwr,mn),"-")


def GetSignalScale(mwr) :
    signal_scale = 1.0
    if mwr < 800.1 : signal_scale *= 0.1; 
    elif mwr < 3600.1 : signal_scale *= 50
    else : signal_scale *= 500
    return signal_scale

def GetDirList(file) :
    dirlist = []
    for key in file.GetListOfKeys() :
        obj = key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            dirName = obj.GetName()
            dirlist.append(dirName)
    return dirlist


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
        rounded_content = int(ceil(bin_content))
        rounded_histogram.SetBinContent(bin, rounded_content)
        rounded_histogram.SetBinError(bin, 0)
    return rounded_histogram

def getSystString(systname) :
    if systname == "Central" : return ""
    elif "Syst_" in systname :
        return f"_{systname.replace('Syst_','')}"
    elif "Central_" in systname:
        return f"_{systname.replace('Central_','')}"
    else : return systname

def GetLumi(era) :
    if era == "2016preVFP" : return 19.5
    elif era == "2016postVFP" : return 16.8
    elif era == "2016" : return 36.3
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8
    elif era == "Run2" : return 138

 
def GetEnvelope(d_histograms,central, upper_name="upper_envelope", upper_title="Upper Envelope Histogram",
                               lower_name="lower_envelope", lower_title="Lower Envelope Histogram"):

    if not d_histograms:
        raise ValueError("The dictionary of histograms is empty. Provide at least one histogram.")
    l_central = []
    for i in range(1,central.GetNbinsX()+1) : l_central.append(central.GetBinContent(i))
    n_bins = len(l_central)
    upper_envelope_hist = central.Clone(upper_name)
    lower_envelope_hist = central.Clone(lower_name)
    for h in [upper_envelope_hist,lower_envelope_hist] :
        for i in range(1,n_bins+1) :
            h.SetBinContent(i,0)

    for bin_index in range(1, n_bins + 1):
        bin_central = central.GetBinContent(bin_index)
        binmax = bin_central
        binmin = bin_central
        
        for var in d_histograms : 
            binmax = max(binmax, d_histograms[var][bin_index-1] )
            binmin = min(binmin, d_histograms[var][bin_index-1] )

        #print(bin_index,binmax,bin_central,binmin)
        upper_envelope_hist.SetBinContent(bin_index, binmax)
        lower_envelope_hist.SetBinContent(bin_index, binmin)

    return [upper_envelope_hist, lower_envelope_hist]

def SaveEnvelope(output_file, upper_hist, lower_hist, dir1, dir2):

    dir1_obj = output_file.mkdir(dir1)
    dir1_obj.cd()
    dir2_obj = dir1_obj.mkdir(dir2)
    dir2_obj.cd()

    # Write histograms to the specified directory
    upper_hist.Write()
    lower_hist.Write()

    # Close the ROOT file
    output_file.Close()