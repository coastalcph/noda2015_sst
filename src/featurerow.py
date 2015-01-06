__author__ = 'alonso'
import re

class FeatureRow:

    def __init__(self,s):
        self.rawstring = s
        a = s.strip().split("|")
        self.header=a[0]
        self.feats={}
        for namespace in a[1:]:
            v = namespace.split(" ")
            self.feats[v[0]]=" ".join(v[1:])

    def __str__(self):
        return "|".join([self.header]+self.feats.keys())

    def add_embed_feats(self,namespace,feats):
        featv=[]
        pref=namespace[0]
        i=0
        for f in feats:
            f_i=pref+"_"+str(i)+":"+f
            featv.append(f_i)
            i+=1

        self.feats[namespace] = " ".join(featv)+" "

    def clean_morphology(self):
        #Shared
        #this function is completely ad hoc, i made it to remove the bad groupings of the morphology features
        v = self.feats["morphology"]
        v=v.replace("_suffix"," suffix").replace("_prefix"," prefix").replace("_shape"," shape").replace("_alphanum"," alphanum").replace("_proper"," proper").strip()
        outv = []
        #remove prefixes and suffixes because they are lexical
        for feat in v.split():
            if str(feat).startswith("prefix") or str(feat).startswith("suffix"):
                pass
            else:
                outv.append(feat)
        v=set(outv)

        self.feats["morphology"]=" ".join(v)+" "

    def clean_pos(self,posmap):
        #English
        v = self.feats["pos"]

        v=v.replace("t-2=_","p-2=^").replace("t2=_","p-2=$")
        v=v.replace("t-2F=","REMOVE").replace("t-1F=","REMOVE").replace("tF=","REMOVE").replace("t1F=","REMOVE").replace("t2F=","REMOVE")
        v=v.replace("t-2=","p_-2=").replace("t-1=","p_-1=").replace("t=","p_0=").replace("t1=","p_1=").replace("t2=","p_2=")
        v=v.strip().split(" ")
        vout=[]
        for feat in v:
            if feat.startswith("REMOVE"):
                pass
            elif feat == "proper":
                #proper must be displaced to to the morphology block
                self.feats["morphology"]="proper "+self.feats["morphology"]
            else:
                n,f=feat.split("=")
                try:
                    vout.append(n+"="+posmap[f])
                except:
                    print "Tres etrange", f
        del self.feats["pos"]
        self.feats["poswindow"]=" ".join(vout)+" "

    def clean_poswindow(self,posmap):
        #Danish
        v = self.feats["poswindow"]
        v=v.replace("=U=","=U").replace("=I=","=I")
        v=v.strip().split(" ")
        vout=[]
        for feat in v:
            n,f=feat.split("=")
            try:
                vout.append(n+"="+posmap[f])
            except:
                print f
        self.feats["poswindow"]=" ".join(vout)+" "

    def clean_shape(self):
        v = self.feats["shape"]
        self.feats["morphology"]=v+" "+self.feats["morphology"]


    def clean_sstwindow(self):
        #Danish
        pass #DEPRECATED!!
        v = self.feats["sstwindow"]
        v=v.replace("=B_","=").replace("=I_","=").replace("=O","=_")
        self.feats["sstwindow"]=v



    def clean_bagofsupersenses(self):
        #English
        # v = self.feats["bagofsupersenses"]
        # v=v.replace("psw","s_")
        # outv=[]
        # already=set()
        # whitelist=["s_-2","s_-1","s_-0","s_1","s_2"]
        # trunclist=["s_-2-0","s_-1-0","s_1-0","s_2-0"]
        # for t in v.strip().split(" "):
        #     n, f = t.split("=")
        #     if n == "s_-0":
        #         n="s_0"
        #         outv.append(n+"="+f)
        #     elif n in whitelist:
        #         outv.append(t)
        #     elif n in trunclist:
        #         if n[0:-2] not in already:
        #             outv.append(n[0:-2]+"="+f)
        # v = self.feats["bagofsupersenses"]
        # v = self.feats["bagofsupersenses"]

        #form = word_pat.search(self.rawstring)
        sst=self.feats["bagofsupersenses"]
        s0=re.search("psw\-0=(\S+)",sst)
        if s0 is None:
            s0="_"
        else:
            s0 = s0.groups()[0]

        del self.feats["bagofsupersenses"]
        self.feats["sstwindow"]="s_0="+s0+" "



    def namespaces(self):
        return sorted(self.feats.keys())

    def print_selected(self, namespacewhitelist):
        vout = []
        vout.append(self.header)
        for ns in self.namespaces():
            if ns in namespacewhitelist:
                vout.append(ns+" "+self.feats[ns])
        return "|".join(vout)

    def translate_target_sense_to_danish(self,danishmap,englishmap):
        sense, idx = self.header.strip().split(" ")
        sense = danishmap[englishmap[sense]]
        self.header = sense+" "+idx+" "

    def retrieve_headword(self,fieldname):
        x=re.search(" "+fieldname+"=(.+?) ",self.rawstring)
        hw= x.groups()[0]
        if hw=="<COLON>":
            hw=":"
        return hw

    def dannet_replace_sst(self,dannet,DanishLemmatizer,onto2supersense,form,pos):
        checkpos = ""
        if pos == "NOUN":
            checkpos="n"
        elif pos == "ADJ":
            checkpos = "a"
        elif pos == "VERB":
            checkpos="v"

        if pos in ["NOUN","VERB","ADJ"]:
            lemma=DanishLemmatizer.lemmatize(form,pos)
            s = dannet.synsets(lemma.lower()+"."+checkpos)
            if s:
                ot = s[0].attrs()["ontological_type"].replace("(","").replace(")","")
                ontokey = checkpos+"+"+ot
                if ontokey in onto2supersense:
                    sst=onto2supersense[ontokey]
                else:
                    sst="_"
            else:
                sst="_"
        else:
            sst="_"
        self.feats["sstwindow"]="s_0="+sst+" "