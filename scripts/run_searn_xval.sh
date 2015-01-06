PATHTOFEATS="/home/alonso/proj/noda2015_sst/data/folds/"
DESCRIPTOR=$1 #either alltags or nophr
HOME="/home/alonso/proj/"
EVALPATH="$HOME"data/runs/
CONSTRAINDICT="$HOME"data/res/danishsst.possiblesupersenses
VW="/home/alonso/tool/vw_nov2014/vowpal_wabbit/vowpalwabbit/vw"

nclasses=119
B=5
passes=5

for fold in 0 #1 2 3 4
do
    MODELNAME=$DESCRIPTOR.$fold.mdl
    TRAINFILE=$PATHTOFEATS$DESCRIPTOR.trainforfold$fold
    TESTFILE=$PATHTOFEATS$DESCRIPTOR.testforfold$fold
    predout=$EVALPATH/$DESCRIPTOR.fold$fold.preds
    rawout=$EVALPATH/$DESCRIPTOR.fold$fold.raw
    bioout=$EVALPATH/$DESCRIPTOR.fold$fold.bio
    evalout=$EVALPATH/$DESCRIPTOR.fold$fold.evalsimple
    evalcrout=$EVALPATH/$DESCRIPTOR.fold$fold.evalconstr



    $VW -b $B -k -c -d $TRAINFILE --passes $passes --search_task sequence --search $nclasses -f $MODELNAME --keep b
    $VW -t -d  $TESTFILE -i $MODELNAME -p $predout -r $rawout

    python $HOME/src/vwsearn2column.py $predout --class-map $HOME/data/res/da_map_bio_testtime.txt > $onecolout
	python $HOME/src/da2conllinput.py $TESTFILE $onecolout --class-map $HOME/data/res/da_map_bio_testtime.txt > $bioout
	perl $HOME/scripts/conlleval.pl -d "\t" < $bioout > $evalout

	python $HOME/src/cr_contrains_on_raw_searn.py $TESTFILE $rawout --class-map ../data/res/da_map_bio_testtime.txt --supersense-dict $CONSTRAINDICT > $bioconstout
	perl $HOME/scripts/conlleval.pl -d "\t" < $bioconstout > $evalcrout

    rm $MODELNAME
done