import argparse
import codecs
import numpy as np
import sys
from featurerow import FeatureRow
from collections import  defaultdict
import HTMLParser


parser = argparse.ArgumentParser(description="""""")
parser.add_argument('gold')
parser.add_argument('system')
parser.add_argument('--class-map', help="Map for string class to integer", required=False)
parser.add_argument('--supersense-dict', help="supersense dictionary to constrain from", required=False)

args = parser.parse_args()


#python cr_contrains_on_raw_searn.py /media/hvk610/OSD/data/sst/semcor/SEM.BIO.conll.fold2 /media/hvk610/OSD/data/sst/patcheval/raw --class-map ../../res/vwmap_bio.txt --supersense-dict /media/hvk610/OSD/data/sst/emnlp_dict.txt --normalization-dict /media/hvk610/OSD/data/sst/emnlp_dict.txt


MFSdict = defaultdict(set)

pairs = [line.replace("_","-").strip().split("\t") for line in open(args.class_map)]
class_str_to_int = dict((pair[1], int(pair[0])) for pair in pairs)
int_to_class_str = dict((int(pair[0]),pair[1]) for pair in pairs)
int_to_class_str[0] = "LOOKUPERROR"
class_str_to_int["LOOKUPERROR"] = 0
#normalization = dict(tuple(line.strip().split("\t"))                      for line in codecs.open(args.normalization_dict, encoding='utf-8'))
posinf = float("inf")



fin = codecs.open(args.supersense_dict, encoding='utf-8')
lines = fin.readlines()
for line in lines[1:]:
    w, k = line.strip().split("\t")
    if k != "O":
        MFSdict[w].add(k)
h = HTMLParser.HTMLParser()


for line, gold_line in zip(codecs.open(args.system, encoding='utf-8').readlines(),codecs.open(args.gold, encoding='utf-8').readlines()):
    ar = line.strip().split(" ")
    if len(gold_line) < 3:
        ##pass
        print 
    else:
        authorized_for_word = []
        gold_ar = []
        features_gold= FeatureRow(gold_line)

        #1) retrieve word from gold line
        whtml  =features_gold.retrieve_headword("w_0")
        word = h.unescape(whtml)
        postag = features_gold.retrieve_headword("p_0").lower()
        goldtag = features_gold.header.split(" ")[0]

        predictions = np.array([posinf]+[float(iv.split(":")[1]) for iv in line.split()][:-1])
        oldpreds = np.array(predictions)

        if word in MFSdict and np.argmin(predictions) != 119:
            authorized_for_word = MFSdict[word]
            #2) prune non-valid class values
            #word = word+"\tchecked"
            #out = whtml + str(authorized_for_word}
            #sys.stderr.write(out)
            for i,v in enumerate(predictions):
                #if i is NOT a valid sense class for the word, set the value to float.
                if i == 119 or i == 0:
                    pass
                #elif int_to_class_str[i].split("-")[1].lower()[0] != postag[0].lower() and i != 119 and postag in ["noun", "adj", "verb"]:
                #    out = "removing"+int_to_class_str[i][2].lower()+":"+int_to_class_str[i]+":"+postag+":"+word+"\n"
                #    #sys.stderr.write(out)
                #    predictions[i] = posinf
                if int_to_class_str[i] not in authorized_for_word:
                    predictions[i] = posinf
        else:
            pass
            #whtml = whtml+"\tnoconstrain"+"\t"+postag+"#".join(authorized_for_word)

        gold_ar.append(whtml)
        gold_ar.append(int_to_class_str[int(goldtag)])
        if np.argmin(predictions) == 0: #pruned all, give original pred
            s = str(int_to_class_str[np.argmin(oldpreds)])
        else:
            s = str(int_to_class_str[np.argmin(predictions)])
        gold_ar.append(s)
        print "\t".join(gold_ar)
        #4) convert to class and print something like conelleval input





