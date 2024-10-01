import pandas as pd
import numpy as np

from scipy.special import logsumexp
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
    raise NotImplementedError("Not implemented yet")


def create_histogram_for_top_k_logprobs__openai(
    df: pd.DataFrame,
    id_col: str,
    number_cols: List[str],
    number_logprob_cols: List[str],
    unc_col: str,
    uncertainty_expressions: List[str],
    bin_center: float,
    bin_offset: float,
    ok_non_symmetric: bool=False,
) -> Tuple[Dict[str, float]]:
    assert len(number_cols) == len(number_logprob_cols)
    # Select the subset of rows concerning the specified uncertainty expressions
    df = df[df[unc_col].isin(uncertainty_expressions)].copy()

    # Initialize the histogram
    uhistograms = init_histograms(uncertainty_expressions, bin_center)
    # --- ------ ------ ------ ------ ------ ------ ------ ---
    # Iterate each row of the dataframe
    # --- ------ ------ ------ ------ ------ ------ ------ ---
    # Each row concerns a single model inference, which means
    # that all necessary probability information is represented 
    # in a single row. To facilitate the normalization per 
    # example we will iterate each row, assigning the remaining
    # probability to -1.
    # ----------------------------------------------------------
    accumulator = 0
    for row_ix, example in df.iterrows():
        unc_expr = example[unc_col]

        # Determine the association between predicted response
        # and the associated probability
        cols = [(col, logprob) 
            for col, logprob in zip(number_cols, number_logprob_cols)
            if not np.isnan(example[col]) # remove cols for which no log prob is observed
        ]
        if len(cols) > 0:
            num2logprob = {float(example[num_col]): example[num_logprob]
                for num_col, num_logprob in cols
            }
            
            # Compute the remaining probability (that is not assigned within the top k probs)
            logprob_defined = logsumexp(list(num2logprob.values()))
            prob_remaining = 1 - np.exp(logprob_defined)
            assert 0-1e-7 <= prob_remaining <= 1+1e-7, f"{prob_remaining}"
            prob_remaining = max(0, min(1, prob_remaining))
            # Sanity check that this adds to 1
            val = np.exp(logprob_defined) + prob_remaining
            assert np.abs(val - 1) <= 1e-7, f"Does not add to 1: {val}"
        else:
            num2logprob = {}
            prob_remaining = 1
        
        # For each number, get its binn and accumulate its probability
        for num, logprob in num2logprob.items():
            bn = get_bin_for_val(num, bin_center, bin_offset)
            assert -1 <= bn <= 100, f"{num} was assigned to bin: {bn}"
            uhistograms[unc_expr][bn] += np.exp(logprob)
        uhistograms[unc_expr][-1] += prob_remaining
        
    # Sanity check (verify that we've accumulated the expressions)
    total = {u: df[df[unc_col] == u][id_col].nunique() for u in uncertainty_expressions}

    total_mass_uhist = {u: np.sum(list(uhistograms[u].values())) for u in uncertainty_expressions}
    min_uhist = min(total_mass_uhist.values())
    max_uhist = max(total_mass_uhist.values())
    assert ok_non_symmetric or np.abs(max_uhist - min_uhist) <= 1e-6, f"Bug detected: {max_uhist}, {min_uhist}"

    for u in uncertainty_expressions:
        assert np.abs(total[u]-total_mass_uhist[u]) <= 1e-6, f"Bug detected: {np.abs(total[u]-total_mass_uhist[u])}"
    
    # Normalized histograms
    nhistograms = {u: {bc: cs / total_mass_uhist[u] for bc, cs in uhistograms[u].items()} for u in uncertainty_expressions}
    return uhistograms, nhistograms



    