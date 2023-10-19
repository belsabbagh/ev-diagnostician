import sys
from os import path, makedirs
from timeit import default_timer
from matplotlib import pyplot as plt
import pandas as pd
from src.config import charts, paths

BATTERIES = ["B0005", "B0006", "B0007", "B0018", "B0026"]


def plot_capacity_degradation(index):
    # plot capacity over cycle
    index = index[["Capacity", "Rectified_Impedance", "Re", "Rct"]]
    return index.plot(**charts.BATTERY_DISCHARGE_DEGRADATION)


def plot_impedance(df):
    df["Rectified_Impedance"] = df["Rectified_Impedance"].apply(
        lambda x: complex(x).real
    )
    return df.plot(**charts.BATTERY_IMPEDANCE_CURVE)


def plot_impedance_with_capacity(df):
    df["Rectified_Impedance"] = df["Rectified_Impedance"].apply(
        lambda x: complex(x).real
    )
    return df.plot(**charts.BATTERY_IMPEDANCE_CURVE)


def plot_cycle(cycle, cycle_type):
    params = (
        charts.CYCLE_DISCHARGE_CURVE
        if cycle_type == "discharge"
        else charts.CYCLE_CHARGE_CURVE
    )
    return cycle.plot(**params)


def save_cycle_plot(battery_name, cycle_name, save_dir="out/cycles"):
    save_plot(f"{cycle_name}.png", save_dir=path.join(save_dir, battery_name))
    plt.close()


def save_plot(filename, save_dir="out"):
    if not path.exists(save_dir):
        makedirs(save_dir)
    plt.savefig(path.join(save_dir, filename), dpi=300)
    plt.close()


if __name__ == "__main__":
    plot_all = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-all":
            plot_all = True
    print("Will finally start plotting")
    start = default_timer()
    for battery_name in BATTERIES:
        df = pd.read_csv(
            path.join(paths.PREPROCESSED_PATH, f"{battery_name}.csv"), index_col=0
        )
        plot_capacity_degradation(df)
        save_plot(f"{battery_name}.png", save_dir="out/preprocessed_batteries")
        plot_impedance(df)
        save_plot(f"{battery_name}.png", save_dir="out/impedance")
        if plot_all:
            for name, df in []:
                cycle_type = name.split("_")[1]
                if cycle_type == "impedance":
                    continue
                plot_cycle(df, cycle_type)
                save_cycle_plot(battery_name, name, save_dir="out/cycles")
        print(f"Plotted {battery_name}")
    print(f"Finished visualization in {default_timer() - start} seconds.")
