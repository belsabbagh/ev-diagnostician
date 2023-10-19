import tensorflow as tf

Sequential = tf.keras.models.Sequential
load_model = tf.keras.models.load_model
layers = tf.keras.layers

DENSE_PROPS = {
    "kernel_initializer": "uniform",
    "activation": "linear",
}


def linear_layers():
    return [
        layers.Dense(4, **DENSE_PROPS),
        layers.Dense(2, **DENSE_PROPS),
        layers.Dense(1, **DENSE_PROPS),
    ]


def build_model1() -> Sequential:
    nn_model: Sequential = Sequential(
        [
            layers.InputLayer(input_shape=(2,)),
            *linear_layers(),
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
            *linear_layers(),
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
