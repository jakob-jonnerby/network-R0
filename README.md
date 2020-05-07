# Calculating R0 on a Network

## Modelling an Infectious Disease on a Network
Infectious diseases can be modelled using the Susceptible-Infected-Recovered (SIR) model, where an individual belongs to either of the S, I, or R states. In a network model the population is assumed to consist of nodes which are connected to each other via edges. At each timestep, a node 

<a href="https://www.codecogs.com/eqnedit.php?latex=\beta,&space;\gamma" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\beta,&space;\gamma" title="\beta, \gamma" /></a>

## The Basic Reproductive Number
The basic reproductive number, known as R0, is defined as the expected number of secondary infections caused by one case in a population where everyone is susceptible to infection [1].

Here we present an empirical method and code implementation to calculate R0 using an SIR model arbitrary network



[1] https://en.wikipedia.org/wiki/Basic_reproduction_number
