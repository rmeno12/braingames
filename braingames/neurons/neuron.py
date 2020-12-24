class Neuron:
    def __init__(self, connectedness: int) -> None:
        super().__init__()
        self.connectedness = connectedness
        self.value = 0