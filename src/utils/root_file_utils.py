import hist
from hist import Hist, loc, rebin
import numpy as np
import matplotlib.pyplot as plt



def hist2d_to_hist1d_shells(
    hist_obj: Hist,
    shell_axis: int,
    binned_axis: int,
    shell_min: float,
    shell_max: float,
    shell_step: float,
    xlabel: str,
    ylabel: str,
    title: str,
):
    """
    Returns a plot with multiple 1D histograms from slicing a 2D histogram. 
    
    :param hist_obj     : Description
    :param shell_axis   : Description
    :param binned_axis  : Description
    :param shell_min    : Description
    :param shell_max    : Description
    :param shell_step   : Description
    :param xlabel       : Description
    :param ylabel       : Description
    :param title        : Description
    """
    # Bin centers of the axis we plot
    edges = hist_obj.axes[binned_axis].edges
    centers = 0.5 * (edges[:-1] + edges[1:])

    # Generate shell ranges
    shells = [
        (lo, lo + shell_step)
        for lo in np.arange(shell_min, shell_max, shell_step)
    ]

    plt.figure(figsize=(7, 4))

    for (lo, hi) in shells:
        # Build slice object dynamically
        # Ex: if hist dimensions is 2 -> slicer == [slice(None), slice(None)] == [:, :]
        slicer = [slice(None)] * hist_obj.ndim

        # Replace the shell axis slicer position with the shell range
        # Ex: if shell axis is 0 -> slicer == [loc(lo):loc(hi), :]
        slicer[shell_axis] = slice(loc(lo), loc(hi))

        h_slice = hist_obj[tuple(slicer)]

        # Collapse shell axis -> 1D histogram of binned-axis variable within a shell of the shell-axis variable
        counts = h_slice.values().sum(axis=shell_axis)

        # Plot 1D histogram shell
        plt.step(
            centers,
            counts,
            where="mid",
            label=f"{lo}–{hi}"
        )

    # Label figure with plotted histogram shells
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
# End function


def rebin_hist(
    hist_obj,
    factors=None,
    new_bins=None
):
    """
    Rebin multiple axes of a hist.Hist.
    Rebin either by merging bins by a factor, or by specifying the number of bins.
    If a number of new bins is given, it must factor into the existing bins.

    Parameters
    ----------
    hist_obj : hist.Hist

    factors : dict[int, int], optional
        {axis: merge_factor}

    new_bins : dict[int, int], optional
        {axis: target_bin_count}

    Returns
    -------
    hist.Hist
    """

    if factors is None:
        factors = {}

    # Rebin by consolidating old bins into number of new bins.
    if new_bins is not None:
        # Rebin each axis specified.
        for ax, nb in new_bins.items():
            # Get original number of bins for this axis.
            old = hist_obj.axes[ax].size
            # Check that new bins evenly divide into old bins.
            if old % nb != 0:
                raise ValueError(f"Axis {ax}: new_bins must divide existing bins")
            # Get the factor.
            factors[ax] = old // nb

    # Rebin along specified axes by factor.
    slicer = [slice(None)] * hist_obj.ndim

    for ax, factor in factors.items():
        slicer[ax] = rebin(factor)

    return hist_obj[tuple(slicer)]
# End function.





