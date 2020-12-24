import networkx as nx
import random
from typing import Deque, Dict, List, Tuple
from .neurons.neuron import Neuron
from .neurons.matter_neuron import MatterNeuron
from .neurons.output_neuron import OutputNeuron
from .neurons.input_neuron import InputNeuron


class Brain:
    colors = ["blue", "orange", "orange", "orange", "orange", "green"]

    def __init__(self) -> None:
        super().__init__()
        self.inputs: List[InputNeuron] = []
        self.matter: List[MatterNeuron] = []
        self.outputs: List[OutputNeuron] = []
        self.connections = nx.DiGraph()

    def __str__(self) -> str:
        return (
            f"[inputs: {self.inputs}, matter: {self.matter}, outputs: {self.outputs}]"
        )

    def add_input_neurons(self, input_neurons: List[InputNeuron]) -> None:
        self.inputs.extend(input_neurons)
        self.connections.add_nodes_from(input_neurons, layer=0)

    def add_matter_neurons(self, matter_neurons: List[MatterNeuron]) -> None:
        self.matter.extend(matter_neurons)
        for mat in matter_neurons:
            self.connections.add_node(mat, layer=random.randint(1, 4))

    def add_output_neurons(self, output_neurons: List[OutputNeuron]) -> None:
        self.outputs.extend(output_neurons)
        self.connections.add_nodes_from(output_neurons, layer=5)

    # TODO: make sure input and output are connected
    def startup(self):
        for inp in self.randomize(self.inputs):
            for mat in self.randomize(self.matter):
                if self.degree(inp) >= inp.connectedness:
                    break
                self.connections.add_edge(inp, mat, weight=random.random() - 0.5)

        for mat in self.randomize(self.matter):
            for neu in self.randomize(self.matter + self.outputs):
                if neu == mat:
                    break
                if (
                    self.degree(mat) >= mat.connectedness
                    or self.degree(neu) >= neu.connectedness
                ):
                    break
                self.connections.add_edge(mat, neu, weight=random.random() - 0.5)

    def evaluate(self, input: List[int]):
        assert len(input) == len(
            self.inputs
        ), "Input should be same size as input nodes length"

        num_visits = 5
        visits: Dict[Neuron, int] = {
            neu: 0 for neu in self.inputs + self.matter + self.outputs
        }

        # set inputs
        for i, inp in enumerate(input):
            self.inputs[i].value = inp

        # bfs to propagate inputs
        q: Deque[Tuple[Neuron, Neuron]] = Deque()
        for inp in self.inputs:
            visits[inp] += 1
            for neu in self.connections.neighbors(inp):
                q.append((inp, neu))

        while len(q) > 0:
            x, y = q.pop()
            edge_weight = self.connections[x][y]["weight"]
            y.value += edge_weight * x.value
            visits[y] += 1
            for neu in self.connections.neighbors(y):
                if visits[neu] < num_visits:
                    q.append((y, neu))

        return [neu.value for neu in self.outputs]

    def randomize(self, lst: List) -> List:
        return random.sample(lst, len(lst))

    def degree(self, neuron: Neuron) -> int:
        # TODO: consider whether to use in/out degree or both
        # rn only using out degree
        return len(self.connections.succ[neuron])

    def draw(self) -> None:
        g = self.connections.copy()
        newlabels = {neu: float(f"{neu.value:.2f}") for neu in g.nodes}
        g = nx.relabel_nodes(g, newlabels)
        pos = nx.multipartite_layout(g, subset_key="layer")
        ncolor = [Brain.colors[data["layer"]] for v, data in g.nodes(data=True)]
        nodes = nx.draw_networkx_nodes(g, pos, node_color=ncolor)
        edges = nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos)
