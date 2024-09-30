import glob, json, os
import pandas as pd
from typing import Dict


def print_sep(*msgs):
    print("\n", "+" * 80)
    print(*msgs)
    print("+" * 80, "\n")


def read_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def to_json(data: dict, path: str):
    assert ".json" in path
    os.makedirs(path.rpartition("/")[0], exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def to_csv(data: dict, path: str):
    assert ".csv" in path
    os.makedirs(path.rpartition("/")[0], exist_ok=True)
    pd.DataFrame(data).T.to_csv(path)


def persist_histograms(unnorm_hist: Dict[str, Dict[str, int]], norm_hist: Dict[str, Dict[str, float]], results_folder: str, prefix=""):
    basename = prefix + "_" if prefix else ""
    
    to_csv(unnorm_hist, f"{results_folder}/{basename}unnormalized.csv")
    to_json(unnorm_hist, f"{results_folder}/{basename}unnormalized.json")

    # Normalized 
    to_csv(norm_hist, f"{results_folder}/{basename}normalized.csv")
    to_json(norm_hist, f"{results_folder}/{basename}normalized.json")

