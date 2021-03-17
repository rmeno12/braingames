import random
import math
from typing import List
from .abstract_environment import AbstractEnvironment


class XOREnvironment(AbstractEnvironment):
    def __init__(self) -> None:
        self.internal = [random.randint(0, 1), random.randint(0, 1)]
        self.correct = self.internal[0] ^ self.internal[1]
        self.action = None
        self.score = 0.0
        self.iter = 0
        super().__init__()

    def get_info(self) -> List[float]:
        self.internal = [random.randint(0, 1), random.randint(0, 1)]
        self.correct = self.internal[0] ^ self.internal[1]
        return self.internal

    def act(self, actions: List[float]) -> None:
        self.action = actions[0]
        old = self.score
        self.score += self.calculate_score()
        # print(self.correct, self.action)
        # print("adding", self.score - old)
        self.iter += 1

    def get_score(self) -> float:
        # print("score of", self.score / self.iter)
        return self.score / self.iter

    def calculate_score(self) -> float:
        if self.correct == 0:
            if self.action < -0.01:
                return -math.log(-2 * self.action)
            elif abs(self.action) <= 0.01:
                return 4
            else:
                return -math.log(2 * self.action)
        else:
            if self.action < 0.99:
                return -math.log(-2 * self.action + 2)
            elif abs(self.action - 1) <= 0.01:
                return 4
            else:
                return -math.log(2 * self.action - 2)

    def done(self) -> bool:
        return self.iter >= 10

    def reset(self) -> None:
        self.internal = [random.randint(0, 1), random.randint(0, 1)]
        self.correct = self.internal[0] ^ self.internal[1]
        self.action = None
        self.iter = 0
        self.score = 0.0
