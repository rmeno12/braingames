from braingames.neurons.output_neuron import OutputNeuron
from braingames.neurons.matter_neuron import MatterNeuron
from braingames.neurons.input_neuron import InputNeuron
from braingames.brain import Brain
from matplotlib import pyplot as plt
import networkx as nx
import copy


b = Brain()
b.add_input_neurons([InputNeuron(2) for _ in range(2)])
b.add_matter_neurons([MatterNeuron(5) for _ in range(9)])
b.add_output_neurons([OutputNeuron(3) for _ in range(2)])

b.startup()
print(b.evaluate([1, 2]))

b.draw()
for out in b.outputs:
    print(b.connections.pred[out])
    print(b.connections.succ[out])
plt.show()
# ideas: start every net with inputs directly connected to output, matter unconnected, then use neat-like algo to connect matter