from braingames.brain import Brain
from matplotlib import pyplot as plt

# Create a brain with 2 inputs, 9 matter neurons, and 2 outputs
b = Brain()
b.add_input_neurons(2, 2)
b.add_matter_neurons(9, 4)
b.add_output_neurons(2, 3)

# Initialize the brain to the random connections and weights, then evaluate it with some inputs
b.startup()
print(b.evaluate([1, 2]))

# Draw the brain using matplotlib
b.draw()
plt.show()