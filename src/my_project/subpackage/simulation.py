"""Lennard-Jones cluster molecular dynamics building blocks.

Geometry and dynamics utilities for a 2-D Lennard-Jones cluster simulated
under periodic boundary conditions with velocity-Verlet integration.
"""

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from numba import jit

__all__ = [
    "compute_forces_and_potential",
    "draw_config",
    "init_config",
    "plot_circle",
]

FloatArray = npt.NDArray[np.float64]


def plot_circle(center: FloatArray, radius: float) -> None:
    """Draw the outline of a circle on the current matplotlib axes.

    :param center: x and y coordinates of the circle's center.
    :type center: FloatArray
    :param radius: Radius of the circle.
    :type radius: float
    """
    npoints = 100
    theta = np.arange(0, 2 * np.pi + 1e-7, 2 * np.pi / npoints)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    plt.plot(x, y, "k", linewidth=2)


def draw_config(N: int, box_length: float, r: FloatArray) -> None:
    """Draw all particles and the periodic box boundary.

    Positions in ``r`` are wrapped into the primary box (in place) before
    being drawn, so callers who need the un-wrapped positions afterwards
    should pass a copy.

    :param N: Number of particles.
    :type N: int
    :param box_length: Length of one side of the periodic box.
    :type box_length: float
    :param r: Particle positions, shape ``(N, 2)``. Wrapped in place.
    :type r: FloatArray
    """
    plt.clf()
    for i in range(N):
        r[i, :] -= box_length * np.floor(r[i, :] / box_length + 0.5)
        plot_circle(r[i, :], 0.5)
    plt.axis("equal")
    plt.gca().set_adjustable("box")
    view_scale = 1.1 * box_length / 2
    plt.xlim(-view_scale, view_scale)
    plt.ylim(-view_scale, view_scale)

    boundary_x = box_length * (np.array([0, 1, 1, 0, 0]) - 0.5)
    boundary_y = box_length * (np.array([0, 0, 1, 1, 0]) - 0.5)
    plt.plot(boundary_x, boundary_y)

    plt.pause(0.01)


def init_config(N: int) -> FloatArray:
    """Create the initial configuration for a given number of particles.

    Particles are placed on a square lattice with unit spacing.

    :param N: Number of particles.
    :type N: int
    :return: Array of particle coordinates, shape ``(N, 2)``.
    :rtype: FloatArray
    """
    r = np.zeros((N, 2))

    # Determines how many particles need to be on a side to create a square
    # lattice of particles.
    n_side = int(np.sqrt(N) + 0.99)

    count = 0
    for row in range(n_side):
        for column in range(n_side):
            if count < N:
                r[count, :] = [row, column]
                count += 1
    return r


@jit(nopython=True)
def compute_forces_and_potential(
    N: int, r: FloatArray, box_length: float, r_cut_squared: float
) -> tuple[FloatArray, float, list[float]]:
    """Calculate inter-particle forces and total potential energy.

    Uses a shifted Lennard-Jones potential with periodic boundary
    conditions and a spherical cutoff.

    :param N: Number of particles.
    :type N: int
    :param r: Particle positions, shape ``(N, 2)``.
    :type r: FloatArray
    :param box_length: Length of one side of the periodic box.
    :type box_length: float
    :param r_cut_squared: Cutoff radius, squared.
    :type r_cut_squared: float
    :return: Forces on each particle (shape ``(N, 2)``), total potential
        energy of the system, and the list of inter-particle distances
        that fall within the cutoff.
    :rtype: tuple[FloatArray, float, list[float]]
    """
    forces = np.zeros((N, 2))
    potential = 0.0
    distances = []

    for i in range(N):
        for j in range(i + 1, N):
            dr = r[i, :] - r[j, :]
            # Shift by the box length for periodic boundaries.
            dr -= box_length * np.floor(dr / box_length + 0.5)
            dr2 = np.sum(dr * dr)

            # The potential is 0 when r > r_cut, so the force must be too.
            if dr2 <= r_cut_squared:
                # From the derivative of the potential; r_cut is a constant.
                force_factor = 48 * (dr2 ** (-7) - 0.5 * dr2 ** (-4))
                forces[i, :] += force_factor * dr
                forces[j, :] += force_factor * (-dr)
                distances.append(np.sqrt(dr2))

            dr2 = min(dr2, r_cut_squared)  # necessary for the shifted potential
            potential += 4 * (dr2 ** (-6) - dr2 ** (-3)) - 4 * (
                r_cut_squared ** (-6) - r_cut_squared ** (-3)
            )

    return forces, potential, distances
