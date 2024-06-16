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
    ('2016preVFP','BoostedPreselection_ElTau') : 0.47007991190480414,
('2016preVFP','BoostedPreselection_MuTau') : 0.5187586108693739,
('2016preVFP','BoostedSignalRegionMETInvert_ElTau') : 0.44624839294201685,
('2016preVFP','BoostedSignalRegionMETInvert_MuTau') : 0.5042496989651002,
('2016preVFP','ResolvedSignalRegionMETInvert_ElTau') : 0.1883571411557831,
('2016preVFP','ResolvedSignalRegionMETInvert_MuTau') : 0.43909587221337104,
('2016preVFP','BoostedLowMassControlRegion_ElTau') : 0.441338095712019,
('2016preVFP','BoostedLowMassControlRegion_MuTau') : 0.49224402241032417,
('2016preVFP','ResolvedLowMassControlRegion_ElTau') : 0.18745936183533637,
('2016preVFP','ResolvedLowMassControlRegion_MuTau') : 0.4208241596074686,
('2016preVFP','ResolvedPreselection_ElTau') : 0.18232852809901254,
('2016preVFP','ResolvedPreselection_MuTau') : 0.4131021493988013,
('2016postVFP','BoostedPreselection_ElTau') : 0.4681890976035911,
('2016postVFP','BoostedPreselection_MuTau') : 0.5270725442334869,
('2016postVFP','BoostedSignalRegionMETInvert_ElTau') : 0.4737309432298713,
('2016postVFP','BoostedSignalRegionMETInvert_MuTau') : 0.5219814684771116,
('2016postVFP','ResolvedSignalRegionMETInvert_ElTau') : 0.3014894724490703,
('2016postVFP','ResolvedSignalRegionMETInvert_MuTau') : 0.43471187414365436,
('2016postVFP','BoostedLowMassControlRegion_ElTau') : 0.45405056897350937,
('2016postVFP','BoostedLowMassControlRegion_MuTau') : 0.48364311559357803,
('2016postVFP','ResolvedLowMassControlRegion_ElTau') : 0.22747811898157713,
('2016postVFP','ResolvedLowMassControlRegion_MuTau') : 0.41029063857839526,
('2016postVFP','ResolvedPreselection_ElTau') : 0.236029499373972,
('2016postVFP','ResolvedPreselection_MuTau') : 0.4067491990650641,
('2016','BoostedPreselection_ElTau') : 0.469183210518712,
('2016','BoostedPreselection_MuTau') : 0.5225602020388435,
('2016','BoostedSignalRegionMETInvert_ElTau') : 0.4591295711221127,
('2016','BoostedSignalRegionMETInvert_MuTau') : 0.5131249032335115,
('2016','ResolvedSignalRegionMETInvert_ElTau') : 0.247719183163669,
('2016','ResolvedSignalRegionMETInvert_MuTau') : 0.4371180517926956,
('2016','BoostedLowMassControlRegion_ElTau') : 0.4470814270358277,
('2016','BoostedLowMassControlRegion_MuTau') : 0.4880961651371059,
('2016','ResolvedLowMassControlRegion_ElTau') : 0.2074366120054506,
('2016','ResolvedLowMassControlRegion_MuTau') : 0.4160166425905767,
('2016','ResolvedPreselection_ElTau') : 0.20884322287841015,
('2016','ResolvedPreselection_MuTau') : 0.4101821260100116,
('2017','BoostedPreselection_ElTau') : 0.45381469294213084,
('2017','BoostedPreselection_MuTau') : 0.4226598064796522,
('2017','BoostedSignalRegionMETInvert_ElTau') : 0.4375062765853309,
('2017','BoostedSignalRegionMETInvert_MuTau') : 0.4568244061312007,
('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.2523670816488621,
('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.46853735711437094,
('2017','BoostedLowMassControlRegion_ElTau') : 0.44367768988326484,
('2017','BoostedLowMassControlRegion_MuTau') : 0.43717057919283037,
('2017','ResolvedLowMassControlRegion_ElTau') : 0.17983442837328156,
('2017','ResolvedLowMassControlRegion_MuTau') : 0.43873405322751585,
('2017','ResolvedPreselection_ElTau') : 0.17426591968880428,
('2017','ResolvedPreselection_MuTau') : 0.4180826421217039,
('2018','BoostedPreselection_ElTau') : 0.4559167238450597,
('2018','BoostedPreselection_MuTau') : 0.42308081099172856,
('2018','BoostedSignalRegionMETInvert_ElTau') : 0.45098531387311386,
('2018','BoostedSignalRegionMETInvert_MuTau') : 0.4556871218314583,
('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.25089369810675716,
('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.46328423728481016,
('2018','BoostedLowMassControlRegion_ElTau') : 0.4528815242419642,
('2018','BoostedLowMassControlRegion_MuTau') : 0.4165890246750598,
('2018','ResolvedLowMassControlRegion_ElTau') : 0.2103166350875158,
('2018','ResolvedLowMassControlRegion_MuTau') : 0.45210451968655896,
('2018','ResolvedPreselection_ElTau') : 0.2069811960629034,
('2018','ResolvedPreselection_MuTau') : 0.4458317641821596,
('Run2','BoostedPreselection_ElTau') : 0.4585985589890297,
('Run2','BoostedPreselection_MuTau') : 0.4464925820897482,
('Run2','BoostedSignalRegionMETInvert_ElTau') : 0.44939139625617547,
('Run2','BoostedSignalRegionMETInvert_MuTau') : 0.4717163933610445,
('Run2','ResolvedSignalRegionMETInvert_ElTau') : 0.2506696230868927,
('Run2','ResolvedSignalRegionMETInvert_MuTau') : 0.457840725899117,
('Run2','BoostedLowMassControlRegion_ElTau') : 0.44907512926541,
('Run2','BoostedLowMassControlRegion_MuTau') : 0.44184883047534546,
('Run2','ResolvedLowMassControlRegion_ElTau') : 0.20021401392711174,
('Run2','ResolvedLowMassControlRegion_MuTau') : 0.43868954881246786,
('Run2','ResolvedPreselection_ElTau') : 0.19717498182898052,
('Run2','ResolvedPreselection_MuTau') : 0.42842578295861283,

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
    elif era == "Run2" : return 0.016

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