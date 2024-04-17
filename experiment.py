import pygame
import sys
import time

from board import Board
from settings import *

class Experiment:
    def __len__(self):
        return NUMBER_OF_RUNS

    def __init__(self, algorithm, auto, board_size, obstacle_density):
        self.algorithm = algorithm
        self.auto = auto
        self.board_size = board_size
        self.obstacle_density = obstacle_density
        self.results = []

    def setup(self, seed=None):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(f'Pathfinding Experiment - {self.algorithm.__name__}')

        # Initialize Board
        self.board = Board(
            size=self.board_size,
            start=(0, 0),
            end=(self.board_size[0] - 1, self.board_size[1] - 1)
        )
        self.board.set_biomes(5, seed)
        self.algorithm_instance = self.algorithm(self.board)
        self.steps = 0
        self.start_time = time.time()

    def run(self, seed):
        self.setup(seed)
        self.running = True
        while self.running:
            if self.auto:
                search_complete = self.algorithm_instance.step()
                self.steps += 1
                if search_complete:
                    self.finalize()
            else:
                search_complete = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE
                        and not search_complete):
                        search_complete = self.algorithm_instance.step()
                        self.steps += 1
                        if search_complete:
                            self.finalize()
            self.board.draw(self.screen)
            pygame.display.flip()

    def finalize(self):
        self.running = False
        elapsed_time = time.time() - self.start_time
        self.results.append(
            {
                "algorithm": self.algorithm.__name__,
                "board_size": self.board_size,
                "obstacle_density": self.obstacle_density,
                "elapsed_time": elapsed_time,
                "steps": self.steps,
                "path_found": bool(self.board.path)
            }
        )