## Running
- Format is the same as the scala implementation
    `python apriori.py datafile delimiter threshold [maxrecords]`
- Example:
    `python apriori.py ../code/data/good-movies.csv ";" 0.001 30`

## Bash files for generating test results
- There are some bash files that emulate the tests in this folder
    - `test01.sh` `test02.sh` `test03.sh`
    - These have the data location hardcoded to `../code/data/<csvfile>`

- Usage:
    - `sh test01.sh > test01.results`

## Test all at once
 - `test_all.sh data_dir`
    - generate all 3 test files, files obtained from the passed in data_dir
    - compare them to expected results with diff
    - delete the generated test files
 - Example:
    - `sh test_all.sh ../code/data/`


## Example Output of test-all.sh
```
Running test 1
Running with parameters: Filename [../code/data//good-movies.csv] Separator [;] Minimum relative support threshold [0.001]. Print at most 30 tuples.
Running test 2
Running with parameters: Filename [../code/data//market.csv] Separator [,] Minimum relative support threshold [0.03].
Running test 3
Running with parameters: Filename [../code/data//online.csv] Separator [,] Minimum relative support threshold [0.025]. Print at most 50 tuples.
********************************
Test 01 passed
********************************
********************************
Test 02 passed
********************************
********************************
Test 03 passed
********************************
```