inputpath=$1
descriptor=$2

cat $inputpath.f[1234] > $descriptor.trainforfold0
cat $inputpath.f[0234] > $descriptor.trainforfold1
cat $inputpath.f[0134] > $descriptor.trainforfold2
cat $inputpath.f[0124] > $descriptor.trainforfold3
cat $inputpath.f[0123] > $descriptor.trainforfold4

cat $inputpath.f0 > $descriptor.testforfold0
cat $inputpath.f1 > $descriptor.testforfold1
cat $inputpath.f2 > $descriptor.testforfold2
cat $inputpath.f3 > $descriptor.testforfold3
cat $inputpath.f4 > $descriptor.testforfold4
