from experiment import Experiment

from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.Dijkstra import Dijkstra
from algorithms.GBFS import GreedyBFS
from algorithms.AStar import AStar

experiment = Experiment(
    algorithm=DFS,
    auto=True,
    board_size=(20, 20),
    obstacle_density=0.25,
)

results = []

for i in range(5):
    print(f"Running experiment {i + 1}")
    experiment.run(seed=i)
    results.append(experiment.results)
    print(f"Experiment {i + 1} completed")

print(results)