from .neuron import Neuron


class MatterNeuron(Neuron):
    def __init__(self, connectedness: int) -> None:
        super().__init__(connectedness)