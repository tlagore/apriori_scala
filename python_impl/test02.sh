#!/bin/bash
if [ -z "$1" ];
then
      echo "data_directory must be supplied. Usage is \"sh test02.sh data_directory/\""
      exit -1
fi

data_dir=$1

python apriori.py $data_dir/market.csv "," 0.03
