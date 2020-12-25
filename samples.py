from braingames.neurons.output_neuron import OutputNeuron
from braingames.neurons.matter_neuron import MatterNeuron
from braingames.neurons.input_neuron import InputNeuron
from braingames.brain import Brain
from matplotlib import pyplot as plt

# Create a brain with 2 inputs, 9 matter neurons, and 2 outputs
b = Brain()
b.add_input_neurons([InputNeuron(2) for _ in range(2)])
b.add_matter_neurons([MatterNeuron(5) for _ in range(9)])
b.add_output_neurons([OutputNeuron(3) for _ in range(2)])

# Initialize the brain to the random connections and weights, then evaluate it with some inputs
b.startup()
print(b.evaluate([1, 2]))

# Draw the brain using matplotlib
b.draw()
plt.show()