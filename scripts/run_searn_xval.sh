PATHTOFEATS="/home/alonso/proj/noda2015_sst/data/folds/"
DESCRIPTOR=$1 #either alltags or nophr

VW="/home/alonso/tool/vw_nov2014/vowpal_wabbit/vowpalwabbit/vw"

nclasses=119
B=25
passes=5

for fold in 0 #1 2 3 4
do
    MODELNAME=$DESCRIPTOR.$fold.mdl
    TRAINFILE=$PATHTOFEATS$DESCRIPTOR.trainforfold$fold
    TESTFILE=$PATHTOFEATS$DESCRIPTOR.testorfold$fold
    predout=A
    rawout=B

    $VW -b $B -k -c -d $TRAINFILE --passes $passes --search_task sequence --search $nclasses -f $MODELNAME
    $VW -t -d  $TESTFILE -i $MODELNAME -p $predout -r $rawout



    rm $MODELNAME
done