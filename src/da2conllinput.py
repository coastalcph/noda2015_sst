import argparse
parser = argparse.ArgumentParser(description="""""")
parser.add_argument('gold')
parser.add_argument('system')
parser.add_argument('--class-map', help="Map for string class to integer", required=True)

args = parser.parse_args()

classdict = dict(p for p in [line.strip().split("\t") for line in open(args.class_map)])



for line_gold, line_system in zip(open(args.gold),open(args.system)):
    line_gold = line_gold.strip()
    if len(line_gold) < 2:
        print
    else:
        goldline = line_gold.split("|")
        header = goldline[0]
        a = header.strip().split(" ")
        g = a[0]
        idx = a[-1]

        if args.bio or g == "O":
            pass 
        else:
            g = g[2:] #if BIO is not toggled, we discard the first two chars of the label before mapping

        s = line_system.strip()
        g = classdict[g]
        if s == "":
            s = "ERROR"
        else:
            s = classdict[s]
        outline = []
        outline.append(idx)
        outline.append(g)
        outline.append(s)
        print "\t".join(outline)
