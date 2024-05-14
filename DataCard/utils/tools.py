import os

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

def getTauFakeNormalization(era,region) :
    try :
        return TauFakeNormalization[(era,region)]
    except KeyError :
        print(f"TauFakeNormalization not found for era: {era} and region: {region}, please run GetFakeNormalization.py to get the normalization factor.")
        sys.exit(1)

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