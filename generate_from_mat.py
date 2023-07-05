from os import path, listdir, makedirs
from src import mat_handler

ROOT = "dataset"
ORIGINAL_PATH = path.join(ROOT, "data")
GENERATED_PATH = path.join(ROOT, "generated")


def dataset_exists():
    return path.exists(ORIGINAL_PATH)


def dataset_path_iter():
    for folder in listdir(ORIGINAL_PATH):
        for filename in listdir(path.join(ORIGINAL_PATH, folder)):
            if not filename.endswith(".mat"):
                continue
            yield folder, filename


if __name__ == "__main__":
    if not dataset_exists():
        print(
            "Dataset not found. Please download the dataset first and place the folders in the dataset/data folder"
        )
        exit(1)
    for folder, filename in dataset_path_iter():
        battery_name = filename.split(".")[0]
        filepath = path.join(ORIGINAL_PATH, folder, filename)
        mat = mat_handler.loadMat(filepath)
        try:
            index, cycles = mat_handler.mat_to_df(mat)
            battery_folder = path.join(GENERATED_PATH, folder, battery_name)
            if not path.exists(battery_folder):
                makedirs(battery_folder)
            for i, cycle in enumerate(cycles):
                cycle_type = index.iloc[i]["type"]
                cycle.to_csv(path.join(battery_folder, f"{i+1}_{cycle_type}.csv"))
            index.to_csv(path.join(battery_folder, f"index.csv"))
            print(f"Generated {battery_name} in {folder}")
        except Exception as e:
            raise RuntimeError(
                f"Error while generating {battery_name} in {folder}.\n{e}"
            )
