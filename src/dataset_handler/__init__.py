from os import path, listdir
import os
import numpy as np

import pandas as pd
from src.config import paths


def dataset_exists():
    return path.exists(paths.ORIGINAL_PATH)


def original_path_iter():
    for folder in listdir(paths.ORIGINAL_PATH):
        for filename in listdir(path.join(paths.ORIGINAL_PATH, folder)):
            if not filename.endswith(".mat"):
                continue
            yield folder, filename


def battery_cycles_iter(battery_path):
    for cycle in listdir(battery_path):
        if cycle == "index.csv" or not cycle.endswith(".csv"):
            continue
        yield cycle


def dataset_path_iter():
    for battery in battery_path_iter():
        for cycle in battery_cycles_iter(path.join(paths.GENERATED_PATH, battery)):
            yield battery, cycle


def get_battery(battery):
    batt_dir = path.join(paths.GENERATED_PATH, battery)
    battery_index = pd.read_csv(path.join(batt_dir, "index.csv"), index_col="cycle")
    battery_index["Rectified_Impedance"] = battery_index["Rectified_Impedance"].apply(
        lambda x: complex(x).real, convert_dtype=True
    )
    cycles = [
        (cycle.split(".")[0], get_battery_cycle(batt_dir, cycle))
        for cycle in battery_cycles_iter(batt_dir)
    ]
    return battery_index, cycles


def get_battery_cycle(batt_dir, cycle):
    cycle_type = cycle.split(".")[0].split("_")[1]
    df = pd.read_csv(path.join(batt_dir, cycle))
    if cycle_type != "impedance":
        df.set_index("Time", inplace=True)
    return df


def battery_path_iter(root=paths.GENERATED_PATH):
    """Returns a generator of battery directory names from the generated data"""
    for battery in listdir(root):
        yield battery


def battery_iter(root=paths.GENERATED_PATH):
    """Returns a generator of tuples (battery_name, (index, cycles))"""
    for battery in battery_path_iter(root):
        yield battery.split(".")[0], get_battery(battery)


def validate_data(df):
    nan_values = df.isna().any(axis=1)
    if nan_values.any():
        raise ValueError(f"NaN values found in {df[nan_values]}")
    return True


def collect_feature_from_index(feature, cycle_type, _iter=battery_iter):
    data_dict = {
        "Cycle": [],
        feature: [],
        "Battery": [],
    }
    for battery_name, data in _iter():
        batt_index, _ = data
        batt_index = batt_index.loc[batt_index["type"] == cycle_type]
        data_dict["Cycle"].extend(batt_index.index.values)
        data_dict[feature].extend(batt_index[feature].values)
        data_dict["Battery"].extend([battery_name] * len(batt_index))
    df = pd.DataFrame.from_dict(data_dict)
    df.sort_values(by=["Cycle", "Battery"], inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.dropna(inplace=True)
    validate_data(df)
    return pd.DataFrame.from_dict(df)


def collect_discharge_data(battery_iter=battery_iter):
    return collect_feature_from_index("Capacity", "discharge", battery_iter)


def collect_impedance_data(battery_iter=battery_iter):
    return collect_feature_from_index("Rectified_Impedance", "impedance", battery_iter)


def cycle_to_capacity(df):
    return df.iloc[:, 0:1], df.iloc[:, 1]


def impedance_to_cycle(df):
    return df.iloc[:, 1:2], df.iloc[:, 0]


def filter_outliers(df, column, threshold=2.5):
    return df[abs((df[column] - df[column].mean()) / df[column].std()) < threshold]


def save_to_csv(df, filepath, **kwargs):
    if not path.exists(path.dirname(filepath)):
        os.makedirs(path.dirname(filepath))
    df.to_csv(filepath, **kwargs)


def fill_capacity(capacities):
    return np.mean(capacities)


def sync_data(index):
    capacities = []
    discharge = False
    for cycle in index.index.values:
        cycle_type = index.loc[cycle, "type"]
        value = index["Capacity"].dropna(inplace=False).iloc[0]
        if cycle_type == "discharge":
            discharge = True
            capacities.append(index.loc[cycle, "Capacity"])
        elif cycle_type == "impedance":
            if discharge:
                value = fill_capacity(capacities)
                capacities.clear()
                discharge = False
            index.loc[cycle, "Capacity"] = value
    return index
