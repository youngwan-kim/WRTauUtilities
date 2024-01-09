import os
from datetime import datetime

savestr = datetime.now().strftime('%Y%m%d_%H%M%S')
#os.system(f"hadd TauFake_{savestr}_QCDOnly.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/2017/WRTau_TauFake_SkimTree_LRSMTau_QCD_Pt*")
os.system(f"hadd TauFake_{savestr}.root $SKFlatOutputDir/Run2UltraLegacy_v3/WRTau_TauFake/2017/WRTau_TauFake_SkimTree_LRSMTau_*")
