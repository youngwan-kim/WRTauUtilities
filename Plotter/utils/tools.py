from ROOT import *
import array,os,csv,ast
'''
    ('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.34826005735242965,
    ('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.3471670198150653,
    ('2017','ResolvedLowMassControlRegion_ElTau') : 0.26096435625347075,
    ('2017','ResolvedLowMassControlRegion_MuTau') : 0.3217447095654813,
    ('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.288313463123838,
    ('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.3221694463927444,
    ('2018','ResolvedLowMassControlRegion_ElTau') : 0.22806902170014795,
    ('2018','ResolvedLowMassControlRegion_MuTau') : 0.31508093681590654,
    ('2017','BoostedSignalRegionMETInvert_ElTau') : 0.34557918945174776,
    ('2017','BoostedSignalRegionMETInvert_MuTau') : 0.3589339792716537,
    ('2017','BoostedLowMassControlRegion_ElTau') : 0.3607174623641672,
    ('2017','BoostedLowMassControlRegion_MuTau') : 0.36244758931233484,
    ('2018','BoostedSignalRegionMETInvert_ElTau') : 0.37360891610788216,
    ('2018','BoostedSignalRegionMETInvert_MuTau') : 0.3655419157745017,
    ('2018','BoostedLowMassControlRegion_ElTau') : 0.3699993121131814,
    ('2018','BoostedLowMassControlRegion_MuTau') : 0.33605294137356523,
    ('2017','BoostedPreselection_ElTau') : 0.42800555379182303,
    ('2017','BoostedPreselection_MuTau') : 0.32900288935258964,
    ('2017','ResolvedPreselection_ElTau') : 0.25864310778527433,
    ('2017','ResolvedPreselection_MuTau') : 0.3113008371859891,
    ('2018','BoostedPreselection_ElTau') : 0.4032652539564126,
    ('2018','BoostedPreselection_MuTau') : 0.3424372774925394,
    ('2018','ResolvedPreselection_ElTau') : 0.2299782941843531,
    ('2018','ResolvedPreselection_MuTau') : 0.31623359680901664,
'''
TauFakeNormalization = {
    
    ('2017','BoostedPreselection_ElTau') : 0.4658717604959658,
    ('2017','BoostedPreselection_MuTau') : 0.3804986566397224,
    ('2017','BoostedSignalRegionMETInvert_ElTau') : 0.4211360327312417,
    ('2017','BoostedSignalRegionMETInvert_MuTau') : 0.42053892629328193,
    ('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.23916129092035185,
    ('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.4561751944523736,
    ('2017','BoostedLowMassControlRegion_ElTau') : 0.4269722147396055,
    ('2017','BoostedLowMassControlRegion_MuTau') : 0.40733897117593837,
    ('2017','ResolvedLowMassControlRegion_ElTau') : 0.17191315442278235,
    ('2017','ResolvedLowMassControlRegion_MuTau') : 0.418617377737751,
    ('2017','ResolvedPreselection_ElTau') : 0.16750420998618412,
    ('2017','ResolvedPreselection_MuTau') : 0.40321237500162643,
    ('2018','BoostedPreselection_ElTau') : 0.43105289924447426,
    ('2018','BoostedPreselection_MuTau') : 0.35178350215510384,
    ('2018','BoostedSignalRegionMETInvert_ElTau') : 0.42546312092316263,
    ('2018','BoostedSignalRegionMETInvert_MuTau') : 0.3733482573022401,
    ('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.18545433867360892,
    ('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.4133219654807545,
    ('2018','BoostedLowMassControlRegion_ElTau') : 0.42583530535427183,
    ('2018','BoostedLowMassControlRegion_MuTau') : 0.3475888446058985,
    ('2018','ResolvedLowMassControlRegion_ElTau') : 0.6727153972718998,
    ('2018','ResolvedLowMassControlRegion_MuTau') : 0.4006129679624432,
    ('2018','ResolvedPreselection_ElTau') : 0.45091177661911946,
    ('2018','ResolvedPreselection_MuTau') : 0.39703099187682395,
    
}

TauFakeNormalization_deg3 = {

    ('2017','BoostedPreselection_ElTau') : 0.46592036858180025,
    ('2017','BoostedPreselection_MuTau') : 0.3554593106577844,
    ('2017','BoostedSignalRegionMETInvert_ElTau') : 0.4212920132728149,
    ('2017','BoostedSignalRegionMETInvert_MuTau') : 0.4039022358953992,
    ('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.23787755007013892,
    ('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.4564052348980672,
    ('2017','BoostedLowMassControlRegion_ElTau') : 0.42707040334141805,
    ('2017','BoostedLowMassControlRegion_MuTau') : 0.39620253566958136,
    ('2017','ResolvedLowMassControlRegion_ElTau') : 0.17095703741161186,
    ('2017','ResolvedLowMassControlRegion_MuTau') : 0.41883467942790703,
    ('2017','ResolvedPreselection_ElTau') : 0.16663935543400737,
    ('2017','ResolvedPreselection_MuTau') : 0.4034322134173208,
    ('2018','BoostedPreselection_ElTau') : 0.43133611060780186,
    ('2018','BoostedPreselection_MuTau') : 0.3550750136263229,
    ('2018','BoostedSignalRegionMETInvert_ElTau') : 0.42584612932586735,
    ('2018','BoostedSignalRegionMETInvert_MuTau') : 0.37268818834218975,
    ('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.17546813563845526,
    ('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.41184552820790477,
    ('2018','BoostedLowMassControlRegion_ElTau') : 0.4263281187122643,
    ('2018','BoostedLowMassControlRegion_MuTau') : 0.34706477453031637,
    ('2018','ResolvedLowMassControlRegion_ElTau') : 0.14646263616480248,
    ('2018','ResolvedLowMassControlRegion_MuTau') : 0.3992453258038852,
    ('2018','ResolvedPreselection_ElTau') : 0.14832647441569047,
    ('2018','ResolvedPreselection_MuTau') : 0.3956983014897407,

}

def center_histogram(h1):

    h_out = h.Clone("h_centerror")

    # Get the number of bins in the original histogram
    num_bins = h_out.GetNbinsX()

    # Loop over the bins of the new histogram and set content to 1.0
    for i in range(1, num_bins + 1):
        h_out.SetBinContent(i, 1.0)

    return h_out

def getLumiSyst(era) :
    if era == "2016preVFP" or era == "2016postVFP" : return 0.025
    elif era == "2017" : return 0.02
    elif era == "2018" : return 0.015

def getXsec(mWR,mN) :
    with open(f"{os.getenv('WRTau_Data')}/xsec.csv") as f:
        for line in f :
            if mWR == float(line.split(",")[0]) and mN == float(line.split(",")[1]) : 
                return float(line.split(",")[2])


def getNormalization(era,mwr,mn) :
    return getLumi(str(era))/getXsec(mwr,mn) 


def remove_keys_containing_strings(dic, strings_to_remove):
    keys_to_remove = []

    for key in dic.keys():
        for string in strings_to_remove:
            if string in key:
                keys_to_remove.append(key)
                break
    
    for key in keys_to_remove:
        dic.pop(key)
    
    return dic

def getTauFakeNormalization(era,region) :
    try :
        return TauFakeNormalization[(era,region)]
    except KeyError :
        print(f"TauFakeNormalization not found for era: {era} and region: {region}, please run GetFakeNormalization.py to get the normalization factor.")
        sys.exit(1)


def getLumi(era) :
    if era == "2016preVFP" : return 19.5
    elif era == "2016postVFP" : return 16.8
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8

def LeptonString(region) :
    if "ElTau" in region : return "e"
    elif "MuTau" in region : return "#mu"
    else : return "e,#mu"

def LeptonString_Explicit(region) :
    if "ElTau" in region : return "Electron"
    elif "MuTau" in region : return "Muon"
    else : return "Lepton"


def csv2dict(filename,region):
    result_dict = {}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row and not row[0].startswith("#"):  # Skip lines starting with "#"
                key = f"{region}/{row[0]}"
                if len(row[1:]) == 8 :
                    rebinning = str(row[1:][6]).replace("/",",")
                    values = [bool(row[1:][0]),int(row[1:][1]),str(row[1:][2]),str(row[1:][3]),
                              float(row[1:][4]),float(row[1:][5]),ast.literal_eval(rebinning),bool(row[1:][7])]
                elif len(row[1:]) == 6 :
                    values = [bool(row[1:][0]),int(row[1:][1]),str(row[1:][2]),str(row[1:][3]),
                              float(row[1:][4]),float(row[1:][5])]
                result_dict[key] = values
    return result_dict


def GetRegionList(path):
    region_list = []

    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        return region_list

    for subdir in os.listdir(path):
        subdir_path = os.path.join(path, subdir)
        
        if os.path.isdir(subdir_path):
            hists_csv_path = os.path.join(subdir_path, 'hists.csv')
            
            if os.path.isfile(hists_csv_path) and os.path.getsize(hists_csv_path) > 0:
                region_list.append(subdir)
    
    return region_list

def GerVarDic(era,region):
    return csv2dict()