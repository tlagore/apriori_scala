#!/bin/bash
function test_res {
    f1=$1
    f2=$2
    test=$3
    RES= diff $f1 $f2

    echo "********************************"
    if diff $f1 $f2 >/dev/null;
    then
        
        echo "Test $test passed"
    else
        echo "Test $test failed. $f1 did not match $f2"
        echo "Results of diff:"
        echo "$RES"
    fi
    echo "********************************"
}

echo "Running test 1"
python apriori.py ../code/data/good-movies.csv ";" 0.001 30 > test01.results
echo "Running test 2"
python apriori.py ../code/data/market.csv "," 0.03 > test02.results
echo "Running test 3"
python apriori.py ../code/data/online.csv "," 0.025 50 > test03.results

test_res test01.results ../code/data/test-01.expected "01"
test_res test02.results ../code/data/test-02.expected "02"
test_res test03.results ../code/data/test-03.expected "03"

rm test01.results
rm test02.results
rm test03.results