#!/bin/bash
# bash script that runs the data_gen script for all datasets (air_quality, traffic, power, energy, parking)

# set up list of datasets
datasets=(air_quality traffic power energy parking)

# set up arguments
hours=1
logging_level=info

# loop through datasets
for dataset in "${datasets[@]}"; do
  echo "Generating data for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level --hours=$hours
  echo "Done"
  echo ""
done
