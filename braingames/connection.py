import random


class Connection:
    def __init__(self, prec, to, weight: float) -> None:
        super().__init__()
        self.fromNode = prec
        self.toNode = to
        self.weight = weight
        self.enabled = True

    def copy(self):
        conn = Connection(self.fromNode, self.toNode, self.weight)
        conn.enabled = self.enabled
        return conn

    def get_innovation_number(self) -> int:
        return (1 / 2) * (self.fromNode.id + self.toNode.id) * (
            self.fromNode.id + self.toNode.id + 1
        ) + self.toNode.id

    def mutate_weight(self, chance: float):
        # chance% chance of randomly reassigning weight, otherwise uniformly perturb
        if random.random() < chance:
            self.weight = random.random() * 2 - 1
        else:
            self.weight += random.random() / 20
