#!/usr/bin/env bash
sbt --error 'set showSuccess := false' 'run data/good-movies.csv ";" 0.001 30'   
