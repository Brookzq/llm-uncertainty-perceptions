from typing import Dict, List, Tuple


# Auxiliary
def init_histograms(
        exprs: List[str],
        bins: List[int],
        fill_val=0,
    ) -> Dict[str, Dict[int, int]]:
    """Create a histogram centered around ``bins`` for each of the specified expressions."""
    return {exp: {b: fill_val for b in bins.tolist() + [-1]} for exp in exprs}


def get_bin_for_val(val: int, bin_center: List[int], bin_offset: float):
    """Obtain the bin for the specified value. 

    Considering the list of centered bins and their radi, determine
    the bin associated with the specified value ``val``. Except for
    the first bin, the algorithm considers intervals of the form
    [a, b), where the interval is left-closed and right-opened.
    """
    if val is None or val > bin_center[-1] or val < bin_center[0]:
        return -1
        
    lower_bounds = [bc - bin_offset for bc in bin_center]
    for i, lb in enumerate(lower_bounds):
        if val < lb:
            return max(0, bin_center[i-1])

    return bin_center[-1]
