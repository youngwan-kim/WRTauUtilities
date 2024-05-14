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
    
    ('2016preVFP','BoostedPreselection_ElTau') : 0.4109206606539493,
    ('2016preVFP','BoostedPreselection_MuTau') : 0.45399972364805075,
    ('2016preVFP','BoostedSignalRegionMETInvert_ElTau') : 0.38582439721995165,
    ('2016preVFP','BoostedSignalRegionMETInvert_MuTau') : 0.4489169303371895,
    ('2016preVFP','ResolvedSignalRegionMETInvert_ElTau') : 0.16796563780509574,
    ('2016preVFP','ResolvedSignalRegionMETInvert_MuTau') : 0.405679272433424,
    ('2016preVFP','BoostedLowMassControlRegion_ElTau') : 0.3837324562755691,
    ('2016preVFP','BoostedLowMassControlRegion_MuTau') : 0.4374434300756542,
    ('2016preVFP','ResolvedLowMassControlRegion_ElTau') : 0.16780468886546737,
    ('2016preVFP','ResolvedLowMassControlRegion_MuTau') : 0.38953559312886804,
    ('2016preVFP','ResolvedPreselection_ElTau') : 0.16343320116681523,
    ('2016preVFP','ResolvedPreselection_MuTau') : 0.3816223915784582,
    ('2016','BoostedPreselection_ElTau') : 0.4101803928754543,
    ('2016','BoostedPreselection_MuTau') : 0.4554350381607087,
    ('2016','BoostedSignalRegionMETInvert_ElTau') : 0.3968658388123804,
    ('2016','BoostedSignalRegionMETInvert_MuTau') : 0.456014345595277,
    ('2016','ResolvedSignalRegionMETInvert_ElTau') : 0.22171297427688114,
    ('2016','ResolvedSignalRegionMETInvert_MuTau') : 0.4034257251052594,
    ('2016','BoostedLowMassControlRegion_ElTau') : 0.3874682433307977,
    ('2016','BoostedLowMassControlRegion_MuTau') : 0.43240086109758036,
    ('2016','ResolvedLowMassControlRegion_ElTau') : 0.18595981105081155,
    ('2016','ResolvedLowMassControlRegion_MuTau') : 0.38494714046686435,
    ('2016','ResolvedPreselection_ElTau') : 0.18752101237502888,
    ('2016','ResolvedPreselection_MuTau') : 0.3791914186206863,
    ('2017','BoostedPreselection_ElTau') : 0.4234202422949218,
    ('2017','BoostedPreselection_MuTau') : 0.3725625418817358,
    ('2017','BoostedSignalRegionMETInvert_ElTau') : 0.40952811445825116,
    ('2017','BoostedSignalRegionMETInvert_MuTau') : 0.41472781380161894,
    ('2017','ResolvedSignalRegionMETInvert_ElTau') : 0.22605536624033817,
    ('2017','ResolvedSignalRegionMETInvert_MuTau') : 0.43847526787288615,
    ('2017','BoostedLowMassControlRegion_ElTau') : 0.4156089171029557,
    ('2017','BoostedLowMassControlRegion_MuTau') : 0.3960705278898729,
    ('2017','ResolvedLowMassControlRegion_ElTau') : 0.1603284122692651,
    ('2017','ResolvedLowMassControlRegion_MuTau') : 0.41181212153510766,
    ('2017','ResolvedPreselection_ElTau') : 0.15503841620938938,
    ('2017','ResolvedPreselection_MuTau') : 0.39224896474102955,
    ('2018','BoostedPreselection_ElTau') : 0.4343381009644576,
    ('2018','BoostedPreselection_MuTau') : 0.36025765747930083,
    ('2018','BoostedSignalRegionMETInvert_ElTau') : 0.4317492864978111,
    ('2018','BoostedSignalRegionMETInvert_MuTau') : 0.40211038184471465,
    ('2018','ResolvedSignalRegionMETInvert_ElTau') : 0.2048265633471517,
    ('2018','ResolvedSignalRegionMETInvert_MuTau') : 0.43569430253140495,
    ('2018','BoostedLowMassControlRegion_ElTau') : 0.433022914832584,
    ('2018','BoostedLowMassControlRegion_MuTau') : 0.36550762598460584,
    ('2018','ResolvedLowMassControlRegion_ElTau') : 0.7912957403868537,
    ('2018','ResolvedLowMassControlRegion_MuTau') : 0.4259524279525509,
    ('2018','ResolvedPreselection_ElTau') : 0.5361278360358765,
    ('2018','ResolvedPreselection_MuTau') : 0.42017845810282456,
    ('Run2','BoostedPreselection_ElTau') : 0.43253431733509073,
    ('Run2','BoostedPreselection_MuTau') : 0.4063785650512304,
    ('Run2','BoostedSignalRegionMETInvert_ElTau') : 0.425332521156842,
    ('Run2','BoostedSignalRegionMETInvert_MuTau') : 0.4336137657906123,
    ('Run2','ResolvedSignalRegionMETInvert_ElTau') : 0.2279600779670774,
    ('Run2','ResolvedSignalRegionMETInvert_MuTau') : 0.43078511731143926,
    ('Run2','BoostedLowMassControlRegion_ElTau') : 0.425169727304131,
    ('Run2','BoostedLowMassControlRegion_MuTau') : 0.405917001000798,
    ('Run2','ResolvedLowMassControlRegion_ElTau') : 0.18188377129187216,
    ('Run2','ResolvedLowMassControlRegion_MuTau') : 0.4138477632084051,
    ('Run2','ResolvedPreselection_ElTau') : 0.17904170340907347,
    ('Run2','ResolvedPreselection_MuTau') : 0.40418489762351734,
    ('Run2','BoostedSignalRegion_ElTau') : 0.12635104781103595,
    ('Run2','BoostedSignalRegion_MuTau') : 0.46412721920441957,
    ('Run2','ResolvedSignalRegion_ElTau') : 0.04059193222733745,
    ('Run2','ResolvedSignalRegion_MuTau') : 0.0978106947445519,

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