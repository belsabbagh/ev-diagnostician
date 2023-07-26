from os import path
from src import dataset_handler as dh
from src.config import paths

if __name__ == "__main__":
    for battery, data in dh.battery_iter():
        print(f"Preprocessing battery {battery}")
        index, _ = data
        # index = dh.add_cycle_number(index)
        df = dh.sync_impedance_to_discharge(index)
        df = df[df["Rectified_Impedance"].notna() & df["Capacity"].notna()]
        df = dh.normalize(df)
        del df["Battery_impedance"]
        df.insert(len(df.columns), "Cycle_number", range(1, len(df) + 1))
        dh.save_to_csv(df, path.join(paths.PREPROCESSED_PATH, f"{battery}.csv"))
    print("Done. Check the preprocessed folder for the data.")
