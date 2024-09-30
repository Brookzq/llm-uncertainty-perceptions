import pandas as pd

from collections import defaultdict
from typing import Dict, List


def histogram_to_dataframe(
    expr_histograms: Dict[str, Dict[int, float]], 
    expr_order: List[str],
    unc_col: str,
    statistic: Dict[str, float]=None,
) -> pd.DataFrame:
    results = defaultdict(list)
    statistic_mask = defaultdict(list)
    
    if expr_order is not None:
        expr_histograms = {e: expr_histograms[e] for e in expr_order if e in expr_histograms}

    for expression, hist in expr_histograms.items():
        results[unc_col].append(expression)
        statistic_mask[unc_col].append(expression)
        
        for bin_name, bin_value in hist.items():
            if bin_name in ("-1", -1):
                continue
            results[round(float(bin_name))].append(bin_value)
            if statistic and statistic[expression] == bin_name:
                statistic_mask[round(float(bin_name))].append(1)
            else:
                statistic_mask[round(float(bin_name))].append(0)
                
    return (pd.DataFrame(results).set_index(unc_col), 
            pd.DataFrame(statistic_mask).set_index(unc_col))