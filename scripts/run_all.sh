#!/usr//bin/env bash

echo 'start eval'

#run the script:
 #./run_eval.sh /home/adrian/git/ reuters128 advanced nel_archive/20170204/advanced 
#this can also be read as:
#./run_eval.sh git_path dataset profile /path_to_folder

#gold can be either just the name or full path to neleval folder's gold
#gitbase=$1
#gold=$2
#profile=$3
#path_to_folder=$4
#this one should probably also be coded in the script

#this type of comment (:'some text') sis printing on the console (equivalent to multiline comment in bash)
#:'

cd $1/error_analysis/src
python $3run.py -e $1$4 -d $2 -p $3
#convert to TAC-KBP format
python converter.py $1$4/$2-$3.csv $1/$4/$2-$3.out

#cd $1/

#move to neleval to run the evals

cd $1/neleval

#quick results
./nel evaluate -m all -f tab -g $1nel_archive/gold/$2.gs $1$4/$2-$3.out  > $2-$3-results

#typed results
./nel evaluate -b type -f tab -g $1nel_archive/gold/$2.gs $1$4/$2-$3.out > $2-$3-resultsbytype

#copy files back to nel_archive
mv $2-$3-results $1/$4/$2-$3-results
mv $2-$3-resultsbytype $1/$4/$2-$3-resultsbytype


#explained results = primary error analysis from TAC-KBP tool
#this one has some UTF-8 error, so for now it still needs to be copied manually
PYTHONIOENCODING=utf-8 ./nel analyze -g $1nel_archive/gold/$2.gs $1$4/$2-$3.out > $2-$3.analysis

mv $2-$3.analysis $1/$4/$2-$3.analysis


#added merge
#currently needs a fix for encoding qutoed strings
cd $1/error_analysis/src

python tacextractor.py $1/$4/$2-$3.analysis $1/$4/$2-$3.analysis.csv

mv $1/$4/$2-$3-surface.csv $1/$4/$2-$3-surface-withheaders.csv

sed -i 1i"doc|start|end|tac|gold|system|" $1/$4/$2-$3.analysis.csv

sed -i 1i"doc|start|end|link|score|type|surfaceForm|" $1/$4/$2-$3-surface-withheaders.csv

python merger.py $1/$4/ reuters128 $2-$3.analysis.csv $2-$3-surface-withheaders.csv

sed -i 1i"doc|start|end|link|type|surfaceForm|tac|errorType|errorCause|inGold|gold|goldstart|goldend|" $1/$4/$2-overlap.csv
#'

:'

#sleep 20

cd $1/error_analysis/src

python mergerfix.py $1/$4/ reuters128 $2-$3.analysis.csv $2-$3-surface-withheaders.csv

egrep 'missing' $1/$4/$2-fixed.csv > $1/$4/$2-fixed-fn.csv

egrep 'wrong-link|extra' $1/$4/$2-fixed.csv > $1/$4/$2-fixed-fp.csv

#'

echo 'done'