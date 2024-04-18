import pygame
import random
import math
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
        'swamp': 2,
        'mountain': 3,
        'ocean': float('inf')
    }
    # Weights regarding the probability of each biome being generated
    biomes_weights = {
        'plains': 0.4,
        'swamp': 0.2,
        'mountain': 0.3,
        'ocean': 0.1
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

    def set_biomes(self, num_centers, seed=None, max_radius=20):
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
                selected_biome = None
                for center_x, center_y, biome in centers:
                    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                    if distance < min_distance and distance <= max_radius:
                        min_distance = distance
                        selected_biome = biome
                self.set_cell_state(x, y, self.TERRAIN)
                if selected_biome is not None:
                    self.set_cell_cost(x, y, self.biomes_movement_cost[selected_biome])

    def is_valid_position(self, x, y):
        cost = self.get_cell_cost(x, y)
        return cost is not None and cost != float('inf')

    def draw(self, screen):
        cell_x = WINDOW_SIZE // self.size[0]
        cell_y = WINDOW_SIZE // self.size[1]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                rect = pygame.Rect(x * cell_x, y * cell_y, cell_x, cell_y)
                state = self.get_cell_state(x, y)
                terrain = self.get_cell_cost(x, y)
                color = BLACK  # Default color
                if terrain == self.biomes_movement_cost['plains']:
                    color = LIGHT_GREEN  # Light green for plains, easy to traverse
                elif terrain == self.biomes_movement_cost['swamp']:
                    color = DARK_GREEN  # Dark green for swamp, more challenging
                elif terrain == self.biomes_movement_cost['mountain']:
                    color = BROWN  # Brown for hills, difficult terrain
                elif terrain == self.biomes_movement_cost['ocean']:
                    color = DARK_BLUE  # Dark blue for ocean, impassable

                if state == self.VISITING:
                    color = self.darken_color(color, 50)
                elif state == self.VISITED:
                    color = self.darken_color(color, 80)
    
                if state == self.START:
                    color = GREEN  # Bright green for the start point
                elif state == self.END:
                    color = RED  # Red for the end point

                if state == self.PATH:
                    color = GOLD
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, -1)

    def mark_path(self, path):
        total_cost = 0
        for x, y in path:
            self.set_cell_state(x, y, self.PATH)
            total_cost += self.get_cell_cost(x, y)
        self.path = path
        self.total_cost = total_cost

    @staticmethod
    def darken_color(color, percentage=30):
        """Darken a given RGB color by the specified percentage, adjusted by color."""
        # Adjust darkening based on color to keep the visual distinctiveness
        r, g, b = color
        if color == LIGHT_GREEN:  # plains
            dark_factor = (100 - percentage/2) / 100.0  # less darkening for plains
        else:
            dark_factor = (100 - percentage) / 100.0
        return (max(int(r * dark_factor), 0), max(int(g * dark_factor), 0), max(int(b * dark_factor), 0))
