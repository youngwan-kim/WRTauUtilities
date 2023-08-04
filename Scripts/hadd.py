import os,argparse

def HADDnGet(flag,outdir,fakemode):
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hadd output files from WRTauAnalyzer')
    parser.add_argument('--flag', type=str, required=True, help='Additional flag used',default='')
    parser.add_argument('--outdir', type=str, required=True, help='Output dir')
    parser.add_argument('--fakemode', type=int, required=True, help='Fake division mode , 0 : Combine all / 1 : Division per fake source / 2 : Get Both',default=2)
    args = parser.parse_args()

    HADDnGet(args.flag,args.outdir,args.fakemode)