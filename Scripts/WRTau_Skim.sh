SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 15 -e 2017 --skim SkimTree_LRSMTau & 
SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 15 -e 2017 --skim SkimTree_LRSMTau --userflags TauFake & 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2017.txt -n 10 -e 2017 --skim SkimTree_LRSMTau &
SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 15 -e 2018 --skim SkimTree_LRSMTau & 
SKFlat.py -a WRTau_Analyzer  -i Tau                               -n 15 -e 2018 --skim SkimTree_LRSMTau --userflags TauFake & 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2018.txt -n 10 -e 2018 --skim SkimTree_LRSMTau &
