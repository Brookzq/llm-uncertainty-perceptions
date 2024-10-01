import pandas as pd
import numpy as np

from typing import Dict, List, Tuple
from utils_base_histogram import init_histograms, get_bin_for_val


def create_histogram_humans(
    df: pd.DataFrame,
    number_col: str,
    unc_col: str,
    uncertainty_expressions: List[str],
    bin_center: float,
    bin_offset: float,
) -> Tuple[Dict[str, float]]:
    df = df[df[unc_col].isin(uncertainty_expressions)].copy()
    
    uhistograms = init_histograms(uncertainty_expressions, bin_center)
    bins = df[number_col].apply(get_bin_for_val, bin_center=bin_center, bin_offset=bin_offset)
    for u, b in zip(df[unc_col], bins):
        uhistograms[u][b] += 1

    # Normalized
    total = {u: len(df[df[unc_col] == u]) for u in uncertainty_expressions}
    #^Note: there are as many rows in the human subset as the number of annotations
    nhistograms = {u: {bc: cs / total[u] for bc, cs in uhistograms[u].items()} for u in uncertainty_expressions}

    return uhistograms, nhistograms


def create_histogram_for_top_k_logprobs__openai(
    df: pd.DataFrame,
    id_col: str,
    number_col: str,
    unc_col: str,
    uncertainty_expressions: List[str],
    bin_center: float,
    bin_offset: float,
) -> Tuple[Dict[str, float]]:
    # Select the subset of rows concerning the specified uncertainty expressions
    df = df[df[unc_col].isin(uncertainty_expressions)].copy()

    # Initialize the histogram
    uhistograms = init_histograms(uncertainty_expressions, bin_center)

    # Determine the bins
    bins = df[number_col].apply(get_bin_for_val, bin_center=bin_center, bin_offset=bin_offset)
    # Accumulate per bin
    for u, b in zip(df[unc_col], bins):
        uhistograms[u][b] += 1

    # Compute the number of unique statements (identified through id_col)
    total = {u: df[df[unc_col] == u][id_col].nunique() for u in uncertainty_expressions}

    # Normalized histograms
    nhistograms = {u: {bc: cs / total[u] for bc, cs in uhistograms[u].items()} for u in uncertainty_expressions}
    return uhistograms, nhistograms

    