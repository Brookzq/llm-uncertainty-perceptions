import pandas as pd
import numpy as np

from collections import defaultdict
from scipy.stats import wasserstein_distance
from typing import Dict, List
from cpa import *


def absolute_error(dist1: dict, dist2: dict):
    assert dist1.keys() == dist2.keys()
    error = []
    for key in dist1:
        error.append(np.abs(dist1[key] - dist2[key]))
    return np.cumsum(error)[-1], error


def get_statistics_per_distribution(histogram: dict):
    maxs, mins, means, medians, uniques = {}, {}, {}, {}, {}
    for uncertainty, distribution in histogram.items():
        numbers, prob = zip(*distribution.items())
    
        for ix, cdf in enumerate(np.cumsum(prob)):
            if cdf >= 0.5 and uncertainty not in medians:
                medians[uncertainty] = numbers[ix]

        
        mean = 0
        for num, p in distribution.items():
            mean += float(num) * p
        means[uncertainty] = mean

        max_id = np.argmax(prob)
        maxs[uncertainty] = numbers[max_id]
        
        min_id = np.argmax(prob)
        mins[uncertainty] = numbers[min_id]
        
        uniques[uncertainty] = len(np.unique(prob))

        # TODO: IQR, spread
    
    return {
        "mean": means,
        "median": medians,
        "max": maxs,
        "min": mins,
        "num_unique": uniques,
    }


def assert_valid_prob(hist, axis=1, tol=1e-10):
    assert ((1-hist.sum(axis=axis)) <= tol).all()
    assert (np.abs(hist) >= -tol).all().all()
    assert (np.abs(hist) <= 1+tol).all().all()


def assert_same_exprs(test_hist: pd.DataFrame, ref_hist: pd.DataFrame):
    for t_expr, ref_expr in zip(test_hist.index, ref_hist.index):
        assert t_expr == ref_expr, f"Expression order mismatch: {t_expr} != {ref_expr}"


def compute_wasserstein_distance(
    model_df: pd.DataFrame,
    ref_df: pd.DataFrame,
    uncertainty_expressions: List[str],
) -> pd.DataFrame:
    assert_valid_prob(model_df)
    assert_same_exprs(model_df, ref_df)

    results = defaultdict(list)
    for expr in uncertainty_expressions:
        ref_expr_hist = [(float(k), p) for k, p in ref_df.loc[expr].to_dict().items()]
        model_expr_hist = [(float(k), p) for k, p in model_df.loc[expr].to_dict().items()]
    
        ref_expr_hist = sorted(ref_expr_hist, key=lambda x: x[0])
        model_expr_hist = sorted(model_expr_hist, key=lambda x: x[0])
        assert all([p[0] == q[0] for p, q in zip(ref_expr_hist, model_expr_hist)]), f"Number mismatch: {p} vs {q}"
    
        ref_values, ref_weights = zip(*ref_expr_hist)
        model_values, model_weights = zip(*model_expr_hist)
        
        results["uncertainty_expression"].append(expr)
        results["distance"].append(wasserstein_distance(
            u_values=ref_values, u_weights=ref_weights,
            v_values=model_values, v_weights=model_weights,
        ))
    
    return pd.DataFrame(results)