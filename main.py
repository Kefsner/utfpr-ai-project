import pygame
import sys

from board import Board
from settings import *

from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.Dijkstra import Dijkstra
from algorithms.GBFS import GreedyBFS
from algorithms.AStar import AStar
from algorithms.JPS import JPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Pathfinding Visualization')

# Initialize Board
board = Board(BOARD_SIZE)
board.set_random_obstacles(10)
board.set_start(0, 0)
board.set_end(BOARD_SIZE - 1, BOARD_SIZE - 1)

# Algorithm
algorithm = BFS(board)
algorithm = DFS(board)
algorithm = Dijkstra(board)
algorithm = GreedyBFS(board)
algorithm = AStar(board)
algorithm = JPS(board)

# Main loop
running = True
search_complete = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if (event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and not search_complete):
            search_complete = algorithm.step()
            
    # Draw the board
    board.draw(screen) 
    
    if search_complete:
        message = "Path found!" if board.path else "No path found!"
        board.render_message(message, screen)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    else:
        pygame.display.flip()
        pygame.time.delay(100)

# Quit Pygame
pygame.quit()
sys.exit()
