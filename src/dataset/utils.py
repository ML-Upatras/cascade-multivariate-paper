from src.dataset.air import load_air
from src.dataset.air_quality import load_air_quality
from src.dataset.alcohol import load_alcohol
from src.dataset.daily_temperature import load_daily_temperature
from src.dataset.electricity import load_electricity
from src.dataset.energy import load_energy
from src.dataset.iot import load_iot
from src.dataset.joho import load_joho
from src.dataset.kolkata import load_kolkata
from src.dataset.parking import load_parking
from src.dataset.power import load_power
from src.dataset.riders import load_riders
from src.dataset.room import load_room
from src.dataset.sofia import load_sofia
from src.dataset.solar import load_solar
from src.dataset.traffic import load_traffic
from src.dataset.turbine import load_turbine
from src.dataset.wind import load_wind


def get_dataset_names():
    names = [
        "air_quality",
        "traffic",
        "energy",
        "power",
        "parking",
        "room",
        "solar",
        "kolkata",
        "turbine",
        "joho",
        "electricity",
        "iot",
        "wind",
        "sofia",
        "daily_temp",
        "alcohol",
        "air",
        "riders",
    ]

    return names


def load_dataset(data_name, data_path):
    if data_name == "air_quality":
        df = load_air_quality(data_path)
    elif data_name == "traffic":
        df = load_traffic(data_path)
    elif data_name == "energy":
        df = load_energy(data_path)
    elif data_name == "power":
        df = load_power(data_path)
    elif data_name == "parking":
        df = load_parking(data_path)
    elif data_name == "room":
        df = load_room(data_path)
    elif data_name == "solar":
        df = load_solar(data_path)
    elif data_name == "kolkata":
        df = load_kolkata(data_path)
    elif data_name == "turbine":
        df = load_turbine(data_path)
    elif data_name == "joho":
        df = load_joho(data_path)
    elif data_name == "electricity":
        df = load_electricity(data_path)
    elif data_name == "iot":
        df = load_iot(data_path)
    elif data_name == "wind":
        df = load_wind(data_path)
    elif data_name == "sofia":
        df = load_sofia(data_path)
    elif data_name == "daily_temp":
        df = load_daily_temperature(data_path)
    elif data_name == "alcohol":
        df = load_alcohol(data_path)
    elif data_name == "air":
        df = load_air(data_path)
    elif data_name == "riders":
        df = load_riders(data_path)

    return df
