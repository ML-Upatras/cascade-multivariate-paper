#!/bin/bash
# bash script that runs the training pipeline script for all datasets
# (traffic power energy parking room solar turbine joho iot taxi daily_energy covid meat alcohol robberies)

# set up list of datasets
datasets=(traffic power energy parking room solar turbine joho iot taxi daily_energy covid meat alcohol robberies)

# set up arguments
logging_level=debug
ii=0
perc=0

# loop through datasets
for dataset in "${datasets[@]}"; do
  echo "Training pipeline for $dataset"
  python training_pipeline.py --data="$dataset" --logging=$logging_level --ii=$ii --perc=$perc
  echo "Done"
  echo ""
done