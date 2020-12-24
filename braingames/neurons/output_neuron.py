from .neuron import Neuron


class OutputNeuron(Neuron):
    def __init__(self, connectedness: int) -> None:
        super().__init__(connectedness)