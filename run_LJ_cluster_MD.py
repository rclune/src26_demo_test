"""Recreates the simulation in ``LJ_cluster_MD_problem_1.py`` using the
``my_project`` package API.
"""

import numpy as np
import matplotlib.pyplot as plt

from my_project import Histogram, calculate_g_of_r
from my_project.subpackage import (
    compute_forces_and_potential,
    draw_config,
    init_config,
)

# parameters
N = 36  # number of particles in the system
density = 0.7  # density of particles in the system
box_length = np.sqrt(N / density)  # size of the periodic box
r_cut = box_length / 2  # cut off for the potential calculation
r_cut_squared = r_cut**2
delta_t = 0.01  # time step
total_time = 1000
N_steps = int(total_time / delta_t)  # total number of MD steps to take
T = 0.7  # (unitless) temperature of the system
k_coll = 1  # particle collision rate

# get initial configuration of particles
r = init_config(N)
v = np.zeros((N, 2))
draw_config(N, box_length, np.copy(r), save=True, save_dir="for_gif")

# calculate the forces on the initial system
forces, potential_energy, distances = compute_forces_and_potential(N, r, box_length, r_cut_squared)

# initialize histogram, arrays to hold the kinetic and potential energies at each step
hist = Histogram(limits=(0, 3.6), binwidth=0.01)
kinetic_traj = np.zeros(N_steps)
potential_traj = np.zeros(N_steps)

# run the MD simulation using the velocity Verlet algorithm
for step in range(N_steps):
    v = v + 0.5 * delta_t * forces
    r = r + delta_t * v
    forces, potential_energy, distances = compute_forces_and_potential(N, r, box_length, r_cut_squared)
    v = v + 0.5 * delta_t * forces

    # fill histogram every tenth step, but leave out the first 10% of the steps
    if step % 10 == 0 and step > N_steps * 0.1:
        for rij in distances:
            hist.add_sample(rij)

    kinetic_energy = 0.5 * np.sum(v**2)
    kinetic_traj[step] = kinetic_energy
    potential_traj[step] = potential_energy

    # Andersen thermostat, used to modulate the temperature of the system
    for i in range(N):
        if np.random.rand() < k_coll * delta_t:
            speed = np.sqrt(-2 * T * np.log(np.random.rand()))
            angle = 2 * np.pi * np.random.rand()
            v[i, :] = speed * np.array([np.cos(angle), np.sin(angle)])

    if step % 1000 == 0:
        draw_config(N, box_length, np.copy(r), save=True, save_dir="for_gif")

# radial distribution function
rdf = calculate_g_of_r(hist, N, density, N_steps)

# plot and save the radial distribution function
plt.clf()
plt.plot(hist.vals, rdf)
plt.xlabel("r")
plt.ylabel("g(r)")
plt.xlim((0, box_length / 2))
plt.title("Problem 1(iii): Radial distribution function")
plt.savefig("PS12_problem1iii_radial_dis_func.png")
plt.show()
