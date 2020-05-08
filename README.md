# Calculating R0 on a Network

## Modelling an Infectious Disease on a Network
Infectious diseases can be modelled using a Susceptible-Infected-Recovered (SIR) model, where each individual in the population belongs to either of the S, I, or R states. In a network model, the population is assumed to consist of nodes which are connected to each other via edges (the number of edges connecting to a node is known as the degree of that node). At each timestep, an infected node transmits the disease to each of its susceptible neighbours with probability `beta`, and recover from the disease with probability `gamma`. 

## The Basic Reproductive Number
The basic reproductive number, known as `R0`, is a dimensionless number defined as the expected number of secondary infections directly caused by one infected individual (_patient 0_) in a population where everyone else is initially susceptible to infection [1]. When considering a network model, we assume that the node representing patient 0 is distributed proportionally to the degrees of the nodes (as nodes with many connections have a higher probability of being infected). For this reason, the expectation is taken w.r.t. this distribution as well as the inherent probability parameters `beta` and `gamma`.

Note that for any fixed node, the total number of secondary infections that are caused _directly_ by the node is bounded from above by its degree. Hence 'R0' is less than or equal to the expected degree when we sample from the population with the above non-uniform distribution.

Here we present an empirical method and code implementation in Python to calculate `R0` using an SIR model on any realistic network. The code was written in Python 3 and requires the installation of `graph-tools` [2].

## Calculating R0 on a Network
Following the approach presented in [3], we first select one node in the network to seed an infection. In order to sample from the population according to a distribution that gives preference to nodes of high degree, we make use of the 'friendship paradox': the average degree of neighbouring nodes is higher than the degree of the node itself [4]. We begin by choosing one node uniformly at random from the population and then pick one of its neighbouring nodes in the network (uniformly at random) to be patient 0. After seeding the infection with patient 0, we count the number of infections directly caused by the initial case, while ignoring those caused by any of the secondary cases.

By initialising and running the above procedure multiple times, we obtain an accurate estimate of the expected number of secondary infections, or `R0`.

## Algorithm
```
  PROGRAM Calculate R0:
  count = 0
  Pick one node uniformly at random
  Pick one neighbour to this node uniformly at random and infect (= Patient zero)
  While Patient zero is infected do:
      For each node in the network do:
          If node is infected do:
              Recover node with probability beta
          If node is susceptible do:
                For each neighbour to node do:
                    If neighbour is infected do:
                        Infect node with probability beta
                            If neighbour is patient zero:
                                count = count+1
  R0 = count
  END
```

## Authors
Jakob Jonnerby
jakob.jonnerby@physics.ox.ac.uk

Edwin Lock
edwin.lock@merton.ox.ac.uk

## Requirements
graph-tools

## References


[1] https://en.wikipedia.org/wiki/Basic_reproduction_number

[2] https://graph-tool.skewed.de/

[3] https://royalsocietypublishing.org/doi/pdf/10.1098/rspb.2006.0057 (Supplemental Material)

[4] https://en.wikipedia.org/wiki/Friendship_paradox
