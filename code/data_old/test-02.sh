#!/usr/bin/env bash
sbt --error 'set showSuccess := false' 'run data/market.csv "," 0.03'
