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
    ('2016preVFP','BoostedSignalRegionMETInvertMTSame_ElTau') : 0.4631410733436301,
('2016preVFP','BoostedSignalRegionMETInvertMTSame_MuTau') : 0.1496545474143908,
('2016preVFP','ResolvedSignalRegionMETInvertMTSame_ElTau') : 0.1882185474833002,
('2016preVFP','ResolvedSignalRegionMETInvertMTSame_MuTau') : 0.4445967092239198,
('2016preVFP','BoostedLowMassControlRegion_ElTau') : 0.5103835015641703,
('2016preVFP','BoostedLowMassControlRegion_MuTau') : 0.5667438948838599,
('2016preVFP','ResolvedLowMassControlRegion_ElTau') : 0.12426428947550901,
('2016preVFP','ResolvedLowMassControlRegion_MuTau') : 0.31812907062677437,
('2016postVFP','BoostedSignalRegionMETInvertMTSame_ElTau') : 0.49837948240374574,
('2016postVFP','BoostedSignalRegionMETInvertMTSame_MuTau') : 0.44156676413310525,
('2016postVFP','ResolvedSignalRegionMETInvertMTSame_ElTau') : 0.27610165420453736,
('2016postVFP','ResolvedSignalRegionMETInvertMTSame_MuTau') : 0.44724573924146915,
('2016postVFP','BoostedLowMassControlRegion_ElTau') : 0.5203134599843624,
('2016postVFP','BoostedLowMassControlRegion_MuTau') : 0.5729863239742667,
('2016postVFP','ResolvedLowMassControlRegion_ElTau') : 0.22936318776398867,
('2016postVFP','ResolvedLowMassControlRegion_MuTau') : 0.3095801987282328,
('2017','BoostedSignalRegionMETInvertMTSame_ElTau') : 0.5006126805248111,
('2017','BoostedSignalRegionMETInvertMTSame_MuTau') : 0.5843472290539367,
('2017','ResolvedSignalRegionMETInvertMTSame_ElTau') : 0.3610190877105149,
('2017','ResolvedSignalRegionMETInvertMTSame_MuTau') : 0.49999333286537895,
('2017','BoostedLowMassControlRegion_ElTau') : 0.4832573816299416,
('2017','BoostedLowMassControlRegion_MuTau') : 0.6046402618524856,
('2017','ResolvedLowMassControlRegion_ElTau') : 0.257063712373197,
('2017','ResolvedLowMassControlRegion_MuTau') : 0.49990865325620004,
('2018','BoostedSignalRegionMETInvertMTSame_ElTau') : 0.4778310628522663,
('2018','BoostedSignalRegionMETInvertMTSame_MuTau') : 0.40230058410208197,
('2018','ResolvedSignalRegionMETInvertMTSame_ElTau') : 0.2941642560234192,
('2018','ResolvedSignalRegionMETInvertMTSame_MuTau') : 0.47947186745894743,
('2018','BoostedLowMassControlRegion_ElTau') : 0.4723619333283279,
('2018','BoostedLowMassControlRegion_MuTau') : 0.3683248055941307,
('2018','ResolvedLowMassControlRegion_ElTau') : 0.2371718311656036,
('2018','ResolvedLowMassControlRegion_MuTau') : 0.4176870918083577,
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
    if "2016" in era : return 1.012
    elif era == "2017" : return 1.023
    elif era == "2018" : return 1.025
    elif era == "Run2" : return 1.016

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
    elif era == "2016" : return 36.3
    elif era == "2017" : return 41.5
    elif era == "2018" : return 59.8
    elif era == "Run2" : return 138

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