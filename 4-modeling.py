from os import path
import pandas as pd
from src.config import paths
from src import dataset_handler as dh
from src import model

BATTERIES = ["B0005", "B0006", "B0007"]


def smoothen(values, window=10):
    return values.rolling(window=window).mean()


def train_model(model, X, y, save_path, **kwargs):
    model.fit(X.values, y.values, **kwargs)
    model.save(save_path)
    print(f"Saved model to {save_path}")
    return model


if __name__ == "__main__":
    df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, "B0005.csv"))
    X, y = df[["Rectified_Impedance"]], df["Capacity"]
    model = model.build_model1()
    model_path = path.join(paths.MODELS_SAVE_PATH, "model1")
    model = train_model(model, X, y, model_path, epochs=100)
    exit(0)
    df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, "impedance.csv"))
    df = df[df["Battery"].isin(BATTERIES)]
    X, y = df[["Rectified_Impedance"]], df["Capacity"]
    model1 = model.build_model1()
    model1_path = path.join(paths.MODELS_SAVE_PATH, "model2")
    train_model(model1, X, y, model1_path, epochs=100)
    df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, "discharge.csv"))
    df = df[df["Battery"].isin(BATTERIES)]
    X, y = dh.cycle_to_capacity(df)
    model2 = model.build_model2()
    model2_path = path.join(paths.MODELS_SAVE_PATH, "model2")
    train_model(model2, X, y, model2_path, epochs=100)
