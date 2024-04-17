import pygame
import random
from settings import *

class Board:
    # States
    EMPTY = 0
    TERRAIN = 1
    START = 2
    END = 3
    VISITING = 4
    VISITED = 5
    PATH = 6
    # Cost for each terrain type
    biomes_movement_cost = {
        'plains': 1,
        'swamp': 3,
        'mountain': 5,
        'ocean': float('inf')
    }
    # Weights regarding the probability of each biome being generated
    biomes_weights = {
        'swamp': 0.4,
        'mountain': 0.4,
        'ocean': 0.2
    }

    def __init__(self, size, start, end):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size[0])] for _ in range(size[1])]
        self.cost = [[1 for _ in range(size[0])] for _ in range(size[1])]
        self.set_cell_state(*start, self.START)
        self.set_cell_state(*end, self.END)
        self.path = None
        self.start = start
        self.end = end

    def set_cell_state(self, x, y, state, cost=None):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.grid[y][x] = state
        else:
            raise ValueError(f"Invalid cell position: ({x}, {y})")

    def set_cell_cost(self, x, y, cost):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            self.cost[y][x] = cost
        else:
            raise ValueError(f"Invalid cell position: ({x}, {y})")

    def get_cell_state(self, x, y):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.grid[y][x]
        return None

    def get_cell_cost(self, x, y):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return self.cost[y][x]
        return float('inf')

    def set_biomes(self, num_centers, seed=None):
        if seed is not None:
            random.seed(seed)
        centers = []
        for _ in range(num_centers):
            x, y = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
            biome = random.choices(list(self.biomes_weights.keys()), list(self.biomes_weights.values()))[0]
            centers.append((x, y, biome))
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                min_distance = float('inf')
                for center_x, center_y, biome in centers:
                    distance = abs(x - center_x) + abs(y - center_y)
                    if distance < min_distance:
                        min_distance = distance
                        self.set_cell_state(x, y, self.TERRAIN)
                        self.set_cell_cost(x, y, self.biomes_movement_cost[biome])

    def draw(self, screen):
        cell_x = WINDOW_SIZE // self.size[0]
        cell_y = WINDOW_SIZE // self.size[1]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                rect = pygame.Rect(x * cell_x, y * cell_y, cell_x, cell_y)
                state = self.get_cell_state(x, y)
                terrain = self.get_cell_cost(x, y)
                color = WHITE  # Default color
                # Define colors based on state and terrain
                if state == self.TERRAIN:
                    if terrain == 'plains':
                        color = LIGHT_GREEN  # Light green for plains, easy to traverse
                    elif terrain == 'swamp':
                        color = DARK_GREEN  # Dark green for swamp, more challenging
                    elif terrain == 'hill':
                        color = BROWN  # Brown for hills, difficult terrain
                    elif terrain == 'ocean':
                        color = DARK_BLUE  # Dark blue for ocean, impassable
                elif state == self.START:
                    color = GREEN  # Bright green for the start point
                elif state == self.END:
                    color = RED  # Red for the end point
                elif state == self.VISITING:
                    color = LIGHT_BLUE  # Light blue for cells currently being visited
                elif state == self.VISITED:
                    color = BLUE  # Standard blue for cells that have been visited
                elif state == self.PATH:
                    color = GOLD  # Gold for the path from start to end

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