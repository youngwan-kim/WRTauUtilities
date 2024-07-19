#!/usr/bin/python3
import os
from datetime import datetime

savestr = datetime.now().strftime('%Y%m%d_%H%M%S')

for era in ["2016preVFP","2016postVFP","2017","2018"] :
    os.system(f"mkdir -p Inputs/{savestr}/{era}/Split")
    os.system(f"mkdir -p Inputs/{savestr}/{era}/Data")
    os.system(f"cp $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_* Inputs/{savestr}/{era}/Split")
    os.system(f"cp $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_TTLL_powheg.root Inputs/{savestr}/{era}/TauFake_{savestr}_TTLL.root")
    os.system(f"cp $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_TTLJ_powheg.root Inputs/{savestr}/{era}/TauFake_{savestr}_TTLJ.root")
    os.system(f"cp $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_TTJJ_powheg.root Inputs/{savestr}/{era}/TauFake_{savestr}_TTJJ.root")
    #os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}_QCDOnly.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_QCD_Pt*")
    #os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}_noDY.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/noDY__/WRTau_TauFake_SkimTree_LRSMTau_*")
    os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_*")
    os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}_TT.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_TT*")
    os.system(f"hadd Inputs/{savestr}/{era}/Data/TauFake_{savestr}.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/DATA/*")

os.system(f"mkdir -p Inputs/{savestr}/2016/Data")
os.system(f"hadd Inputs/{savestr}/2016/TauFake_{savestr}.root  Inputs/{savestr}/2016preVFP/TauFake_{savestr}.root Inputs/{savestr}/2016postVFP/TauFake_{savestr}.root ")
os.system(f"hadd Inputs/{savestr}/2016/Data/TauFake_{savestr}.root  Inputs/{savestr}/2016preVFP/Data/TauFake_{savestr}.root Inputs/{savestr}/2016postVFP/Data/TauFake_{savestr}.root ")
os.system(f"hadd Inputs/{savestr}/2016/Data/TauFake_{savestr}_TT.root  Inputs/{savestr}/2016preVFP/Data/TauFake_{savestr}_TT.root Inputs/{savestr}/2016postVFP/Data/TauFake_{savestr}_TT.root ")
os.system(f"hadd Inputs/{savestr}/2016/TauFake_{savestr}_noDY.root  Inputs/{savestr}/2016preVFP/TauFake_{savestr}_noDY.root Inputs/{savestr}/2016postVFP/TauFake_{savestr}_noDY.root ")