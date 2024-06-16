#SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 10 -e 2017 --skim SkimTree_LRSMTau   --userflags 2DScan & 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2017.txt -n 1 -e 2017 --skim SkimTree_LRSMTau   --userflags 2DScan,Delta & 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal2DScan.txt -n 1 -e 2017   --userflags 2DScan,Delta  &
#SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 10 -e 2018 --skim SkimTree_LRSMTau   --userflags 2DScan & 
#SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2018.txt -n 10 -e 2018 --skim SkimTree_LRSMTau   --userflags 2DScan &
#SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 10 -e 2016a --skim SkimTree_LRSMTau  --userflags 2DScan & 
#SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2016a.txt -n 10 -e 2016a --skim SkimTree_LRSMTau --userflags 2DScan &
#SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 10 -e 2016b --skim SkimTree_LRSMTau  --userflags 2DScan & 
#SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2016b.txt -n 10 -e 2016b --skim SkimTree_LRSMTau --userflags 2DScan &