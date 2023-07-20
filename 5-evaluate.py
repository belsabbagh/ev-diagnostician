from os import path
import pandas as pd
from src.config import paths
from src.model import load_keras_model
from src import dataset_handler as dh

BATTERIES = ["B0006", "B0007", "B0048", "B0052", "B0055", "B0056"]

if __name__ == "__main__":
    model = load_keras_model("out/models/model1")
    results = {metric: [] for metric in model.metrics_names}
    results["Battery"] = []
    for b in BATTERIES:
        df = pd.read_csv(path.join(paths.PREPROCESSED_PATH, f"{b}.csv"))
        X, y = df[["Rectified_Impedance"]], df["Capacity"]
        res = model.evaluate(X.values, y.values)
        res = {k: v for k, v in zip(model.metrics_names, res)}
        results["Battery"].append(b)
        for metric in model.metrics_names:
            results[metric].append(res[metric])
    results = pd.DataFrame(results).set_index("Battery", inplace=False)
    res_path = path.join(paths.EVAL_RESULTS_PATH, "model1.csv")
    dh.save_to_csv(results, res_path)
    print(f"Finished evaluating model1 on {BATTERIES}. Results saved to {res_path}")
