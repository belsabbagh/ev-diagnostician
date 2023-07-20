import sys
from os import path, makedirs
from timeit import default_timer
from matplotlib import pyplot as plt
from src import dataset_handler as dh
from src.config import charts


def plot_capacity_degradation(index):
    # plot capacity over cycle
    index = index.loc[index["type"] == "discharge", ["Capacity"]]
    return index.plot(**charts.BATTERY_DISCHARGE_DEGRADATION)


def plot_impedance(index):
    df = index.loc[
        index["type"] == "impedance",
        ["Rectified_Impedance", "Re", "Rct"],
    ].copy()
    df["Rectified_Impedance"] = df["Rectified_Impedance"].apply(
        lambda x: complex(x).real
    )
    return df.plot(**charts.BATTERY_IMPEDANCE_CURVE)


def plot_impedance_with_capacity(index):
    df = index.loc[
        index["type"] == "impedance",
        ["Rectified_Impedance"],
    ].copy()
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
    # remove outliers using z-score
    discharge_df = dh.filter_outliers(dh.collect_discharge_data(), "Capacity")
    impedance_df = dh.filter_outliers(dh.collect_impedance_data(), "Rectified_Impedance")
    plt.scatter(
        *zip(
            *[(x, y) for x, y in zip(discharge_df["Cycle"], discharge_df["Capacity"])]
        ),
        s=1,
        c="blue",
    )
    plt.scatter(
        *zip(
            *[
                (x, y)
                for x, y in zip(
                    impedance_df["Cycle"], impedance_df["Rectified_Impedance"]
                )
            ]
        ),
        s=1,
        c="red",
    )
    plt.show()
    print("Will finally start plotting")
    start = default_timer()
    for battery_name, data in dh.battery_iter():
        index, cycles = data
        plot_capacity_degradation(index)
        save_plot(f"{battery_name}.png", save_dir="out/batteries")
        plot_impedance(index)
        save_plot(f"{battery_name}.png", save_dir="out/impedance")
        if plot_all:
            for name, df in cycles:
                cycle_type = name.split("_")[1]
                if cycle_type == "impedance":
                    continue
                plot_cycle(df, cycle_type)
                save_cycle_plot(battery_name, name, save_dir="out/cycles")
        print(f"Plotted {battery_name}")
    print(f"Finished visualization in {default_timer() - start} seconds.")
