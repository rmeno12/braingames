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
        self.dead = False
        self.fitness: float = None

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

    def evaluate(self, input: List[float]):
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
            n = q.popleft()
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
        child = Brain(True)
        if other.fitness < self.fitness:
            child = self.cross(other)
        else:
            child: Brain = other.cross(self)

        child.mutate()
        return child

    def cross(self, other):
        child = Brain(True)
        child.nextNodeId = self.nextNodeId

        # randomly take neuron values from either parent (50/50 either way)
        for i in range(len(self.inputs)):
            # TODO: consider removing unused nodes? idk
            neu = self.inputs[i].copy()
            if random.random() > 0.5:
                neu.bias = other.inputs[i].bias
            child.inputs.append(neu)

        for i in range(len(self.matter)):
            neu = self.matter[i].copy()
            if random.random() > 0.5:
                neu.bias = other.matter[i].bias
            child.matter.append(neu)

        for i in range(len(self.outputs)):
            neu = self.outputs[i].copy()
            if random.random() > 0.5:
                neu.bias = other.outputs[i].bias
            child.outputs.append(neu)

        # copy connections from this brain, but if other brain has same connection then randomly take weights from other brain
        for i in range(len(self.connections)):
            idx = other.find_matching_connection_index(
                self.connections[i].get_innovation_number
            )

            if idx == -1:
                # other brain doesn't have same connection, so just use this brain's version
                conn = self.connections[i].copy()
                conn.fromNode = self.get_node_by_number(conn.fromNode.id)
                conn.toNode = self.get_node_by_number(conn.toNode.id)
                child.connections.append(conn)
            else:
                # other brain has same connection, pick one 50/50
                conn = (
                    self.connections[i].copy()
                    if random.random() > 0.5
                    else other.connections[idx].copy()
                )
                conn.fromNode = self.get_node_by_number(conn.fromNode.id)
                conn.toNode = self.get_node_by_number(conn.toNode.id)
                child.connections.append(conn)

        return child

    def mutate(self):
        # TODO: change some of these probabilities to hyperparams
        # TODO: explore doing probability inside loops

        # 80% chance to mutate weights of all connections
        if random.random() < 0.8:
            for conn in self.connections:
                conn.mutate_weight(0.05)

        # 80% chance to mutate biases of all nodes
        if random.random() < 0.8:
            for neu in self.inputs + self.matter + self.outputs:
                neu.mutate_bias(0.05)

        # 5% chance to add a new connection (if possible)
        if random.random() < 0.05:
            self.add_new_connection()

        # 5% chance to randomly remove a connection
        if random.random() < 0.05 and len(self.connections) > 1:
            self.connections.pop(random.randint(0, len(self.connections) - 1))

    def add_new_connection(self):
        n1: Neuron = None
        n2: Neuron = None

        n1 = random.choice(self.inputs + self.matter + self.outputs)
        while self.degree(n1) >= n1.connectedness:
            n1 = random.choice(self.inputs + self.matter + self.outputs)

        n2 = random.choice(self.inputs + self.matter + self.outputs)
        while self.degree(n2) >= n2.connectedness or n1 == n2 or n1.connected_to(n2):
            n2 = random.choice(self.inputs + self.matter + self.outputs)

        self.connections.append(Connection(n1, n2, random.random() * 2 - 1))

    def find_matching_connection_index(self, index: int) -> int:
        for i in range(len(self.connections)):
            if self.connections[i].get_innovation_number() == index:
                return i

        return -1

    def get_node_by_number(self, number: int) -> Neuron:
        for neu in self.inputs + self.matter + self.outputs:
            if neu.id == number:
                return neu

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
            pass
            g.add_weighted_edges_from([(conn.fromNode, conn.toNode, conn.weight)])
        newlabels = {neu: float(f"{neu.output:.2f}") for neu in g.nodes}
        g = nx.relabel_nodes(g, newlabels)
        pos = nx.multipartite_layout(g)
        colors = ["blue"] + ["orange"] * math.ceil(len(self.matter) / 3) + ["green"]
        ncolor = [colors[data["subset"]] for v, data in g.nodes(data=True)]
        nodes = nx.draw_networkx_nodes(g, pos, node_color=ncolor)
        edges = nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos)

    def add_node_to_graph(self, node, graph: nx.DiGraph):
        if node.neuronType == NeuronTypes.INPUTNEURON:
            graph.add_node(node, subset=0)
        elif node.neuronType == NeuronTypes.MATTERNEURON:
            graph.add_node(
                node,
                subset=random.randint(1, math.ceil(len(self.matter) / 3)),
            )
        else:
            graph.add_node(node, subset=math.ceil(len(self.matter) / 3) + 1)
