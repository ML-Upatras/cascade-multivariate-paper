# cascade-multivariate-paper

![Python 3.7.15](https://img.shields.io/badge/python-3.7.15-green.svg)
![black](https://img.shields.io/badge/code%20style-black-000000.svg)
![isort](https://img.shields.io/badge/isort-5.11.4-blue.svg)
![flake8](https://img.shields.io/badge/flake8-5.0.4-blue.svg)

## How to run

### Install dependencies

First, you need to install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Data preprocessing

Then, you can run the preprocessing of the data script:

```bash
python gen_data.py --data=<dataset> --hours=1 --p_steps=0
```

- `--data` is the dataset to use. The options are air_quality, traffic, energy, power, parking, room, solar, kolkata, turbine, joho, electricity, iot and wind.
- `--hours` is the number of hours to aggregate the data.
- `--p_steps` is the number of previous time steps to add as features to the final dataset.

You can also run the preprocessing script for all the datasets, with the paper's parameters with the following bash script:

```bash
/bin/bash gen_data.sh
```

### Training

For training the model, you can run:

```bash
python training_pipeline.py  --data=<dataset> --logging=info --ii=<int>
```

- `--data` is the dataset to use. The options are air_quality, traffic, energy, power, parking, room, solar, kolkata, turbine, joho, electricity, iot and wind.
- `--logging` is the logging level. The options are `debug`, `info`, `warning`,
  `error` and `critical`. The default is `info`.
- `--ii` is the number of the importance iterations of the experiment. If it's 0 then feature importance is not calculated. The default is 0.

## Dataset descriptions

### Air Quality Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/fedesoriano/air-quality-data-set?resource=download)

### Traffic Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/fedesoriano/traffic-prediction-dataset)

### Energy consumption Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption?select=PJM_Load_hourly.csv)

### Power Consumption of Turkey (2016-2020)

[Download & information about the dataset](https://www.kaggle.com/datasets/hgultekin/hourly-power-consumption-of-turkey-20162020?select=RealTimeConsumption-01012016-04082020.csv)

### Parking Occupancy Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/mypapit/klccparking)

### Room Temperature Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/vitthalmadane/ts-temp-1)

### Solar Generation in Italy Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/arielcedola/solar-generation-and-demand-italy-20152016)

### Temperature and Humidity of Kolkata from 2015-2020

[Download & information about the dataset](https://www.kaggle.com/datasets/sumandey/temperature-and-humidity-of-kolkata-from-20152020)

### Wind Turbine Texas Dataset

[Download & information about the dataset](https://www.kaggle.com/datasets/pravdomirdobrev/texas-wind-turbine-dataset-simulated)

### Hourly load data of the power supply company of the city of Joho

[Download & information about the dataset](https://www.kaggle.com/datasets/pattnaiksatyajit/hourly-load-data)

### Household Electric Power Consumption

[Download & information about the dataset](https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set)

### Temperature Readings : IOT Devices

[Download & information about the dataset](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)

### Wind Time Series Dataset

[Download & information about the dataset](https://zenodo.org/record/5516539#.Y8rmb3ZByUk)

### Sofia Dataset

[Download & information about the dataset](https://zenodo.org/record/5516539#.Y8rmb3ZByUk)

### Alcohol Sales Dataset

[Download & information about the dataset](https://fred.stlouisfed.org/series/S4248SM144NCEN)
