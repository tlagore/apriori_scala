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
 - `test_all.sh` will
    - generate all 3 test files
    - compare them to expected results with diff
    - delete the generated test files
 - also expects data location is kept at `../code/data/<csvfile>`