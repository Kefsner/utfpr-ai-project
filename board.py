import pygame
import random
from settings import *

class Board:
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    END = 3
    VISITING = 4    # Cells that are in the queue to be visited
    VISITED = 5     # Cells that have been visited
    PATH = 6        # Cells that are part of the path

    def __init__(self, size, start, end):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size[0])] for _ in range(size[1])]
        self.set_cell_state(*start, self.START)
        self.set_cell_state(*end, self.END)
        self.path = None
        self.start = start
        self.end = end

    def set_cell_state(self, x, y, state):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.grid[y][x] = state
        else:
            raise ValueError(f"Invalid cell position: ({x}, {y})")

    def get_cell_state(self, x, y):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.grid[y][x]
        return None

    def set_random_obstacles(self, density, seed=None):
        if seed is not None:
            random.seed(seed)
        count = 0
        n = int(self.size[0] * self.size[1] * density)
        while count < n:
            x, y = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
            if self.get_cell_state(x, y) == self.EMPTY:
                self.set_cell_state(x, y, self.OBSTACLE)
                count += 1

    def is_valid_position(self, x, y):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.get_cell_state(x, y) != self.OBSTACLE
        return False

    def draw(self, screen):
        cell_x = WINDOW_SIZE // self.size[0]
        cell_y = WINDOW_SIZE // self.size[1]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                rect = pygame.Rect(x * cell_x, y * cell_y, cell_x, cell_y)
                state = self.get_cell_state(x, y)
                color = BLACK  # Default color

                # Define colors based on state
                if state == self.OBSTACLE:
                    color = ORANGE
                elif state == self.START:
                    color = GREEN
                elif state == self.END:
                    color = RED
                elif state == self.VISITING:
                    color = LIGHT_BLUE
                elif state == self.VISITED:
                    color = BLUE
                elif state == self.PATH:
                    color = GREEN

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def mark_path(self, path):
        for x, y in path:
            self.set_cell_state(x, y, self.PATH)

    def render_message(self, message, screen):
        container_width = 130
        container_height = 50
        container_x = (WINDOW_SIZE - container_width) // 2
        container_y = (WINDOW_SIZE - container_height) // 2

        # Container color
        container_color = DARK_GRAY

        # Text color
        text_color = WHITE

        # Draw the container rectangle
        pygame.draw.rect(screen, container_color, [container_x, container_y, container_width, container_height])

        # Render the message text
        text = pygame.font.SysFont(None, 24).render(message, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

        screen.blit(text, text_rect)