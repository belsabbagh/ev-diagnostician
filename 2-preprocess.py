from os import path
from src import dataset_handler as dh
from src.config import paths

if __name__ == "__main__":
    for battery, data in dh.battery_iter():
        print(f"Preprocessing battery {battery}")
        df = dh.sync_data(data[0])
        df = df[df["Rectified_Impedance"].notna() & df["Capacity"].notna()]
        dh.save_to_csv(df, path.join(paths.PREPROCESSED_PATH, f"{battery}.csv"))
    print("Done. Check the preprocessed folder for the data.")
