#!/bin/bash
if [ -z "$1" ];
then
      echo "data_directory must be supplied. Usage is \"sh test03.sh data_directory/\""
      exit -1
fi

data_dir=$1

python apriori.py $data_dir/online.csv "," 0.025 50
