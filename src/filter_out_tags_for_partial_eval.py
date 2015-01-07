import argparse

parser = argparse.ArgumentParser(description="""""")
parser.add_argument('file')
parser.add_argument('filtetype',default="keeplexical")
args = parser.parse_args()


VERBPRHASALS = "B-verb.PARTICLE B-verb.COLL I-verb.COLL B-verb.REFLPRON".split(" ")

def filtersense(tag,filtertype):
    if filtertype == "keeplexical":
        if tag in VERBPRHASALS:
            return "O"
        else:
            return tag
    else:
        if tag not in VERBPRHASALS:
            return "O"
        else:
            return tag


for line in open(args.file).readlines():
    if len(line) < 3:
        print
    else:
        key, gold, system = line.strip().split("\t")
        gold = filtersense(gold,args.filtersense)
        sense = filtersense(sense,args.filtersense)
        print "\t".join(key,gold,system)