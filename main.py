from experiment import Experiment

from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.Dijkstra import Dijkstra
from algorithms.GBFS import GreedyBFS
from algorithms.AStar import AStar

from report import Report

import pandas as pd
import os
import glob

from datetime import datetime

results = []

for algorithm in [BFS, DFS, Dijkstra, GreedyBFS, AStar]:
    experiment = Experiment(
        algorithm=algorithm,
        auto=True,
        board_size=(50, 50),
        obstacle_density=0.25,
    )
    for i in range(len(experiment)):
        print(f"Running experiment {i + 1}/{len(experiment)} with {algorithm.__name__}")
        experiment.run(seed=i)
        raise SystemExit

    results.append(experiment.results)

results = [result for sublist in results for result in sublist]

try:
    os.mkdir("results")
except FileExistsError:
    pass
finally:
    pd.DataFrame(results).to_csv(f"results/results_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", index=False)

# Get the latest file
list_of_files = glob.glob('results/*.csv')
if not list_of_files:
    print("No files found in the results directory")
    raise SystemExit

latest_file = max(list_of_files, key=os.path.getctime)

# Load the data
df = pd.read_csv(latest_file)

df = df.loc[df['path_found']]

report = Report(df)

report.save()