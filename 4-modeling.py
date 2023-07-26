from os import path
import pandas as pd
from src.config import paths
from src import model as mymodel


def train_model1(model, X, y, save_path, **kwargs):
    model.fit(X.values, y.values, **kwargs)
    model.save(save_path)
    print(f"Saved model to {save_path}")
    return model


def train_model2(model, X, y, save_path, **kwargs):
    model.fit(X.values, y["Cycle_number"].values, **kwargs)
    for layer in model.layers:
        layer.trainable = False
    model.add(mymodel.build_model2())
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    model.fit(y["Cycle_number"].values, y["Capacity"].values, **kwargs)
    model.save(save_path)
    print(f"Saved model to {save_path}")
    return model


if __name__ == "__main__":
    df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, "B0006.csv"))
    y1 = df["Capacity"]
    y2 = df[["Capacity", "Cycle_number"]]
    for col in ["Rectified_Impedance", "Re", "Rct"]:
        X1 = df[[col, "Cycle_number"]]
        X2 = df[[col]]
        model1 = mymodel.build_model1()
        model1_path = path.join(paths.MODELS_SAVE_PATH, f"model1_{col}")
        model1 = train_model1(model1, X1, y1, model1_path, epochs=100)
        model2 = mymodel.build_model2()
        model2_path = path.join(paths.MODELS_SAVE_PATH, f"model2_{col}")
        model2 = train_model2(model2, X2, y2, model2_path, epochs=100)
        print(model2.summary())
