SKFlat.py -a WRTau_Analyzer  -i Tau -n 15 -e 2017 --skim SkimTree_LRSMTau & #--userflags unweighted,noTauWeight& 
# All Prompt
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags PromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight& 

SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_QCD_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags PromptLepton,PromptTau & #--userflags unweighted,noTauWeight&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_QCD_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags NonpromptLepton,PromptTau & #--userflags unweighted,noTauWeight&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_QCD_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags PromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_QCD_Skim.txt -n 10 -e 2017 --skim SkimTree_LRSMTau --userflags NonpromptLepton,NonpromptTau & #--userflags unweighted,noTauWeight&
