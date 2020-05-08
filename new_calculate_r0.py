import numpy as np
from graph_tool.generation import price_network, geometric_graph
from graph_tool.dynamics import SIRState
from graph_tool import infect_vertex_property
import matplotlib.pyplot as plt

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

print('Imported all libraries')

def coinflips(p, n = None):
    """Return True with probability p and False otherwise."""
    return np.random.random(n) < p

def prune(g, patient_zero, t):
    """Remove all vertices in g that have distance >t from patient_zero."""
    keep = g.new_vertex_property('bool', False)
    keep.a[patient_zero] = True
    for _ in range(t):
        # For all vertices in 'keep', also add their neighbours
        infect_vertex_property(g, keep, vals=[True])
    g.set_vertex_filter(keep)

def unprune(g):
    """Restore all vertices in g."""
    g.set_vertex_filter(None)

def SIRmodel(g, patient_zero, beta, gamma):
    """
    Runs a standard SIR model on graph g with parameters 'beta' and 'gamma' and 
    one infected individual, patient_zero. Uses graph-tool SIRState model to
    speed up computation.
    
    g - graph-tool graph object
    patient_zero - index of patient zero
    beta - infection probability of edge
    gamma - recovery probability
    """
    zero_neighbours = g.get_out_neighbours(patient_zero)
    # Initialise infection states
    state = g.new_vertex_property('double', 0)
    state.a[patient_zero] = RECOVERED  # this is a technicality, not a typo
    # Determine time that patient_zero is infected
    infection_time = np.random.geometric(gamma)  # TODO: is this correct?
    prune(g, patient_zero, 1 + infection_time // 2)  # prune the graph
    # Run a standard SIR model for as long as patient_zero is infected and
    # increment R0 value each time patient_zero directly infects another person 
    R0 = 0
    for _ in range(infection_time):
        """ The following doesn't seem to speed up the function in practice.
        """
        # Terminate if patient zero has no susceptible neighbours
        if (state.a[zero_neighbours] > 0).all():
            print('early termination')
            break

        # Execute all possible primary infections by patient zero

        """ Alternative numpy code to replace the for loop below. May not be
        worth it, as it's less readable and doesn't seem to bring huge speed
        benefits!
        
        newly_infected = np.logical_and(state.a[zero_neighbours]==SUSCEPTIBLE,
                                        coinflips(beta, zero_neighbours.size),
                                        dtype='bool')
        # newly_infected is a boolean mask,
        # zero_neighbours is a list of indices
        state.a[zero_neighbours][newly_infected] = INFECTED
        R0 += newly_infected.sum()
        """
        
        for neighbour in zero_neighbours:
            if state.a[neighbour] == SUSCEPTIBLE and coinflips(beta):
                state.a[neighbour] = INFECTED  # patient_zero infects neighbour
                R0 += 1  # increment counter
        # Execute all other infections using graph-tool model
        model = SIRState(g, beta, gamma, s=state)
        model.iterate_sync()
        state = model.get_state()
    unprune(g)
    return R0

def calculate_R0(g, beta, gamma, trials):
    """Calculate and return an array of length 'trials' with R0 values."""
    vxs = g.get_vertices()
    results = np.zeros(trials)
    for i in range(trials):
        print(f'trial {i}')
        # Pick one person uniformly at random
        person = np.random.choice(vxs, 1, replace=False)
        neighbours = g.get_out_neighbours(person)
        if neighbours.size == 0:  # trivial edge case
            results[i] = 0
        else:
            # Pick one neighbour at random to be patient_zero
            patient_zero = np.random.choice(neighbours)
            # Initialise model with correct state
            results[i] = SIRmodel(g, patient_zero, beta, gamma)
    return results


if __name__ == "__main__":
    n = 10**5  # Population size
    g = price_network(n, directed=False, m=2)
    # RANDOM GEOMETRIC NETWORK
    # points = np.random.random((n, 2)) * 5
    # g, pos = geometric_graph(points, 0.05, [(0, 4), (0, 4)])
    beta = 0.01
    gamma = 0.0476
    trials = 100
    R0_results = calculate_R0(g, beta, gamma, trials)
    
    print(np.mean(R0_results))
    print(np.std(R0_results))
    plt.hist(R0_results, bins=np.linspace(0, 20, round(trials/10)))
    plt.title('mean(R0) = '+str(np.mean(R0_results))+', std(R0) ='+str(round(np.std(R0_results)*100)/100))
    plt.xlabel('R0')
    plt.ylabel('Frequency')
    plt.show(block=False)
