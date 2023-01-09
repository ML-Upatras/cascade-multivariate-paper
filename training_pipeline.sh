#!/bin/bash
# bash script that runs the training pipeline script for all datasets (air_quality, traffic, power, energy, parking)

# set up list of datasets
datasets=(air_quality)

# set up arguments
logging_level=info

# loop through datasets
for dataset in "${datasets[@]}"; do
  echo "Training pipeline for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level
  echo "Done"
  echo ""
done