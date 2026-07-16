"""Tests for the ``my_project`` Lennard-Jones cluster MD utilities."""

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

import my_project
from my_project import Histogram, calculate_g_of_r
from my_project.subpackage import (
    compute_forces_and_potential,
    draw_config,
    init_config,
    plot_circle,
)


class TestHistogram:
    """Tests for :class:`my_project.Histogram`."""

    def test_bin_centers_span_the_requested_range(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        assert np.allclose(hist.vals, [0.25, 0.75])
        assert np.allclose(hist.histo, [0.0, 0.0])
        assert hist.N_samples == 0

    def test_add_sample_increments_the_matching_bin(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        hist.add_sample(0.1)
        hist.add_sample(0.6)
        hist.add_sample(0.6)
        assert list(hist.histo) == [1.0, 2.0]
        assert hist.N_samples == 3

    def test_add_sample_outside_limits_is_counted_but_not_binned(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        hist.add_sample(5.0)
        assert list(hist.histo) == [0.0, 0.0]
        assert hist.N_samples == 1

    def test_normalize_divides_by_samples_and_binwidth(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        hist.add_sample(0.1)
        hist.add_sample(0.6)
        hist.normalize()
        assert np.allclose(hist.histo, [1.0, 1.0])

    def test_barplot_and_lineplot_do_not_raise(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        hist.add_sample(0.1)
        hist.barplot()
        hist.lineplot()


class TestCalculateGOfR:
    """Tests for :func:`my_project.calculate_g_of_r`."""

    def test_empty_histogram_gives_zero_everywhere(self):
        hist = Histogram(limits=(0.0, 1.0), binwidth=0.5)
        g = calculate_g_of_r(hist, N=10, density=0.7, N_sweeps=1000)
        assert np.allclose(g, 0.0)

    def test_result_has_one_value_per_bin(self):
        hist = Histogram(limits=(0.0, 3.6), binwidth=0.01)
        g = calculate_g_of_r(hist, N=36, density=0.7, N_sweeps=1000)
        assert g.shape == hist.vals.shape


class TestInitConfig:
    """Tests for :func:`my_project.init_config`."""

    def test_places_particles_on_a_square_lattice(self):
        r = init_config(4)
        assert np.array_equal(r, [[0, 0], [0, 1], [1, 0], [1, 1]])

    def test_returns_the_requested_number_of_particles(self):
        r = init_config(5)
        assert r.shape == (5, 2)

    def test_zero_particles_gives_an_empty_array(self):
        r = init_config(0)
        assert r.shape == (0, 2)


class TestPlotCircleAndDrawConfig:
    """Tests for :func:`my_project.plot_circle` and :func:`my_project.draw_config`."""

    def test_plot_circle_does_not_raise(self):
        plot_circle(np.array([0.0, 0.0]), radius=0.5)

    def test_draw_config_does_not_raise(self):
        r = init_config(4)
        draw_config(4, box_length=3.0, r=r)

    def test_draw_config_wraps_positions_into_the_box_in_place(self):
        r = np.array([[10.0, 10.0]])
        draw_config(1, box_length=3.0, r=r)
        assert np.all(np.abs(r) <= 1.5)


class TestComputeForcesAndPotential:
    """Tests for :func:`my_project.compute_forces_and_potential`."""

    def test_forces_are_equal_and_opposite(self):
        r = np.array([[0.0, 0.0], [1.0, 0.0]])
        forces, _, _ = compute_forces_and_potential(2, r, box_length=10.0, r_cut_squared=9.0)
        assert np.allclose(forces[0], -forces[1])

    def test_no_force_beyond_the_cutoff(self):
        r = np.array([[0.0, 0.0], [5.0, 0.0]])
        forces, potential, distances = compute_forces_and_potential(
            2, r, box_length=20.0, r_cut_squared=4.0
        )
        assert np.allclose(forces, 0.0)
        assert distances == []

    def test_periodic_boundary_wraps_the_shortest_distance(self):
        # Separated by 0.1 across the periodic boundary of a box of length 1,
        # not by the naive 0.9 within the box.
        r = np.array([[0.0, 0.0], [0.9, 0.0]])
        forces, _, distances = compute_forces_and_potential(
            2, r, box_length=1.0, r_cut_squared=0.09
        )
        assert distances == pytest.approx([0.1])
        assert not np.allclose(forces, 0.0)
