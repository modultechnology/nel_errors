#!/usr//bin/env bash

#please make sure you have permissions to create files and folder if running this script without sudo
# (e.g., use chmod -R 777 for the nel_archive folder or similar commands)

# example run:
# ./run_test.sh /home/adrian/git reuters128 recognize nel_archive/20170724/recognize

# modified to 
# ./run_test.sh reuters128 20170724 recognize

echo 'start eval'

ds=$1 #echo $ds
today=$2 #echo $today
tool=$3 #echo $tool

#archibase is current archival base (today's run)
gitbase=`python gitpath.py | tail -n 1`
#archipath = 'nel_archive'
archibase=$gitbase/nel_archive/$today/$tool

echo $gitbase

mkdir -p $archibase
mkdir -p $archibase/runs/
mkdir -p $archibase/runs/$ds/

cp $gitbase/nel_archive/corpora/$ds"a.csv" $archibase/$ds"a.csv"
cp $gitbase/nel_archive/corpora/$ds"b.csv" $archibase/$ds"b.csv"

cd $gitbase/error_analysis/src

#python recognyzerunner.py -g $gitbase -e $archibase -d $ds -p MAXIMUM.COVERAGE
python recognyzerunner.py -g $gitbase -e $archibase -d $ds -p GENERAL-2
python recognyzerun.py -e $archibase -d $ds -p $tool

#convert to TAC-KBP format
python converter.py $archibase/$ds-$tool.csv $archibase/$ds-$tool.out

#move to neleval to run the evals

cd $gitbase/neleval

#:'

#quick results
./nel evaluate -m all -f tab -g $gitbase/nel_archive/gold/$ds.gs $archibase/$ds-$tool.out  > $ds-$tool-results

#typed results
./nel evaluate -b type -f tab -g $gitbase/nel_archive/gold/$ds.gs $archibase/$ds-$tool.out > $ds-$tool-resultsbytype

#copy files back to nel_archive
mv $ds-$tool-results $archibase/$ds-$tool-results
mv $ds-$tool-resultsbytype $archibase/$ds-$tool-resultsbytype


PYTHONIOENCODING=utf-8 ./nel analyze -g $gitbase/nel_archive/gold/$ds.gs $archibase/$ds-$tool.out > $ds-$tool.analysis

mv $ds-$tool.analysis $archibase/$ds-$tool.analysis


#added merge
#currently needs a fix for encoding qutoed strings
cd $gitbase/error_analysis/src

python tacextractor.py $archibase/$ds-$tool.analysis $archibase/$ds-$tool.analysis.csv

mv $archibase/$ds-$tool-surface.csv $archibase/$ds-$tool-surface-withheaders.csv

sed -i 1i"doc|start|end|tac|gold|system|" $archibase/$ds-$tool.analysis.csv 

sed -i 's/\"//g' $archibase/$ds-$tool.analysis.csv 

sed -i 1i"doc|start|end|link|score|type|surfaceForm|" $archibase/$ds-$tool-surface-withheaders.csv 

sed -i 's/\"//g' $archibase/$ds-$tool-surface-withheaders.csv 

python merger.py $archibase/ $ds $ds-$tool.analysis.csv $ds-$tool-surface-withheaders.csv $gitbase

sed -i 1i"doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|gold|goldstart|goldend|" $archibase/$ds-overlap.csv

#'

#sleep 200

#cd $gitbase/error_analysis/src

#python mergerfix.py $archibase/ reuters128 $ds-$tool.analysis.csv $ds-$tool-surface-withheaders.csv

#egrep 'missing' $archibase/$ds-fixed.csv > $archibase/$ds-fixed-fn.csv

#egrep 'wrong-link|extra' $archibase/$ds-fixed.csv > $archibase/$ds-fixed-fp.csv

#'

echo 'end eval'