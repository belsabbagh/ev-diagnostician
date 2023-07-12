import pandas as pd
from datetime import datetime
import numpy as np
import scipy.io
from os import path


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


def loadMat(filepath):
    data = scipy.io.loadmat(filepath)
    filename = path.basename(filepath).split(".")[0]
    col = data[filename]
    col = col[0][0][0][0]
    size = col.shape[0]
    data = []
    for i in range(size):
        k = list(col[i][3][0].dtype.fields.keys())
        d1, d2 = {}, {}
        cycle_type = str(col[i][0][0])
        for j in range(len(k)):
            t = col[i][3][0][0][j][0]
            l = [t[m] for m in range(len(t))]
            d2[k[j]] = l
        d1["type"], d1["temp"], d1["time"], d1["data"] = (
            cycle_type,
            int(col[i][1][0]),
            str(convert_to_time(col[i][2][0])),
            d2,
        )
        data.append(d1)

    return np.array(data)


def mat_to_df(mat):
    batt = pd.DataFrame(
        columns=[
            "cycle",
            "type",
            "ambient_temperature",
            "time",
            "Capacity",
            "Battery_impedance",
            "Rectified_Impedance",
            "Re",
            "Rct",
        ]
    )
    batt.set_index("cycle", inplace=True)
    cycles = []
    for i, d in enumerate(mat):
        cycle_num = i
        cycle_type = d["type"]
        row, data = [d["type"], d["temp"], d["time"], *[np.nan] * 5], d["data"]
        match cycle_type:
            case "discharge":
                row[3] = data["Capacity"][0] if len(data["Capacity"]) == 1 else np.nan
                if len(data["Capacity"]) > 1:
                    print(f"Warning: {cycle_num} has multiple capacity values")
                del data["Capacity"]
            case "impedance":
                data, other = split_dict_by_keys(
                    data, ["Sense_current", "Battery_current", "Current_ratio"]
                )
                row[4:] = list(other.values())
        batt.loc[cycle_num] = row
        df = pd.DataFrame.from_dict(data)
        if cycle_type != "impedance":
            df.set_index("Time", inplace=True)
        cycles.append(df)
    return batt, cycles


def split_dict_by_keys(d, keys):
    return {k: d[k] for k in keys}, {k: d[k] for k in d if k not in keys}
