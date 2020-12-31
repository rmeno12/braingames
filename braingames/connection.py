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

    def getInnovationnumber(self) -> int:
        return (1 / 2) * (self.fromNode.id + self.toNode.id) * (
            self.fromNode.idi + self.toNode.id + 1
        ) + self.toNode.id
