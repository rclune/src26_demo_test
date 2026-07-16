This repository will be used for an in-person demonstration to show off the uses of this template repository. The original template repository can be found here: https://github.com/omsf/OMSF_docs_template. It contains a sample python module and documentation (using Sphinx) and testing (with PyTest) infrastructure. The goal is to change/append to the existing infrastructure as little as possible. Files will be added to the `/docs/` directory, tests will be added to the `/tests/` directory, and the example module will be replaced with a different example, but the infrastructure that is in place to build the docs and run the tests should not be touched unless absolutely necessary. 

Keep everything concise and prioritize clarity. Any added python code should have type hints, all functions/classes/etc. should have docstrings in the reStructuredText format. Follow existing patterns exactly. Tests should be run via `uv run pytest`. Tests should cover all behaviors, including edge cases and errors. All new features require tests. Use PEP8 code style where applicable. 

## Module Overview

`src/my_project` implements a 2-D Lennard-Jones cluster molecular dynamics example.

- `my_project.histogram`: `Histogram` accumulates samples into a fixed-width histogram and can plot as a bar or line chart; `calculate_g_of_r` computes the radial distribution function from a histogram.
- `my_project.subpackage.simulation`: `init_config` builds an initial square-lattice configuration; `compute_forces_and_potential` (Numba-jitted) computes inter-particle forces, potential energy, and pairwise distances under periodic boundary conditions with a Lennard-Jones cutoff; `draw_config` and `plot_circle` render the particle configuration and periodic box.

Coding Best Practices:
- Early Returns: Use to avoid nested conditions
- Descriptive Names: Use clear variable/function names (prefix handlers with "handle")
- Constants Over Functions: Use constants where possible
- DRY Code: Don't repeat yourself
- Functional Style: Prefer functional, immutable approaches when not verbose
- Minimal Changes: Only modify code related to the task at hand
- Function Ordering: Define composing functions before their components
- TODO Comments: Mark issues in existing code with "TODO:" prefix
- Simplicity: Prioritize simplicity and readability over clever solutions
- Build Iteratively Start with minimal functionality and verify it works before adding complexity
- Run Tests: Test your code frequently with realistic inputs and validate outputs
- Build Test Environments: Create testing environments for components that are difficult to validate directly
- Functional Code: Use functional and stateless approaches where they improve clarity
- Clean logic: Keep core logic clean and push implementation details to the edges
- File Organsiation: Balance file organization with simplicity - use an appropriate number of files for the project scale