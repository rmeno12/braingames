from .connection import Connection
from .neurons.neuron_types import NeuronTypes
import networkx as nx
import random
import math
from typing import Deque, Dict, List, Tuple
from .neurons.neuron import Neuron


# ideas: start every net with inputs directly connected to output, matter unconnected, then use neat-like algo to connect matter
class Brain:
    colors = ["blue", "orange", "orange", "orange", "orange", "green"]

    def __init__(self, isOffspring: bool = False) -> None:
        super().__init__()
        self.inputs: List[Neuron] = []
        self.matter: List[Neuron] = []
        self.outputs: List[Neuron] = []
        self.nextNodeId = 0
        self.connections: List[Connection] = []
        self.isOffspring = isOffspring

    def __str__(self) -> str:
        return (
            f"[inputs: {self.inputs}, matter: {self.matter}, outputs: {self.outputs}]"
        )

    def add_input_neurons(self, number: int, connectedness: int) -> None:
        for _ in range(number):
            self.inputs.append(
                Neuron(self.nextNodeId, NeuronTypes.INPUTNEURON, connectedness)
            )
            self.nextNodeId += 1

    def add_matter_neurons(self, number: int, connectedness: int) -> None:
        for _ in range(number):
            self.matter.append(
                Neuron(self.nextNodeId, NeuronTypes.MATTERNEURON, connectedness)
            )
            self.nextNodeId += 1

    def add_output_neurons(self, number: int, connectedness: int) -> None:
        for _ in range(number):
            self.outputs.append(
                Neuron(self.nextNodeId, NeuronTypes.OUTPUTNEURON, connectedness)
            )
            self.nextNodeId += 1

    def startup(self):
        if self.isOffspring:
            return

        for inp in self.randomize(self.inputs):
            for out in self.randomize(self.outputs):
                if self.degree(inp) >= inp.connectedness:
                    break
                weight = random.random() * 2 - 1
                self.connections.append(Connection(inp, out, weight))

    def evaluate(self, input: List[int]):
        assert len(input) == len(
            self.inputs
        ), "Input should be same size as input nodes length"

        self.generate_connections()

        for neu in self.inputs + self.matter + self.outputs:
            neu.input = 0

        # set inputs
        for i, inp in enumerate(input):
            self.inputs[i].input = inp

        num_visits = 5
        visits: Dict[Neuron, int] = {
            neu: 0 for neu in self.inputs + self.matter + self.outputs
        }

        # bfs to propagate inputs
        q: Deque[Neuron] = Deque()
        for inp in self.inputs:
            visits[inp] += 1
            q.append(inp)

        while len(q) > 0:
            n = q.pop()
            n.evaluate()
            for conn in n.outputConnections:
                if visits[conn.toNode] < num_visits:
                    q.append(conn.toNode)
                    visits[conn.toNode] += 1

        return [neu.output for neu in self.outputs]

    def generate_connections(self) -> None:
        for neu in self.inputs + self.matter:
            neu.outputConnections = []

        for conn in self.connections:
            conn.fromNode.outputConnections.append(conn)

    def crossover(self, other):
        child = Brain()
        if other.fitness < self.fitness:
            child = self.cross(other)
        else:
            child = other.cross(self)

        child.mutate()
        return child

    def cross(self, other):
        pass

    def randomize(self, lst: List) -> List:
        return random.sample(lst, len(lst))

    def degree(self, neuron: Neuron) -> int:
        # TODO: consider whether to use in/out degree or both
        # rn only using out degree
        return len(neuron.outputConnections)

    def draw(self) -> None:
        g = nx.DiGraph()
        for node in self.inputs + self.matter + self.outputs:
            self.add_node_to_graph(node, g)
        for conn in self.connections:
            g.add_weighted_edges_from([(conn.fromNode, conn.toNode, conn.weight)])
        newlabels = {neu: float(f"{neu.output:.2f}") for neu in g.nodes}
        # g = nx.relabel_nodes(g, newlabels)
        pos = nx.multipartite_layout(g)
        colors = ["blue"] + ["orange"] * math.ceil(len(self.matter) / 3) + ["green"]
        ncolor = [colors[data["subset"]] for v, data in g.nodes(data=True)]
        nodes = nx.draw_networkx_nodes(g, pos, node_color=ncolor)
        edges = nx.draw_networkx_edges(g, pos)
        # nx.draw_networkx_labels(g, pos)

    def add_node_to_graph(self, node, graph):
        if node.neuronType == NeuronTypes.INPUTNEURON:
            graph.add_node(node, subset=0)
        elif node.neuronType == NeuronTypes.MATTERNEURON:
            graph.add_node(
                node,
                subset=random.randint(1, math.ceil(len(self.matter) / 3)),
            )
        else:
            graph.add_node(node, subset=math.ceil(len(self.matter) / 3) + 1)
