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
    
    ('2016','BoostedPreselection_ElTau') : 0.37439030284713637,
    ('2016','BoostedPreselection_MuTau') : 0.4087304330059199,
    ('2016','BoostedSignalRegionMETInvert_ElTau') : 0.3598411780196724,
    ('2016','BoostedSignalRegionMETInvert_MuTau') : 0.3880792241932713,
    ('2016','ResolvedSignalRegionMETInvert_ElTau') : 0.17146136685868768,
    ('2016','ResolvedSignalRegionMETInvert_MuTau') : 0.3623693563197689,
    ('2016','BoostedLowMassControlRegion_ElTau') : 0.348481737807039,
    ('2016','BoostedLowMassControlRegion_MuTau') : 0.3761263021779037,
    ('2016','ResolvedLowMassControlRegion_ElTau') : 0.12678444978433318,
    ('2016','ResolvedLowMassControlRegion_MuTau') : 0.3289719943353614,
    ('2016','ResolvedPreselection_ElTau') : 0.12434723747077665,
    ('2016','ResolvedPreselection_MuTau') : 0.3193621322324346,
    ('2016preVFP','BoostedPreselection_ElTau') : 0.37578667510934044,
    ('2016preVFP','BoostedPreselection_MuTau') : 0.40466190743947933,
    ('2016preVFP','BoostedSignalRegionMETInvert_ElTau') : 0.34835248222532345,
    ('2016preVFP','BoostedSignalRegionMETInvert_MuTau') : 0.3731794879638745,
    ('2016preVFP','ResolvedSignalRegionMETInvert_ElTau') : 0.11760992808887079,
    ('2016preVFP','ResolvedSignalRegionMETInvert_MuTau') : 0.3668005790305472,
    ('2016preVFP','BoostedLowMassControlRegion_ElTau') : 0.3436381250003045,
    ('2016preVFP','BoostedLowMassControlRegion_MuTau') : 0.3777860503480214,
    ('2016preVFP','ResolvedLowMassControlRegion_ElTau') : 0.10942258958520956,
    ('2016preVFP','ResolvedLowMassControlRegion_MuTau') : 0.3323381021167858,
    ('2016preVFP','ResolvedPreselection_ElTau') : 0.1016122795670169,
    ('2016preVFP','ResolvedPreselection_MuTau') : 0.3212141801294782,
    ('2016postVFP','BoostedPreselection_ElTau') : 0.372841891285584,
    ('2016postVFP','BoostedPreselection_MuTau') : 0.4135161434921839,
    ('2016postVFP','BoostedSignalRegionMETInvert_ElTau') : 0.37285742376248443,
    ('2016postVFP','BoostedSignalRegionMETInvert_MuTau') : 0.40231793539136,
    ('2016postVFP','ResolvedSignalRegionMETInvert_ElTau') : 0.2205829185707805,
    ('2016postVFP','ResolvedSignalRegionMETInvert_MuTau') : 0.35690993427280787,
    ('2016postVFP','BoostedLowMassControlRegion_ElTau') : 0.3543172000784769,
    ('2016postVFP','BoostedLowMassControlRegion_MuTau') : 0.3743621096790748,
    ('2016postVFP','ResolvedLowMassControlRegion_ElTau') : 0.14425342240811848,
    ('2016postVFP','ResolvedLowMassControlRegion_MuTau') : 0.3249381414064681,
    ('2016postVFP','ResolvedPreselection_ElTau') : 0.14773912143364126,
    ('2016postVFP','ResolvedPreselection_MuTau') : 0.3171814363264606,
    ('2017','BoostedPreselection_ElTau') : 0.39197936791377347,
    ('2017','BoostedPreselection_MuTau') : 0.3442879132913283,
    ('2017','BoostedSignalRegionMETInvert_ElTau') : 0.37913636911713716,
    ('2017','BoostedSignalRegionMETInvert_MuTau') : 0.3799897856320475,
    ('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.20842574736776365,
    ('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.4143404411007184,
    ('2017','BoostedLowMassControlRegion_ElTau') : 0.3845865610446934,
    ('2017','BoostedLowMassControlRegion_MuTau') : 0.36590791602639233,
    ('2017','ResolvedLowMassControlRegion_ElTau') : 0.1471216013247821,
    ('2017','ResolvedLowMassControlRegion_MuTau') : 0.37836663306192536,
    ('2017','ResolvedPreselection_ElTau') : 0.14188576301696848,
    ('2017','ResolvedPreselection_MuTau') : 0.36210723675764617,
    ('2018','BoostedPreselection_ElTau') : 0.3972511450440384,
    ('2018','BoostedPreselection_MuTau') : 0.3208968864261235,
    ('2018','BoostedSignalRegionMETInvert_ElTau') : 0.39036547346181805,
    ('2018','BoostedSignalRegionMETInvert_MuTau') : 0.3356080985885143,
    ('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.16067867559605223,
    ('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.37433394830549893,
    ('2018','BoostedLowMassControlRegion_ElTau') : 0.3901964454258573,
    ('2018','BoostedLowMassControlRegion_MuTau') : 0.3110879268930388,
    ('2018','ResolvedLowMassControlRegion_ElTau') : 0.5553174800295634,
    ('2018','ResolvedLowMassControlRegion_MuTau') : 0.35874334917524875,
    ('2018','ResolvedPreselection_ElTau') : 0.36895474506513515,
    ('2018','ResolvedPreselection_MuTau') : 0.3544318493298223,

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
    if "2016" in era : return 0.012
    elif era == "2017" : return 0.023
    elif era == "2018" : return 0.025

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