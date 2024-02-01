SKFlat.py -a WRTau_Analyzer  -i Tau -n 15 -e 2017 --userflags MuIsoCutOpt &
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Bkg_All.txt -n 5 -e 2017 --userflags MuIsoCutOpt &
SKFlat.py -a WRTau_Analyzer  -l SubmitLists/Signal.txt -n 5 -e 2017 --userflags MuIsoCutOpt &

