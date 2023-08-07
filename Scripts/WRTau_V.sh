SKFlat.py -a WRTau_Analyzer  -l SubmitLists/VJets.txt -n 30 -e 2017 --userflags PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/VJets.txt -n 30 -e 2017 --userflags NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/VJets.txt -n 30 -e 2017 --userflags PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/VJets.txt -n 30 -e 2017 --userflags NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 