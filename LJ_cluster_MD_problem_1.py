"""
Rachel Clune
CHEM 121 Spring 2023
Problem Set 12 Problem 1
Last Updated 4/16/23
"""

# import packages for basic math, plotting, linear algebra, etc.
from numpy import *
from numpy.linalg import *
from numpy.random import *
from matplotlib.pyplot import *

class histogram():
    def __init__(self,limits,binwidth):
        self.limits = limits
        self.binwidth = binwidth
        self.vals = arange(self.limits[0] + self.binwidth / 2, self.limits[1], self.binwidth)
        self.histo = 0 * self.vals
        self.N_samples = 0

    def add_sample(self,dat):
        self.N_samples += 1
        if dat > self.limits[0] and dat < self.limits[1]:
            bin_index = int((dat - self.limits[0]) / self.binwidth)
            self.histo[bin_index] += 1

    def normalize(self):
        self.histo = self.histo / (self.N_samples * self.binwidth)

    def barplot(self):
        bar(self.vals, self.histo, width=0.95 * self.binwidth, color='k')
        
    def lineplot(self):
        plot(self.vals, self.histo)

def plot_circle(center,radius):
    npoints = 100
    theta = arange(0,2*pi + 1e-7,2*pi/npoints)
    x = center[0] + radius*cos(theta)
    y = center[1] + radius*sin(theta)
    plot(x,y,'k',linewidth=2)

def draw_config(N, box_length, r):
    clf()
    for i in range(N):
        r[i,:] -= box_length * floor(r[i,:]/box_length + 0.5)
        plot_circle(r[i, :], 0.5)
    axis('equal')
    gca().set_adjustable("box")
    view_scale = 1.1 * box_length/2
    xlim(-view_scale, view_scale)
    ylim(-view_scale, view_scale)

    boundary_x = box_length * (array([0, 1, 1, 0, 0]) - 0.5)
    boundary_y = box_length * (array([0, 0, 1, 1, 0]) - 0.5)
    plot(boundary_x, boundary_y)

    pause(0.01)

def init_config(N):
    """
    creates the intial configuration for a given number of particles
    :param N: int, number of particles
    :return: 2-d array of particle coordinates
    """
    r = zeros((N, 2)) # placeholder

    # Determines how many particles need to be on a side to create a sqare lattice of particles
    n_side = int(sqrt(N) + 0.99)

    count = 0
    # fill in r with evenly spaced particles
    for row in range(n_side):
        for column in range(n_side):
            if count < N:
                r[count, :] = [row, column]
                count += 1
    return r

def calculate_g_of_r(hist, N, density, N_sweeps):
    """
    Calculates the radial distribution function from a histogram
    :param hist: histogram of inter-particle distances
    :param N: int, number of particles in the system
    :param density: float, density of the system
    :return: 1-d array of radial distribution function at different values of r
    """
    g = np.zeros(hist.histo.size)
    M_conf = (N_sweeps - N_sweeps*0.1)/10
    # using the center of each bin to represent r
    for ii in range(hist.vals.size):
        r = hist.vals[ii]
        g[ii] = hist.histo[ii]/(M_conf * pi * r * hist.binwidth * (N-1) * density)
    return g


################################################################################################
# parameters
################################################################################################
N = 36  # number of particles in the system
density = 0.7  # density of particles in the system
box_length = sqrt(N/density)  # size of the periodic box
r_cut = box_length/2  # cut off for the potential calculation
r_cut_squared = r_cut**2
delta_t = 0.01  # time step
total_time = 1000
N_steps = int(total_time/delta_t)  # total number of MD steps to take
T = 0.7  # (unitless) temperature of the system
k_coll = 1  # particle collision rate

# get initial configuration of particles
r = init_config(N)
v = zeros((N,2))
draw_config(N, box_length, np.copy(r))

from numba import jit
@jit(nopython=True)
def compute_forces_and_potential(N, r, box_length, r_cut_squared):
    """
    Calculates the inter-particle forces and total potential energy of the system at a given configuration
    :param N: int, number of particles
    :param r: 2-d array  of particle positions
    :param box_length: float, length of one side of the periodic box
    :param r_cut_squared: float, cutoff radius squared
    :return: 2-d array of x and y forces on each particle, total potential energy of the system (float),
                 1-d array of inter-particle distances
    """
    # place holders for the objects to be returned
    forces = zeros((N,2))
    potential = 0
    distances = []

    # calculate the forces keeping in mind that we are using periodic boundary conditions
    for i in range(N):
        for j in range(i+1,N):
            dr = r[i,:] - r[j,:]
            dr -= box_length * floor(dr/box_length + 0.5) # shifting the distances based on the box length, necessary for periodic boundaries
            dr2 = dr @ dr

            # since the potential is 0 when r> r_cut, the force must be too!
            if dr2 <= r_cut_squared:
                # force_factor equation is from derivative of potential, remember r_cut is a constant!
                force_factor = 48 * ( dr2**(-7) - 0.5 * dr2**(-4) )
                # the force between two particles should send them in opposing directions (either towards or away
                # from each other)
                forces[i,:] += force_factor * dr
                forces[j,:] += force_factor * (-dr)
                distances.append(sqrt(dr2))

            dr2 = min(dr2, r_cut_squared) # necessary for the shifted potential
            potential += 4 * ( dr2**(-6) - dr2**(-3) ) - 4 * (r_cut_squared**(-6) - r_cut_squared**(-3))

    return forces, potential, distances


# calculate the forces on the initial system
forces, potential_energy, distances = compute_forces_and_potential(N, r, box_length, r_cut_squared)

# initialize histogram, arrays to hold the kinetic and potential energies at each step
hist = histogram(limits=[0, 3.6], binwidth=0.01)
kinetic_traj = zeros(N_steps)
potential_traj = zeros(N_steps)

# run the MD simulation using the velocity Verlet algorithm
for step in range(N_steps):
    v = v + 0.5 * delta_t * forces
    r = r + delta_t * v
    forces, potential_energy, distances = compute_forces_and_potential(N, r, box_length, r_cut_squared)
    v = v + 0.5 * delta_t * forces

    # fill histogram every tenth step, but leave out the first 10% of the steps
    if step % 10 == 0 and step > N_steps*0.1:
        for rij in distances:
            hist.add_sample(rij)

    kinetic_energy = 0.5 * sum( v**2 )
    kinetic_traj[step] = kinetic_energy
    potential_traj[step] = potential_energy

    # Andersen thermostat, used to modulate the temperature of the syste,
    for i in range(N):
        if rand() < k_coll * delta_t:
            speed = sqrt(-2 * T * log(rand()) )
            angle = 2 * pi * rand()
            v[i,:] = speed * array([cos(angle), sin(angle)])

    if step % 1000 == 0:
        draw_config(N, box_length, np.copy(r))

# radial distribution function
rdf = calculate_g_of_r(hist, N, density, N_steps)

# plot and save the radial distribution function
clf()
plot(hist.vals, rdf)
xlabel("r")
ylabel("g(r)")
xlim((0, box_length/2))
title("Problem 1(iii): Radial distribution function")
savefig("PS12_problem1iii_radial_dis_func.png")
show()