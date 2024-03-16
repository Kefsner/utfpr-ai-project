import pygame
import random
from settings import *

class Board:
    EMPTY = 0
    OBSTACLE = 1
    START = 2       # Starting cell
    END = 3         # Ending cell
    VISITING = 4    # Cells that are in the queue to be visited
    VISITED = 5     # Cells that have been visited
    PATH = 6        # Cells that are part of the path

    def __init__(self, size):
        self.size = size
        self.grid = [[(self.EMPTY, None) for _ in range(size)] for _ in range(size)]  # Now stores a tuple of state and order
        self.start = None
        self.end = None
        self.step_font = pygame.font.Font(None, 24)  # Initialize font; specify your font path here if not using default
        self.message_font = pygame.font.Font(None, 30)  # Initialize font; specify your font path here if not using default
        self.path = None

    def set_start(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.start = (x, y)
            self.grid[y][x] = (self.START, None)

    def set_end(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.end = (x, y)
            self.grid[y][x] = (self.END, None)

    def set_obstacle(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = (self.OBSTACLE, None)

    def set_random_obstacles(self, n):
        for _ in range(n):
            x, y = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            self.set_obstacle(x, y)

    def set_cell_state(self, x, y, state, order=None):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = (state, order)

    def get_cell_state(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        return None

    def is_obstacle(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x] == (self.OBSTACLE, None)
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and not self.is_obstacle(x, y)
    
    def draw(self, screen):
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                state, order = self.get_cell_state(x, y)  # Unpack state and order
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

                if order is not None:
                    order_text = self.step_font.render(str(order), True, WHITE)
                    text_rect = order_text.get_rect(center=(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                    screen.blit(order_text, text_rect)

    def mark_path(self, path):
        for x, y in path:
            self.set_cell_state(x, y, self.PATH)

    def render_message(self, message, screen):
        # Container dimensions and position
        container_width = 130  # Adjust the width as needed
        container_height = 50  # Adjust the height as needed
        container_x = (WINDOW_SIZE - container_width) // 2
        container_y = (WINDOW_SIZE - container_height) // 2

        # Container color
        container_color = (50, 50, 50)  # Dark gray (or choose another dark color)

        # Text color
        text_color = (255, 255, 255)  # White

        # Draw the container rectangle
        pygame.draw.rect(screen, container_color, [container_x, container_y, container_width, container_height])

        # Render the message text
        text = self.message_font.render(message, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

        # Blit the text onto the screen, centered within the container
        screen.blit(text, text_rect)