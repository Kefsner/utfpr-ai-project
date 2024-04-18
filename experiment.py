import pygame
import sys
import time

from board import Board
from settings import *

class Experiment:
    def __len__(self):
        return NUMBER_OF_RUNS

    def __init__(self, algorithm, board_size):
        self.algorithm = algorithm
        self.board_size = board_size
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
        self.board.set_biomes(30, seed)
        self.board.set_cell_state(0, 0, self.board.START)
        self.board.set_cell_state(self.board_size[0] - 1, self.board_size[1] - 1, self.board.END)
        self.algorithm_instance = self.algorithm(self.board)
        self.steps = 0
        self.start_time = time.time()

    def run(self, seed):
        self.setup(seed)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            search_complete = self.algorithm_instance.step()
            self.steps += 1
            if search_complete:
                self.finalize()
            self.board.draw(self.screen)
            pygame.display.flip()
            if not self.running:
                pygame.time.wait(2000)

    def finalize(self):
        self.running = False
        elapsed_time = time.time() - self.start_time
        self.results.append(
            {
                "algorithm": self.algorithm.__name__,
                "board_size": self.board_size,
                "elapsed_time": elapsed_time,
                "steps": self.steps,
                "path_found": bool(self.board.path)
            }
        )