import argparse
import os

def AddFlagSubmit(input_file, newflag):
    with open(input_file, 'r') as infile :
        for line in infile :
            if line.startswith('#') : continue
            elif '--userflag' in line:
                newstring = line.replace("--userflags ",f"--userflags {newflag},")
                os.system(newstring)
                #outfile.write(newstring)
            else :
                newstring = line.replace("&",f"--userflags {newflag} &")
                os.system(newstring)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a new flag and run')
    parser.add_argument('-i', dest='input_file' ,type=str, help='Path to the input batch .sh file',default='WRTau.sh')
    parser.add_argument('--newflag', type=str, required=True, help='Flag to add')
    args = parser.parse_args()

    AddFlagSubmit(args.input_file, args.newflag)
