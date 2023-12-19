
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 5 -e 2017 --skim SkimTree_LRSMTau --userflags MassOpt,PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 5 -e 2017 --skim SkimTree_LRSMTau --userflags MassOpt,NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 5 -e 2017 --skim SkimTree_LRSMTau --userflags MassOpt,PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 5 -e 2017 --skim SkimTree_LRSMTau --userflags MassOpt,NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt  -n 5  -e 2017  --userflags MassOpt &