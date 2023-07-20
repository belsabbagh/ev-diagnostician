import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import layers


def build_model1() -> Sequential:
    nn_model: Sequential = Sequential(
        [
            layers.Dense(
                2, kernel_initializer="uniform", activation="linear", input_dim=1
            ),
            layers.Dense(1, kernel_initializer="uniform", activation="linear"),
        ]
    )

    nn_model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    return nn_model


def build_model2() -> Sequential:
    nn_model: Sequential = Sequential(
        [
            layers.Dense(
                100, kernel_initializer="uniform", activation="tanh", input_dim=1
            ),
            layers.Dense(1, kernel_initializer="uniform", activation="linear"),
        ]
    )

    nn_model.compile(
        optimizer="sgd",
        loss="mean_squared_error",
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    return nn_model


def load_keras_model(model_path: str) -> Sequential:
    return load_model(model_path)


def predict(models, X):
    pred_cycle = models[0].predict(X)  # [models[0].predict(i)[0][0] for i in X.values]
    pred_cycle = pd.DataFrame.from_dict({"Cycle": pred_cycle})
    return [models[1].predict(i)[0][0] for i in pred_cycle.values]
