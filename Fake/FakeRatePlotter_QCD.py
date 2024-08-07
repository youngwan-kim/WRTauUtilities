from ROOT import *
from utils import *
import array,os

stamp = "20240805_150737"
filename = f"TauFake_{stamp}"
savestr = filename.split("_",1)[1]
#f_fake = TFile(f"Inputs/{stamp}/{filename}.root")

c = TCanvas("","",1000,1000)


d_ptbins = {

    "tag"                                : "TailFatBinning",
    "Inclusive_2017"                     : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "BoostedSignalRegionMETInvert_2017"  : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "ResolvedSignalRegionMETInvert_2017" : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "Inclusive_2018"                     : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "BoostedSignalRegionMETInvert_2018"  : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "ResolvedSignalRegionMETInvert_2018" : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100))


}


ptbins  = {

    '0' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,190,230,270,310,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,200,300,400,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,190,230,300,400,500,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,190,230,270,310,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,200,300,400,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,190,230,300,400,500,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,190,230,270,310,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,200,250,300,800],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,200,300,400,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,190,230,300,400,500,700,1000],
    "InclusiveQCDMR_2017"                                           : [0,190,250,350,500,1000],
    "InclusiveQCDMR_2018"                                           : [0,190,220,250,350,1000],
    },
    '1' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       :  [0,190,230,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      :  [0,190,230,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "InclusiveQCDMR_2016"                                           :  [0,150,190,300,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "InclusiveQCDMR_2016preVFP"                                     :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "InclusiveQCDMR_2016postVFP"                                    :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "InclusiveQCDMR_2017"                                           :  [0,190,270,350,400,500,1000],
    "InclusiveQCDMR_2018"                                           :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],

    },
    '10' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,300,350,450,550,1000], 
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000], 
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000], 
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,300,350,450,1000], 
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,300,350,450,550,1000], 
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,300,350,450,550,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,300,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,300,350,450,550,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,230,300,450,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "InclusiveQCDMR_2017"                                           : [0,190,230,300,350,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,230,300,400,1000],
    },
    '11' : {
    "tag"                                                             : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "InclusiveQCDMR_2017"                                           : [0,190,250,300,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,230,275,350,400,1000],
    },
    # inclusive DMs 
    '1prong' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       :  [0,190,230,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      :  [0,190,230,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "InclusiveQCDMR_2016"                                           :  [0,150,190,300,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "InclusiveQCDMR_2016preVFP"                                     :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "InclusiveQCDMR_2016postVFP"                                    :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "InclusiveQCDMR_2017"                                           :  [0,190,270,350,400,500,1000],
    "InclusiveQCDMR_2018"                                           :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    },
    '3prong' : {
    "tag"                                                             : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "InclusiveQCDMR_2017"                                           : [0,190,250,300,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,230,275,350,400,1000],
    },
}


ptbins_same  = {

    '0' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,190,230,270,310,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,200,300,400,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,190,230,300,400,500,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,190,230,270,310,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,200,300,400,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,190,230,300,400,500,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,190,230,270,310,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,190,230,270,310,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,250,300,800],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,190,250,300,800],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,190,250,300,800],
    "InclusiveQCDMR_2017"                                           : [0,150,190,250,300,800],
    "InclusiveQCDMR_2018"                                           : [0,150,190,250,300,800],
    },
    '1' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       :  [0,190,230,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      :  [0,190,230,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "InclusiveQCDMR_2016"                                           :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2016preVFP"                                     :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2016postVFP"                                    :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2017"                                           :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2018"                                           :  [0,150,190,300,400,500,1000],

    },
    '10' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,300,350,450,550,1000], 
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000], 
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000], 
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,300,350,450,1000], 
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,300,350,450,550,1000], 
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,300,350,450,550,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,300,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,300,350,450,550,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,230,300,450,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,190,230,300,450,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,190,230,300,450,1000],
    "InclusiveQCDMR_2017"                                           : [0,150,190,230,300,450,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,230,300,450,1000],
    },
    '11' : {
    "tag"                                                             : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2017"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,275,375,1000],
    },
    # inclusive DMs 
    '1prong' : {
    "tag"                                                           : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       :  [0,190,230,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                :  [0,150,190,230,300,350,400,500,1000],#[0,150,190,230,270,350,450,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               :  [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      :  [0,190,230,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      :  [0,150,190,230,300,350,400,500,1000],#[0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,1000],
    "InclusiveQCDMR_2016"                                           :  [0,150,190,300,400,500,1000],#[0,150,180,210,250,350,450,550,700,1000],
    "InclusiveQCDMR_2016preVFP"                                     :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2016postVFP"                                    :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2017"                                           :  [0,150,190,300,400,500,1000],
    "InclusiveQCDMR_2018"                                           :  [0,150,190,300,400,500,1000],
    },
    '3prong' : {
    "tag"                                                             : "QCD",
    "BoostedSignalRegionMETInvertMTSame_2016"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "BoostedSignalRegionMETInvertMTSame_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "BoostedSignalRegionMETInvertMTSame_2017"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"                       : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016preVFP"                : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "ResolvedSignalRegionMETInvertMTSame_2016postVFP"               : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "ResolvedSignalRegionMETInvertMTSame_2017"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"                      : [0,150,170,190,210,230,250,275,300,350,400,500,1000],
    "InclusiveQCDMR_2016"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016preVFP"                                     : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2016postVFP"                                    : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2017"                                           : [0,150,190,275,375,1000],
    "InclusiveQCDMR_2018"                                           : [0,150,190,275,375,1000],
    },
}


