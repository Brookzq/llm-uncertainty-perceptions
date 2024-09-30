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
