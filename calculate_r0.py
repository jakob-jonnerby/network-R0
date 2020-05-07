import numpy as np
from graph_tool.generation import price_network, geometric_graph
from graph_tool import infect_vertex_property
import matplotlib.pyplot as plt

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

print('Imported all libraries')


def SIRmodel(g, state, SIRS_params):
    beta = SIRS_params['beta']
    gamma = SIRS_params['gamma']
    vxs = list(g.vertices())
    patient_zero = np.nonzero(state.a)[0][0]
    infection_log = 0
    while state[patient_zero] == INFECTED:
        np.random.shuffle(vxs)
        for v in vxs:
            if state[v] == INFECTED:
                if np.random.random() < gamma:
                    state[v] = RECOVERED
                    if v == patient_zero:
                        break
            elif state[v] == SUSCEPTIBLE:
                ns = list(v.out_neighbors())
                for w in ns:
                    if state[w] == INFECTED:
                        if np.random.random() < beta:
                            state[v] = INFECTED
                            if w == patient_zero:
                                infection_log += 1
                            break

    return infection_log


def calculate_R0(g, SIRS_params):
    vxs = g.get_vertices()

    # Pick one person uniformly at random
    k_selection = np.random.choice(vxs, 1, replace=False)

    if len(g.get_out_neighbours(k_selection)) == 0:
        R0 = 0
    else:
        # Pick one neighbour at random
        k_neighbour = np.random.choice(g.get_out_neighbours(k_selection))

        # Seed infection to patient zero
        state = g.new_vertex_property('int32_t', False)
        state.a[k_neighbour] = 1

        # Remove all  nodes that are not neighbours to patient zero
        new_vxs = state.copy(value_type='bool')
        infect_vertex_property(g, new_vxs, vals=[True])
        g.set_vertex_filter(new_vxs)

        # Initialise model with correct state
        R0 = SIRmodel(g, state, SIRS_params)
    return R0


if __name__ == "__main__":
    n = 10**5  # Population size
    SIRS_params = {'beta': 0.01,
                   'gamma': 0.0476,
                   }
    trials = 100
    R0_trials = np.zeros(trials)
    for i in range(trials):
        print(i)
        # Choose network model to use
        # SCALE-FREE NETWORK
        g = price_network(n, directed=False, m=2)

        # RANDOM GEOMETRIC NETWORK
        # points = np.random.random((n, 2)) * 5
        # g, pos = geometric_graph(points, 0.05, [(0, 4), (0, 4)])
        
        R0_trials[i] = calculate_R0(g, SIRS_params)

    print(np.mean(R0_trials))
    print(np.std(R0_trials))
    plt.hist(R0_trials, bins=np.linspace(0, 20, round(trials/10)))
    plt.title('mean(R0) = '+str(np.mean(R0_trials))+', std(R0) ='+str(round(np.std(R0_trials)*100)/100))
    plt.xlabel('R0')
    plt.ylabel('Frequency')
    plt.show()
