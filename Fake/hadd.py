import os
from datetime import datetime

savestr = datetime.now().strftime('%Y%m%d_%H%M%S')

for era in ["2017","2018"] :
    os.system(f"mkdir -p Inputs/{savestr}/{era}/Split")
    os.system(f"mkdir -p Inputs/{savestr}/{era}/Data")
    os.system(f"cp $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_* Inputs/{savestr}/{era}/Split")
    os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}_QCDOnly.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_QCD_Pt*")
    os.system(f"hadd Inputs/{savestr}/{era}/TauFake_{savestr}.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/WRTau_TauFake_SkimTree_LRSMTau_*")
    os.system(f"hadd Inputs/{savestr}/{era}/Data/TauFake_{savestr}.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/{era}/DATA/*")
