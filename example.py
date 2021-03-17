from braingames.population import Population
from braingames.environments.xor_environment import XOREnvironment

pop = Population(XOREnvironment(), 30, 2, 3, 1, 4, 1, 3)

for i in range(500):
    print("\nGeneration", i)
    pop.step()

best = pop.get_best_individual()
print(best.evaluate([0, 0]))
print(best.evaluate([0, 1]))
print(best.evaluate([1, 1]))
print(best.evaluate([1, 0]))