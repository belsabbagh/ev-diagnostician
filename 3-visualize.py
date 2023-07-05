from os import path, makedirs
from timeit import default_timer
from matplotlib import pyplot as plt
from src import dataset_handler as dh


def plot_cycle(cycle):
    return cycle.plot()


def save_plot(battery_name, cycle_name, save_dir="out/cycles"):
    battery_dir = path.join(save_dir, battery_name)
    if not path.exists(battery_dir):
        makedirs(battery_dir)
    plt.savefig(path.join(battery_dir, f"{cycle_name}.png"))
    plt.close()


if __name__ == "__main__":
    start = default_timer()
    for battery_name, data in dh.battery_iter():
        _, cycles = data
        for cycle in cycles:
            name, df = cycle
            if name.split("_")[1] == "impedance":
                print(f"Skipping impedance cycle {name}")
                continue
            plot_cycle(df)
            save_plot(battery_name, name)
    print(f"Plotted cycles in {default_timer() - start} seconds.")
