SKFlat.py -a WRTau_Analyzer  -i Tau -n 5 -e 2017  --userflags PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
# All Prompt
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 5 -e 2017 --userflags PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 5 -e 2017 --userflags NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 5 -e 2017 --userflags PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 5 -e 2017 --userflags NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 