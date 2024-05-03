from experiment import Experiment

from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.Dijkstra import Dijkstra
from algorithms.GBFS import GBFS
from algorithms.AStar import AStar

from report import Report

import pandas as pd

import os
import glob

from datetime import datetime

from settings import *

board_size = (10, 10)
successful_seeds = []
i = 0
print("Finding seeds...")
while len(successful_seeds) < NUMBER_OF_RUNS:
    experiment = Experiment(GBFS, board_size)
    if experiment.setup(seed=i, test=True):
        successful_seeds.append(i)
    i += 1

results = []
for algorithm in [BFS, DFS, Dijkstra, GBFS, AStar]:
    i = 0
    for seed in successful_seeds:
        i += 1
        experiment = Experiment(algorithm, board_size)
        if experiment.setup(seed=seed):
            print(f"Running experiment {i} of {NUMBER_OF_RUNS} for {algorithm.__name__}")
            experiment.run()
            results.append(experiment.results)

results = [result for sublist in results for result in sublist]
path = f"results/{board_size[0]}x{board_size[1]}"
os.makedirs(f"{path}", exist_ok=True)
pd.DataFrame(results).to_csv(f"{path}/{datetime.now().strftime(DATE_FORMAT)}.csv", index=False)

latest_file = max(glob.glob(f"{path}/*.csv"), key=os.path.getctime)
if latest_file:
    df = pd.read_csv(latest_file)
    report = Report(df, board_size)
    report.save(path)