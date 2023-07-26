import tensorflow as tf

Sequential = tf.keras.models.Sequential
load_model = tf.keras.models.load_model
layers = tf.keras.layers

DENSE_PROPS = {
    "kernel_initializer": "uniform",
    "activation": "linear",
}


def build_model1() -> Sequential:
    nn_model: Sequential = Sequential(
        [
            layers.InputLayer(input_shape=(2,)),
            layers.Dense(4, **DENSE_PROPS),
            layers.Dense(1, **DENSE_PROPS),
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
            layers.InputLayer(input_shape=(1,)),
            layers.Dense(4, activation="linear", kernel_initializer="uniform"),
            layers.Dense(1, activation="linear", kernel_initializer="uniform"),
        ]
    )

    nn_model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error", "mean_squared_error"],
    )
    return nn_model


def load_keras_model(model_path: str) -> Sequential:
    return load_model(model_path)
