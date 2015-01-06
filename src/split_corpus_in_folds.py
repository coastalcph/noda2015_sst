import argparse
import math
parser = argparse.ArgumentParser(description=""" Random sample feature file into N sentences""")
parser.add_argument("infile", metavar="FILE", help="name of the feature file")
parser.add_argument("n", type=int,metavar="FILE", help="number of folds")

args = parser.parse_args()












acc = ""
sentences = []
for line in open(args.infile).readlines():
    if len(line) < 3:
        sentences.append(acc)
        acc = ""
    else:
        acc = acc + line

perFold = math.ceil(len(sentences)/args.n)
numInst=0
fold=0
FILEOUT = open(args.infile+".f"+str(fold),"w")
linenum=0
for line in sentences:
    linenum+=1
    lineList = line.split("\t")

    FILEOUT.write(line+"\n")

    if len(lineList) ==1:
        numInst +=1
        if numInst > 0 and numInst % perFold == 0:
            print("Fold {} created.".format(fold))
            fold +=1
            FILEOUT.close()

            # if we are not at last
            if linenum < len(sentences):
                FILEOUT = open(args.infile+".f"+str(fold),"w")

FILEOUT.close()