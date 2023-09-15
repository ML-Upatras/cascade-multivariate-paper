#!/bin/bash
# bash script that runs the data_gen script for all datasets

# set up list of hourly datasets
datasets=(traffic power energy parking kolkata solar turbine joho iot taxi)

# set up general arguments
logging_level=info
fh=1

# loop through datasets
p_steps=168
for dataset in "${datasets[@]}"; do
  echo "Generating data for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level --p_steps=$p_steps --fh=$fh
  echo "Done"
  echo ""
done