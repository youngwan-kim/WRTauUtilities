SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2017.txt -n 10 -e 2017 --skim SkimTree_SingleTau --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2018.txt -n 10 -e 2018 --skim SkimTree_SingleTau --userflags RunXsecSyst& 
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2016a.txt -n 10 -e 2016a --skim SkimTree_SingleTau --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All_Skim_2016b.txt -n 10 -e 2016b --skim SkimTree_SingleTau --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt -n 5 -e 2016preVFP  --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt -n 5 -e 2016postVFP  --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt -n 5 -e 2017  --userflags RunXsecSyst&
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt -n 5 -e 2018 --userflags RunXsecSyst &  