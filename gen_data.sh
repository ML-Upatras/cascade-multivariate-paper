#!/bin/bash
# bash script that runs the data_gen script for all datasets (air_quality, traffic, power, energy,
# parking, room, solar, kolkata, turbine, joho, electricity, iot, home)

# set up list of datasets
datasets=(air_quality traffic power energy parking room solar kolkata turbine joho electricity iot home)

# set up arguments
hours=24
logging_level=info
p_steps=30
fh=1

# loop through datasets
for dataset in "${datasets[@]}"; do
  echo "Generating data for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level --hours=$hours --p_steps=$p_steps --fh=$fh
  echo "Done"
  echo ""
done
