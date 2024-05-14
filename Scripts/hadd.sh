./hadd_v2.py --outdir 240513 --era 2016preVFP --skim LRSMTau
./hadd_v2.py --outdir 240513 --era 2016postVFP --skim LRSMTau
./hadd_v2.py --outdir 240513 --era 2017 --skim LRSMTau
./hadd_v2.py --outdir 240513 --era 2018 --skim LRSMTau
python3 comb2016.py
python3 combRun2.py