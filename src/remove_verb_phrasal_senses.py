__author__ = 'alonso'
import argparse
import random
parser = argparse.ArgumentParser(description=""" remove verb.PARTICLE,verb.REFLPRON and verb.COLL from sense tags and set it to O """)
parser.add_argument("infile", metavar="FILE", help="name of the feature file")
args = parser.parse_args()



phrasals =  "115 116 117 118".split(" ")
O_tag = "119"

# 115	B_verb.PARTICLE
# 116	B_verb.COLL
# 117	I_verb.COLL
# 118	B_verb.REFLPRON

acc = ""
sentences = []
for line in open(args.infile).readlines():
    if len(line) < 3:
        print
    else:
        a = line.strip().split(" ")
        sensetag = a[0]
        if sensetag in phrasals:
            a[0] = O_tag
        print " ".join(a)