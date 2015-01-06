import argparse
import random
parser = argparse.ArgumentParser(description=""" Random sample feature file into N sentences""")
parser.add_argument("infile", metavar="FILE", help="name of the feature file")
args = parser.parse_args()


acc = ""
sentences = []
for line in open(args.infile).readlines():
    if len(line) < 3:
        sentences.append(acc)
        acc = ""
    else:
        acc = acc + line

random.shuffle(sentences)

for s in sentences:
    print s

