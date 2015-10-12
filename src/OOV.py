import argparse
from collections import Counter
import argparse
import numpy as np
import random
import codecs
from numpy import log2, sum, isnan
from lillelemma.sto_lemmatizer import StoLemmatizer

parser = argparse.ArgumentParser(description="""""")
parser.add_argument('alldata')
from uniwordnet.dannet import DannetLoader


args = parser.parse_args()


loader = DannetLoader('/Users/alonso/data/DanNet-2.2_csv')
loader.load()
wn = loader.dannet

DanishLemmatizer = StoLemmatizer()



def countertoarray(C):
    l = []
    for s in senselist:
        l.append(C[s]+1.0)
    a = np.array(l)
    a /= sum(a)
    return a

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def checkWN(wn,DannishLemmatizer,formset):
    match = 0.0
    for f in formset:
        for POS,checkpos in zip(["NOUN","VERB","ADJ"],["n","v","a"]):
            lemma = DanishLemmatizer.lemmatize(f,POS)
            s = wn.synsets(lemma.lower()+"."+checkpos)
            if s:
                match+=1
                break
            else:
                pass
                #print f, "with lemma", lemma, "is not in DanNet for", POS
    return match

def readSentences(infile):
    words = []
    postags = []
    biosenses = []
    senses = []
    lemmas = []

    words_acc = []
    lemmas_acc = []
    postags_acc = []
    biosenses_acc = []
    senses_acc = []

    for line in codecs.open(infile,encoding="utf-8").readlines():
        line = line.strip()
        if len(line) < 1:
            words.append(words_acc)
            words_acc = []
            lemmas.append(lemmas_acc)
            lemmas_acc = []
            postags.append(postags_acc)
            postags_acc = []
            biosenses.append(biosenses_acc)
            biosenses_acc = []
            senses.append(senses_acc)
            senses_acc = []
        else:
            (w,l,p,bio) = line.strip().split("\t")

            biosensetag = bio.split("|")[0]
            if "_" in biosensetag:
                bio,sense = biosensetag.split("_")

            p=p[:2]

            words_acc.append(w.lower())
            lemmas_acc.append(l.lower())
            postags_acc.append(p)
            biosenses_acc.append(biosensetag)
            senses_acc.append(sense)
    return words, lemmas, postags, biosenses, senses

forms, lemmas, postags, biosenses, senses = readSentences(args.alldata)

indices = range(len(forms))
random.shuffle(indices)

fold1,fold2,fold3,fold4,fold5 = list(chunks(indices,300))


for l in [forms, lemmas]:
    f1 =  [item for sublist in [l[i] for i in fold1] for item in sublist]
    f2 =  [item for sublist in [l[i] for i in fold2] for item in sublist]
    f3 =  [item for sublist in [l[i] for i in fold3] for item in sublist]
    f4 =  [item for sublist in [l[i] for i in fold4] for item in sublist]
    f5 =  [item for sublist in [l[i] for i in fold5] for item in sublist]

    f2345 = f2+f3+f4+f5
    f1345 = f1+f3+f4+f5
    f1245 = f1+f2+f4+f5
    f1235 = f1+f2+f3+f5
    f1234 = f1+f2+f3+f4

    acc = 0.0
    acc_wn = 0.0
    for test, train in zip([f1,f2,f3,f4,f5],[f2345,f1345,f1245,f1235,f1234]):
        #print len(test), len(train)
        acc+= float(len(set(test).difference(set(train)))) / float(len(set(test)))
        not_in_train = set(test).difference(set(train))
        wnmatches = checkWN(wn,DanishLemmatizer,not_in_train)
        print wnmatches, len(not_in_train), len(set(test))
        acc_wn += float(len(not_in_train) - wnmatches ) / len(set(test))



    print acc / 5, (acc_wn / 5)


## from there, DanNet coverage



formset = set([item for sublist in [l[i] for i in fold1] for item in sublist])
print (len(formset) - checkWN(wn,DanishLemmatizer,formset)) / float(len(formset))
