from os import path, listdir

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
    for folder, battery in battery_path_iter():
        for cycle in battery_cycles_iter(
            path.join(paths.GENERATED_PATH, folder, battery)
        ):
            yield folder, battery, cycle


def get_battery(folder, battery):
    batt_dir = path.join(paths.GENERATED_PATH, folder, battery)
    cycles = [
        (cycle.split(".")[0], get_battery_cycle(batt_dir, cycle))
        for cycle in battery_cycles_iter(batt_dir)
    ]
    return pd.read_csv(path.join(batt_dir, "index.csv"), index_col="cycle"), cycles


def get_battery_cycle(batt_dir, cycle):
    cycle_type = cycle.split(".")[0].split("_")[1]
    df = pd.read_csv(path.join(batt_dir, cycle))
    if cycle_type != "impedance":
        df.set_index("Time", inplace=True)
    return df


def battery_path_iter(root=paths.GENERATED_PATH):
    for folder in listdir(root):
        for battery in listdir(path.join(root, folder)):
            yield folder, battery


def battery_iter(root=paths.GENERATED_PATH):
    for folder, battery in battery_path_iter(root):
        battery_name = battery.split(".")[0]
        yield battery_name, get_battery(folder, battery)
