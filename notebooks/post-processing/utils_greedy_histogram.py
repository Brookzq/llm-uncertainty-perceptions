import pandas as pd
import numpy as np

from collections import defaultdict
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


def create_histogram_for_full_logprobs__hf(
    df: pd.DataFrame,
    id_cols: List[str],
    number_col: List[str],
    number_logprob_col: List[str],
    unc_col: str,
    uncertainty_expressions: List[str],
    bin_center: List[float],
    bin_offset: float,
) -> Tuple[Dict[str, float]]:
    # Select the subset of rows concerning the specified uncertainty expressions
    df = df[df[unc_col].isin(uncertainty_expressions)].copy()

    # Initialize the histogram
    uhistograms = init_histograms(uncertainty_expressions, bin_center)

    # Preprocess the dataframe to determine the argmax value for each
    # id_col
    uniq_ids2max = defaultdict(lambda: (-1, -np.inf))
    # ^Note: uniq_ids2max represents a mapping from 
    # the unique id of an example to a tuple with
    #   * num: representing the current argmax
    #   * num_logprob: representing the current max logprob
    for row_ix, example in df.iterrows():        
        id_example = tuple(example[col] for col in id_cols + [unc_col])

        # obtain the previous max value
        prev_max_num, prev_max_num_logprob = uniq_ids2max[id_example]

        if prev_max_num_logprob < example[number_logprob_col]:
            new_num = float(example[number_col])
            new_num_logprob = example[number_logprob_col]
            uniq_ids2max[id_example] = (new_num, new_num_logprob)

    for unique_ids, (argmax, _) in uniq_ids2max.items():
        unc_expr = unique_ids[-1]
        bn = get_bin_for_val(argmax, bin_center, bin_offset)
        assert -1 <= bn <= 100, f"{argmax} was assigned to bin: {bn}"
        uhistograms[unc_expr][bn] += 1

    total_mass_uhist = {u: np.sum(list(uhistograms[u].values())) 
                        for u in uncertainty_expressions}
    min_uhist = min(total_mass_uhist.values())
    max_uhist = max(total_mass_uhist.values())
    assert np.abs(max_uhist - min_uhist) <= 1e-6, f"Bug detected: {max_uhist}, {min_uhist}"

    # Normalized histograms
    nhistograms = {u: {bc: cs / total_mass_uhist[u] 
                       for bc, cs in uhistograms[u].items()} for u in uncertainty_expressions}
    return uhistograms, nhistograms


def create_histogram_for_sampling_approach(
    df: pd.DataFrame, 
    number_col: str, 
    unc_col: str, 
    id_cols: List[str], 
    uncertainty_expressions: list, 
    bin_center: List[float],
    bin_offset: float,
    ok_non_symmetric: bool=False,
) -> Tuple[Dict[str, float]]:
    # Select the subset of rows concerning the specified uncertainty expressions
    df = df[df[unc_col].isin(uncertainty_expressions)]

    # Initialize the histogram
    uhistograms = init_histograms(uncertainty_expressions, bin_center)

    # Preprocess the dataframe to count values for each expression
    unique_ids2counts = defaultdict(lambda: defaultdict(lambda: 0))
    # ^Note:  unique_ids2counts represents a mapping from 
    # the unique id of an example to a number counter
    for row_ix, example in df.iterrows():        
        id_example = tuple(example[col] for col in id_cols + [unc_col])
        num = example[number_col] 
        num = -1 if num is None else num
        unique_ids2counts[id_example][num] += 1

    # collect the max
    for unique_ids, counter in unique_ids2counts.items():
        unc_expr = unique_ids[-1]
        argmax, count_max = sorted(counter.items(), key=lambda x: x[1], reverse=True)[0]
        bn = get_bin_for_val(argmax, bin_center, bin_offset)
        assert -1 <= bn <= 100, f"{argmax} was assigned to bin: {bn}"
        uhistograms[unc_expr][bn] += 1

    total_mass_uhist = {u: np.sum(list(uhistograms[u].values())) 
                        for u in uncertainty_expressions}
    min_uhist = min(total_mass_uhist.values())
    max_uhist = max(total_mass_uhist.values())
    assert ok_non_symmetric or np.abs(max_uhist - min_uhist) <= 1e-6, f"Bug detected: {max_uhist}, {min_uhist}"

    # Normalized histograms
    nhistograms = {u: {bc: cs / total_mass_uhist[u] 
                       for bc, cs in uhistograms[u].items()} for u in uncertainty_expressions}
    return uhistograms, nhistograms
