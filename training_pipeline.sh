#!/bin/bash
# bash script that runs the training pipeline script for all datasets (air_quality, traffic, power, energy, parking, room)

# set up list of datasets
datasets=(air_quality traffic power energy parking room)

# set up arguments
logging_level=info
ii=0

# loop through datasets
for dataset in "${datasets[@]}"; do
  echo "Training pipeline for $dataset"
  python training_pipeline.py --data="$dataset" --logging=$logging_level --ii=$ii
  echo "Done"
  echo ""
done