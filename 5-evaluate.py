from os import path
import pandas as pd
from src.config import paths
from src.model import load_keras_model
from src import dataset_handler as dh

BATTERIES = ["B0005", "B0018", "B0026"]


def score(model, X, y):
    return {
        k: v for k, v in zip(model.metrics_names, model.evaluate(X.values, y.values))
    }


def model_iter():
    for model in ["model1", "model2"]:
        for col in ["Rectified_Impedance", "Re", "Rct"]:
            yield f"{model}_{col}"


if __name__ == "__main__":
    for model_name in model_iter():
        model = load_keras_model(f"out/models/{model_name}")
        name, column = model_name.split("_", 1)
        results = {metric: [] for metric in model.metrics_names}
        results["Battery"] = []
        for b in BATTERIES:
            df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, f"{b}.csv"))
            X, y = (
                df[[column, "Cycle_number"]] if name == "model1" else df[[column]],
                df["Capacity"]
                if name == "model1"
                else df[["Capacity", "Cycle_number"]],
            )
            res = score(model, X, y)
            results["Battery"].append(b)
            for metric in model.metrics_names:
                results[metric].append(res[metric])
        results = pd.DataFrame(results).set_index("Battery", inplace=False)
        res_path = path.join(paths.EVAL_RESULTS_PATH, f"{model_name}.csv")
        dh.save_to_csv(results, res_path)
        print(
            f"Finished evaluating {model_name} on {BATTERIES}. Results saved to {res_path}"
        )
