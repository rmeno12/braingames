# braingames
This is a project in which I attempt to replicate the behavior of a cluster of neurons using ideas from biology and standard deep neural networks.
What differentiates this from a traditional neural network is the posibility of loops and reverse connections between nodes.
Generally, this network topology is not restricted to the sequential layer-based architecture of many modern networks.

In addition, the output of the network is not read immediately after a value is written to it.
Instead, a modified breadth-first search (BFS) is used which allows up to a certain number (determined by a hyperparameter) of repeated visits to a node. This lets paths of different lengths be expressed in the final output of the graph. 
After the completion of this BFS, the value of the output node(s) is output.

Such a network is referred to as a "brain". 
This architecture was inspired by a high-level observation of how natural brains work: sensory neurons receive information and transmit that to a target region of the brain (the brain matter) which then sends an output signal producing a physical response. 
Similarly, the brain architecture has input neurons connected to a cluster of matter neurons which are interconnected and connected to output neurons. 

In the future, I am attempting to use this architecture to allow learning of behavior using a NEAT-style genetic algorithm in which the connections and the weights of connections are part of a genotype. 
The genotypes are evolved over time to optimize performance of a task, just as in other forms of learning. 
The difference from NEAT is the application to the brain architecture and the lack of creation of new neurons. 
The motivation for this second change is that natural brains are very limited in creating new neurons, but are still able to learn to perform new tasks.
Therefore, it should be possible to learn tasks given only a certain number of neurons by modifying the connections between those neurons.

Currently, no activation function is used on neurons after their values have been updated, but this is a topic to be explored in the future. These functions could be associated with connections rather than neurons themselves and learned separately so that different periphery neurons are activated dependent on the value of the current neuron.