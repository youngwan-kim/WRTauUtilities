
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 15 -e 2017 --userflags LSFOpt,PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 15 -e 2017 --userflags LSFOpt,NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 15 -e 2017 --userflags LSFOpt,PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 15 -e 2017 --userflags LSFOpt,NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
