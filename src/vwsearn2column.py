import argparse
import codecs

parser = argparse.ArgumentParser(description="""""")
parser.add_argument('file')
parser.add_argument('--class-map', help="Map for string class to integer", required=True)
args = parser.parse_args()

classdict = dict(p for p in [line.strip().split("\t") for line in open(args.class_map)])

for line in open(args.file):
    for c in line.strip().split(" ")[:-1]:
        if c in classdict:
            print c
        else:
            print
    