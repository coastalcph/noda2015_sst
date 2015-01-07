#nophr.fold0.evalsimple
#alltags.fold0.evalconstr

runspath=/home/alonso/proj/noda2015_sst/data/runs

for evaltype in bio bioconstr
do
    for sensetags in nophr alltags
    do
        outfile=$runspath/$sensetags.allfolds.$evaltype
        cat $runspath/$sensetags.fold*.$evaltype > $outfile
    done
done
