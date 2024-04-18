import heapq

import heapq

class AStar:
    def __init__(self, board):
        self.board = board
        self.priority_queue = []  # Using a heap as a priority queue
        self.start = self.board.start
        self.end = self.board.end
        self.visited = set([self.start])
        self.cost_from_start = {self.start: 0}  # Tracks g(n), the cost from the start node to n
        # Initialize with the start node, where f(n) = g(n) + h(n)
        heapq.heappush(self.priority_queue, (self.heuristic(self.start), self.start, [self.start]))  # (f(n), position, path)

    def heuristic(self, position):
        """ Calculate the Manhattan distance to the goal. """
        x, y = position
        goal_x, goal_y = self.end
        return abs(x - goal_x) + abs(y - goal_y)

    def step(self):
        """
        Perform a single step of the A* algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True

        if not self.priority_queue:
            self.board.path = []
            return True

        # Get the node with the smallest f(n) = g(n) + h(n)
        current_f, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True

        self.board.set_cell_state(x, y, self.board.VISITED)

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Left, Right, Up, Down
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                new_cost = self.cost_from_start[current] + self.board.get_cell_cost(next_x, next_y)
                if next_pos not in self.cost_from_start or new_cost < self.cost_from_start[next_pos]:
                    self.cost_from_start[next_pos] = new_cost
                    f = new_cost + self.heuristic(next_pos)
                    heapq.heappush(self.priority_queue, (f, next_pos, path + [next_pos]))
                    self.visited.add(next_pos)
                    self.board.set_cell_state(next_x, next_y, self.board.VISITING)

        return False
