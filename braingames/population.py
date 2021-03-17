import random
from .environments.abstract_environment import AbstractEnvironment
from typing import List
from .brain import Brain


class Population:
    def __init__(
        self,
        environment: AbstractEnvironment,
        size: int,
        num_input: int,
        input_connectedness: int,
        num_matter: int,
        matter_connectedness: int,
        num_output: int,
        output_connectedness: int,
    ) -> None:
        super().__init__()
        self.environment = environment
        self.num_input = num_input
        self.input_connectedness = input_connectedness
        self.num_matter = num_matter
        self.matter_connectedness = matter_connectedness
        self.num_output = num_output
        self.output_connectedness = output_connectedness

        self.mating_pool: List[int] = []

        self.population: List[Brain] = []
        for _ in range(size):
            b = Brain()
            b.add_input_neurons(num_input, input_connectedness)
            b.add_matter_neurons(num_matter, matter_connectedness)
            b.add_output_neurons(num_output, output_connectedness)
            b.startup()
            self.population.append(b)
        self.best_brain: Brain = self.population[0]

    def step(self):
        self.run_simulation()
        self.fill_mating_pool()
        self.natural_selection()

    def run_simulation(self) -> None:
        maxFitness = 0
        # Run simulations and calculate fitnesses
        for brain in self.population:
            self.environment.reset()
            while True:
                self.environment.act(brain.evaluate(self.environment.get_info()))

                if self.environment.done():
                    break
            brain.fitness = self.environment.get_score()
            if brain.fitness > maxFitness:
                maxFitness = brain.fitness
                self.best_brain = brain

        # Normalize fitnesses
        print("best fitness", maxFitness)
        for brain in self.population:
            brain.fitness /= maxFitness

    def fill_mating_pool(self) -> None:
        self.mating_pool = []
        # store indices of brains in proportion to their fitness
        for i, brain in enumerate(self.population):
            for _ in range(int(100 * brain.fitness)):
                self.mating_pool.append(i)

    def natural_selection(self) -> None:
        nextGen: List[Brain] = []

        for i in range(len(self.population)):
            b1 = self.population[random.choice(self.mating_pool)]
            b2 = self.population[random.choice(self.mating_pool)]
            nextGen.append(b1.crossover(b2))

        self.population = nextGen

    def get_best_individual(self) -> Brain:
        return self.best_brain
