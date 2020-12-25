# braingames
This is a project in which I attempt to replicate the behavior of a cluster of neurons.
What differentiates this from a traditional neural network is the posibility of loops and reverse connections between nodes.
Generally, this network topology is not restricted to the sequential layer-based architecture of many modern networks.

In addition, the output of the network is not read immediately after a value is written to it.
Instead, a modified breadth-first search is used which allows up to a certain number (determined by a hyperparameter) of repeated visits to a node. This lets paths of different lengths be expressed in the final output of the graph.