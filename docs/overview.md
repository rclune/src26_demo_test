# Overview

Welcome to the documentation for `my_project`!
`my_project` is a small 2-D Lennard-Jones cluster molecular dynamics example, used here to demonstrate this documentation and testing template.

If you want to see how a scientific Python package can document its API with Sphinx and test its numerics with PyTest, this project shows a minimal but complete example: initializing a particle configuration, computing pairwise forces and potential energy under periodic boundary conditions, and analyzing the resulting structure with a radial distribution function.

The module has two parts:

- `my_project.subpackage.simulation`: builds an initial square-lattice configuration, computes Lennard-Jones forces and potential energy (accelerated with Numba), and renders the particle configuration and periodic box.
- `my_project.histogram`: accumulates samples into a histogram and computes the radial distribution function, *g(r)*, from it.

New users should start with the [API Reference](api/generated/my_project.rst) to see the available classes and functions, then look at `tests/test_my_project.py` for examples of how each piece is used.