# [0,190,210,230,250,270,320,800] 
d_ptbins_PR = {

    "tag"                                      : "BinOptv2_FlavourSplit",
    "Inclusive_2016"                           : [0,190,220,250,350,1000],
    "Inclusive_2017"                           : [0,190,220,250,350,1000],
    "Inclusive_2018"                           : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2018"                     : [0,190,220,250,350,1000], 
    "Inclusive_MuTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2018"                     : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2016"        : [0,150,250,1000], 
    "ResolvedSignalRegionMETInvertMTSame_2016"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2017"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_2017"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"       : [0,190,220,250,350,1000],
    ####
    "BoostedSignalRegionMETInvertMTSame_ElTau_2016"  : [0,150,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2016" : [0,150,250,1000],
    "BoostedSignalRegionMETInvertMTSame_ElTau_2017"  : [0,190,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2017" : [0,190,350,1000],
    "BoostedSignalRegionMETInvertMTSame_ElTau_2018"  : [0,190,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2018" : [0,190,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2016"  : [0,150,300,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2016" : [0,150,200,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2017"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2017" : [0,190,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2018"  : [0,190,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2018" : [0,190,220,250,350,1000],
    ####

}

savestr += f"_{d_ptbins['tag']}"

l_subtract = ["Subtract"]



l_subtract = ["NonSubtract"]
l_subtract = ["Subtract"]

isnoDY = False
dytag = ""
if isnoDY : dytag = "_noDY"

for era in ["2016","2017","2018"]:
    k = 0
    os.system(f"mkdir -p Plots/{savestr}{dytag}/{era}")
    os.system(f"mkdir -p Files/{savestr}{dytag}")
    for genmatch in ["Data"]:
    #for genmatch in ["Prompt"]: # Switch for prompt rate 
        output_file = TFile(f"Files/{savestr}{dytag}/{era}_{genmatch}.root", "RECREATE")
        isDataDriven = genmatch == "Data"
        isPromptRate = genmatch == "Prompt"
        os.system(f"mkdir -p Plots/{savestr}{dytag}/{era}/Prompt")
        f_fake = TFile(f"Inputs/{stamp}/{era}/{filename}{dytag}.root")
        if isDataDriven : 
            f_fake   = TFile(f"Inputs/{stamp}/{era}/Data/{filename}.root")
            f_prompt = TFile(f"Inputs/{stamp}/{era}/{filename}{dytag}.root")
        for eta in d_geoTag :
            for DM in d_DMtag :
                d_ptbins = ptbins_same[DM]
                for lep in [""] : #["","_ElTau","_MuTau"]
                    for i,r in enumerate([ "InclusiveQCDMR"]) : #["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]
                        if isPromptRate : d_ptbins = d_ptbins_PR
                        #print(d_ptbins)
                        c = TCanvas("","",1000,1000)
                        h_loose_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Loose_{eta}_DM{DM}")
                        if h_loose_tmp :
                            h_loose = h_loose_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"loose{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_loose.SetDirectory(0)
                            #print(h_loose)
                        h_tight_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Tight_{eta}_DM{DM}")
                        if h_tight_tmp :
                            h_tight = h_tight_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"tight{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_tight.SetDirectory(0)
                        if isDataDriven : 
                            h_loose_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}{lep}/Prompt/TauPt_Loose_{eta}_DM{DM}")
                            if h_loose_prompt_tmp :
                                h_loose_prompt = h_loose_prompt_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"ddps_loose{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                                h_loose_prompt.SetDirectory(0)
                            h_tight_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}{lep}/Prompt/TauPt_Tight_{eta}_DM{DM}")
                            if h_tight_prompt_tmp :
                                h_tight_prompt = h_tight_prompt_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"ddps_tight{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                                h_tight_prompt.SetDirectory(0)
                            for i in range(1,h_loose_prompt.GetNbinsX()+1) :
                                print(f"{i} : {h_loose.GetBinContent(i)}-{h_loose_prompt.GetBinContent(i)} = {h_loose.GetBinContent(i)-h_loose_prompt.GetBinContent(i)}")
                                print(f"{i} : {h_tight.GetBinContent(i)}-{h_tight_prompt.GetBinContent(i)} = {h_tight.GetBinContent(i)-h_tight_prompt.GetBinContent(i)}")
                            h_loose = h_loose - h_loose_prompt 
                            h_tight = h_tight - h_tight_prompt
                        for i in range(0,h_loose.GetNbinsX()+1) :
                            if h_loose.GetBinContent(i) < 0 : h_loose.SetBinContent(i,0)
                        for i in range(0,h_tight.GetNbinsX()+1) :
                            if h_tight.GetBinContent(i) < 0 : h_tight.SetBinContent(i,0)
                        for i in range(1,h_loose_prompt.GetNbinsX()+1) :
                                print(f"{i}New : {h_loose.GetBinContent(i)} ")
                                print(f"{i}New : {h_tight.GetBinContent(i)} ")
                        h_fr = h_tight.Clone(f"{r}{lep}_{d_genmatch[genmatch]}{l_subtract[k]}_{eta}_DM{DM}")
                        h_fr.Divide(h_tight,h_loose,1,1,'B')
                        original_directory = gDirectory.GetPath()
                        output_file.cd()
                        h_fr.Write()
                        gDirectory.cd(original_directory)
                        if DM == "10" or DM == "11" or "prong" in DM : h_fr.GetYaxis().SetRangeUser(0,0.5)
                        else : h_fr.GetYaxis().SetRangeUser(0,1.0)
                        h_fr.SetStats(0)
                        h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
                        h_fr.GetYaxis().SetTitleSize(0.05)
                        h_fr.GetYaxis().SetTitle(d_genmatch[genmatch]+"(#tau_{h})")
                        h_fr.GetYaxis().SetTitle("FF(#tau_{h})")
                        h_fr.GetYaxis().SetTitleOffset(0.9)
                        h_fr.GetXaxis().SetNdivisions(509)
                        h_fr.SetLineColor(kRed)
                        h_fr.SetLineWidth(3)
                        h_fr.GetXaxis().SetTitleSize(0.05)
                        h_err = h_fr.Clone(f"{r}_FF_err")
                        h_err.SetLineWidth(2)
                        h_err.SetLineColor(kBlack)

                        c.cd()
                        c.SetLeftMargin(0.125)
                        c.SetRightMargin(0.085)
                        c.SetBottomMargin(0.125)
                        #h_fr.Draw("hist")
                        h_err.Draw("e0")
                        h_fr.Draw("hist&same")
                        drawLatex(r,era,genmatch)
                        drawTagLatexDM(eta,DM)
                        c.Update()
                        if isPromptRate :
                            line = TLine(0,1,1000,1)
                            line.SetLineStyle(3)
                            line.SetLineWidth(2)
                            line.Draw("same")
                            c.Update()
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Prompt/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_DM{DM}.png")
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Prompt/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_DM{DM}.pdf")
                        else :
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_DM{DM}.png")
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_DM{DM}.pdf")
        k += 1
    output_file.Close()