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
python gen_data.py --data=<dataset> --hours=1
```

- `--data` is the dataset to use. The options are air_quality, traffic, energy, power and parking.
- `--hours` is the number of hours to aggregate the data.

You can also run the preprocessing script for all the datasets, with the paper's parameters with the following bash script:

```bash
/bin/bash gen_data.sh
```

### Training

For training the model, you can run:

```bash
python training_pipeline.py  --data=<dataset> --logging=info --ii=<int>
```

- `--data` is the dataset to use. The options are air_quality, traffic, energy, power and parking.
- `--logging` is the logging level. The options are `debug`, `info`, `warning`,
  `error` and `critical`. The default is `info`.
- `--ii` is the number of the importance iterations of the experiment. The default is 3.

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