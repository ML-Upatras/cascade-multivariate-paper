#!/bin/bash
# bash script that runs the data_gen script for all datasets (air_quality, traffic, power, energy,
# parking, room, solar, kolkata, turbine, joho, electricity, iot, wind, sofia, daily_temp, alcohol)

# set up list of hourly datasets
datasets=(air_quality traffic power energy parking room solar kolkata turbine joho electricity iot wind sofia)

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

# set up list of daily datasets
daily_datasets=(daily_temp)

p_steps=7
for dataset in "${daily_datasets[@]}"; do
  echo "Generating data for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level --p_steps=$p_steps --fh=$fh
  echo "Done"
  echo ""
done

# set up list of monthly datasets
monthly_datasets=(alcohol air riders)

p_steps=12
for dataset in "${monthly_datasets[@]}"; do
  echo "Generating data for $dataset"
  python gen_data.py --data="$dataset" --logging=$logging_level --p_steps=$p_steps --fh=$fh
  echo "Done"
  echo ""
done
