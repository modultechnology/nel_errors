#!/usr//bin/env bash

# example run:
# ./run_test.sh /home/adrian/git reuters128 recognize nel_archive/20170724/recognize

# modified to 
# ./run_test_fixer.sh reuters128 20170724 recognize

echo 'start eval'



#sleep 20

ds=$1 #echo $ds
today=$2 #echo $today
tool=$3 #echo $tool

#archibase is current archival base (today's run)
gitbase=`python gitpath.py | tail -n 1`
#archipath = 'nel_archive'
#this in a different context therefore we add / to avoid errors
archibase=$gitbase/nel_archive/$today/$tool

echo $gitbase
echo $archibase

cd $gitbase/error_analysis/src

python mergerfix.py $archibase $ds $ds-$tool.analysis.csv $ds-$tool-surface-withheaders.csv $gitbase

egrep 'correct link' $archibase/$ds-fixed.csv > $archibase/$ds-fixed-tp.csv

egrep 'missing' $archibase/$ds-fixed.csv > $archibase/$ds-fixed-fn.csv

egrep 'wrong-link|extra' $archibase/$ds-fixed.csv > $archibase/$ds-fixed-fp.csv

python evalfixer.py $archibase/$ds-overlap.csv $archibase/$ds-fixed.csv > $archibase/$ds-$tool-resultsbytype-fixed

#'

echo 'done'