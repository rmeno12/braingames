from .neuron_types import NeuronTypes
from ..connection import Connection
import random
from typing import List


class Neuron:
    def __init__(self, id: int, type: NeuronTypes, connectedness: int) -> None:
        super().__init__()
        # TODO: add activation
        self.connectedness = connectedness
        self.bias = random.random() * 2 - 1
        self.neuronType = type
        self.id = id

        self.input = 0
        self.output = 0
        self.outputConnections: List[Connection] = []

    def evaluate(self) -> None:
        if self.neuronType != NeuronTypes.INPUTNEURON:
            self.output = self.activation(self.input + self.bias)
        else:
            self.output = self.input

        for connection in self.outputConnections:
            if connection.enabled:
                connection.toNode.input = connection.weight * self.output

    def activation(self, inp: float) -> float:
        # TODO: add other activation functions
        return inp

    def copy(self):
        neu = Neuron(self.id, self.neuronType, self.connectedness)
        neu.bias = self.bias
        return neu
