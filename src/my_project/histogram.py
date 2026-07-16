"""Histogram accumulation and radial distribution function calculation."""

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

__all__ = [
    "Histogram",
    "calculate_g_of_r",
]

FloatArray = npt.NDArray[np.float64]


class Histogram:
    """Accumulates samples into a fixed-width histogram over a bounded range.

    :param limits: Lower and upper bound of the histogram range.
    :type limits: tuple[float, float]
    :param binwidth: Width of each histogram bin.
    :type binwidth: float
    """

    def __init__(self, limits: tuple[float, float], binwidth: float) -> None:
        self.limits = limits
        self.binwidth = binwidth
        self.vals: FloatArray = np.arange(
            limits[0] + binwidth / 2, limits[1], binwidth
        )
        self.histo: FloatArray = np.zeros_like(self.vals)
        self.N_samples = 0

    def add_sample(self, dat: float) -> None:
        """Add a single sample to the histogram.

        Samples outside ``limits`` are counted towards ``N_samples`` but
        are not binned.

        :param dat: Value to bin.
        :type dat: float
        """
        self.N_samples += 1
        if self.limits[0] < dat < self.limits[1]:
            bin_index = int((dat - self.limits[0]) / self.binwidth)
            self.histo[bin_index] += 1

    def normalize(self) -> None:
        """Normalize the accumulated counts into a probability density."""
        self.histo = self.histo / (self.N_samples * self.binwidth)

    def barplot(self) -> None:
        """Plot the histogram as a bar chart on the current axes."""
        plt.bar(self.vals, self.histo, width=0.95 * self.binwidth, color="k")

    def lineplot(self) -> None:
        """Plot the histogram as a line plot on the current axes."""
        plt.plot(self.vals, self.histo)


def calculate_g_of_r(
    hist: Histogram, N: int, density: float, N_sweeps: int
) -> FloatArray:
    """Calculate the radial distribution function from a histogram.

    :param hist: Histogram of inter-particle distances.
    :type hist: Histogram
    :param N: Number of particles in the system.
    :type N: int
    :param density: Density of the system.
    :type density: float
    :param N_sweeps: Total number of sampling sweeps the histogram was
        built from.
    :type N_sweeps: int
    :return: Radial distribution function evaluated at each bin center.
    :rtype: FloatArray
    """
    g = np.zeros(hist.histo.size)
    M_conf = (N_sweeps - N_sweeps * 0.1) / 10
    # Use the center of each bin to represent r.
    for ii in range(hist.vals.size):
        r = hist.vals[ii]
        g[ii] = hist.histo[ii] / (M_conf * np.pi * r * hist.binwidth * (N - 1) * density)
    return g
