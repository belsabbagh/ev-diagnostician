import numpy as np
import pandas as pd
from src.config import paths
from src import dataset_handler as dh
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def build_model():
    nn_model: Sequential = Sequential(
        [
            Dense(100, kernel_initializer="uniform", activation="tanh", input_dim=1),
            Dense(1, kernel_initializer="uniform", activation="linear"),
        ]
    )

    nn_model.compile(
        optimizer="sgd",
        loss="mean_squared_error",
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    return nn_model


def validate_data(df):
    nan_values = df.isna().any(axis=1)
    if nan_values.any():
        raise ValueError(f"NaN values found in {df[nan_values]}")
    return True


def collect_discharge_data():
    data_dict = {
        "Cycle": [],
        "Capacity": [],
        "Battery": [],
    }
    for battery_name, data in dh.battery_iter():
        batt_index, _ = data
        batt_index = batt_index.loc[batt_index["type"] == "discharge"]
        data_dict["Cycle"].extend(batt_index.index.values)
        data_dict["Capacity"].extend(batt_index["Capacity"].values)
        data_dict["Battery"].extend([battery_name] * len(batt_index))
    discharge_data = pd.DataFrame.from_dict(data_dict)
    discharge_data.sort_values(by=["Cycle", "Battery"], inplace=True)
    discharge_data.reset_index(inplace=True, drop=True)
    # validate_data(discharge_data)
    discharge_data.dropna(inplace=True)
    return pd.DataFrame.from_dict(discharge_data)


def split_data(df):
    return df.iloc[:, 0:1], df.iloc[:, 1]


if __name__ == "__main__":
    df = collect_discharge_data()
    X, y = split_data(df)
    nn_model = build_model()
    nn_model.fit(X.values, y.values, epochs=100)
    nn_model.save(paths.MODELS_SAVE_PATH)
