from os import path, listdir
import pandas as pd
import scipy.io
from datetime import datetime

ROOT = "dataset"
ORIGINAL_PATH = path.join(ROOT, "data")
GENERATED_PATH = path.join(ROOT, "generated")

CHARGE_COLUMNS = [
    "Cycle",
    "Voltage",
    "Current",
    "Temperature",
    "Current_charge",
    "Voltage_charge",
    "Time",
    "Current_load",
    "Voltage_load",
    "Capacity",
]


def convert_to_time(hmm):
    year, month, day, hour, minute, second = (
        int(hmm[0]),
        int(hmm[1]),
        int(hmm[2]),
        int(hmm[3]),
        int(hmm[4]),
        int(hmm[5]),
    )
    return datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )


def mat_to_df(filepath):
    mat = scipy.io.loadmat(filepath)
    filename = path.basename(filepath).split(".")[0]
    col = mat[filename][0][0][0][0]
    size = col.shape[0]
    data: pd.DataFrame = pd.DataFrame(columns=CHARGE_COLUMNS)
    meta = []
    for i in range(size):
        cycle_type = str(col[i][0][0])
        keys = list(col[i][3][0].dtype.fields.keys())
        if cycle_type != "impedance":
            data_row = {}
            for j in range(len(keys)):
                t = col[i][3][0][0][j][0]
                l = [t[m] for m in range(len(t))]
                data_row[keys[j]] = l
            data_row["Cycle"] = i + 1
            data_row["Time"] = str(convert_to_time(col[i][2][0]))
            data.loc[i] = data_row
        meta_row = {}
        (
            meta_row["Cycle"],
            meta_row["Type"],
            meta_row["Ambient_temperature"],
            meta_row["Time"],
        ) = (
            i + 1,
            cycle_type,
            int(col[i][1][0]),
            str(convert_to_time(col[i][2][0])),
        )
        meta.append(meta_row)
    meta_df = pd.DataFrame(meta)
    meta_df.set_index("Cycle", inplace=True)
    data_df = pd.DataFrame(data)
    data_df.set_index("Cycle", inplace=True)
    return data_df, meta_df


if __name__ == "__main__":
    folder = r"1. BatteryAgingARC-FY08Q4"
    filename = r"B0005.mat"
    filepath = path.join(ORIGINAL_PATH, folder, filename)
    df, meta = mat_to_df(filepath)
    df.to_csv(path.join(GENERATED_PATH, folder, "B0005.csv"))
    meta.to_csv(path.join(GENERATED_PATH, folder, "B0005_meta.csv"))
