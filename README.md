# Calculating R0 on a Network

## Modelling an Infectious Disease on a Network
Infectious diseases can be modelled using the Susceptible-Infected-Recovered (SIR) model, where an individual belongs to either of the S, I, or R states. In a network model the population is assumed to consist of nodes which are connected to each other via edges (the number of edges connecting to a node is known as the degree of that node). At each timestep, an infected node can transmit the disease to any of its neighbours with probability beta, and recover from the disease with probability gamma. 

## The Basic Reproductive Number
The basic reproductive number, known as R0, is defined as the expected number of secondary infections caused by one case in a population where everyone is susceptible to infection [1].

Here we present an empirical method and code implementation in Python to calculate R0 using an SIR model on a realistic network. The code was written in Python 3 and requires the installation of graph-tools [2].

## Calculating R0 on a Network
Using the approach presented in [3], we want select one node in the network to seed an infection. Early on in an epidemic, nodes with many connections have a higher probability of becoming infected. Therefore we preferentially choose nodes of high degree using the "friendship paradox", which states that the average degree of neighbouring nodes is higher than ones own degree [4]. We thus start by choosing one node uniformly at random in the network and then choose a connecting node at random to seed the infection. After initialising the epidemic, we count the number of infections caused by the initial case, while ignoring those caused by any of the secondary cases. By initialising and running the model many times, we can then get an estimate of the expected number of secondary infections, or R0.

## Algorithm
0.    Initialise: count = 0
1.    Pick one node uniformly at random
2.    Pick one neighbour to this node uniformly at random and infect (= Patient zero)
4.    While Patient zero is infected do
5.        For each node in the network do
6.            If node is infected do:
7.                Recover with probability beta
8.            If node is susceptible do:
9.                For each neighbour to node do:
10.                   If neighbour is infected do:
11.                       Infect node with probability beta
12.                       If neighbour is patient zero:
13.                           count = count+1




[1] https://en.wikipedia.org/wiki/Basic_reproduction_number
[2] https://graph-tool.skewed.de/
[3] https://royalsocietypublishing.org/doi/pdf/10.1098/rspb.2006.0057 (Supplemental Material)
[4] https://en.wikipedia.org/wiki/Friendship_paradox
