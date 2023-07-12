from os import path, makedirs
from timeit import default_timer
from src import mat_handler as mt, dataset_handler as dh
from src.config import paths


if __name__ == "__main__":
    if not dh.dataset_exists():
        print(
            "Dataset not found. Please download the dataset first and place the folders in the dataset/data folder"
        )
        exit(1)
    start = default_timer()
    filecount = 0
    for folder, filename in dh.original_path_iter():
        batt_name = filename.split(".")[0]
        filepath = path.join(paths.ORIGINAL_PATH, folder, filename)
        mat = mt.loadMat(filepath)
        try:
            index, cycles = mt.mat_to_df(mat)
            battery_folder = path.join(paths.GENERATED_PATH, batt_name)
            if not path.exists(battery_folder):
                makedirs(battery_folder)
            for i, cycle in enumerate(cycles):
                cycle_type = index.iloc[i]["type"]
                padded = str(i).zfill(3)
                cycle.to_csv(path.join(battery_folder, f"{padded}_{cycle_type}.csv"))
                filecount += 1
            index.to_csv(path.join(battery_folder, f"index.csv"))
            print(f"Generated {batt_name} from {folder}")
        except Exception as e:
            raise RuntimeError(f"Error while generating {batt_name} in {folder}.\n{e}")
    print(f"Generated {filecount} files in {default_timer() - start} seconds.")
