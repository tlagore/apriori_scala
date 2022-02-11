#!/usr/bin/env bash

sbt --error 'set showSuccess := false' 'run data/online.csv "," 0.025 50'
