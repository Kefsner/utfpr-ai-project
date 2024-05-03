# Evaluating Pathfinding Algorithms in a Weighted Square Grid
## Overview

This repository contains the source code and supplementary materials for the work titled "Evaluating Pathfinding Algorithms in a Weighted Square Grid." The study investigates the performance of various pathfinding algorithms—Breadth-First Search (BFS), Depth-First Search (DFS), Dijkstra's Algorithm, Greedy Best-First Search (GBFS), and A* Algorithm—across different weighted grid sizes and scenarios. This project is part of the coursework for the Artificial Intelligence class at the Programa de Pós-Graduação em Informática (PPGI) da UTFPR de Cornélio Procópio.

# Pathfinding Algorithm Evaluation

## Overview

This repository contains the source code and supplementary materials for the research paper titled "Evaluating Pathfinding Algorithms in a Weighted Square Grid." Conducted as part of the coursework for the Artificial Intelligence class at the Programa de Pós-Graduação em Informática da UTFPR de Cornélio Procópio (PPGI-CP), this study assesses various pathfinding algorithms across different grid sizes and scenarios, focusing on execution time, number of steps, and path cost efficiency.

## Running Experiments

To reproduce the experiment, set up a Python environment and install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

Next, run the `main.py` script:

```bash
python main.py
```

## Analyzing Results

In order to reproduce the plots from the paper, run the results/analysis.ipybn Jupyter notebook.

In order to reproduce the graph images, run the results/graphs/graphs.ipynb Jupyter notebook. Note the use of the graphviz library to generate the images. It needs to be installed in the system, besides the python library. For Ubuntu, it can be installed using the following command:

```bash
sudo apt-get install graphviz
```

For Windows, it can be downloaded from the official website: https://graphviz.org/download/

## License

This project is licensed under the MIT License.