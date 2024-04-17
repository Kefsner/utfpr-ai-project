import heapq

class GreedyBFS:
    def __init__(self, board):
        self.board = board
        self.priority_queue = []  # Use a heap as a priority queue
        self.visited = set([self.board.start])
        self.start = self.board.start
        self.end = self.board.end
        # Initialize with the start node, calculating the heuristic as the priority
        heapq.heappush(self.priority_queue, (self.heuristic(self.start), self.start, [self.start]))  # (heuristic, position, path)

    def heuristic(self, position):
        """ Calculate the Manhattan distance to the goal. """
        x, y = position
        goal_x, goal_y = self.end
        return abs(x - goal_x) + abs(y - goal_y)

    def step(self):
        """
        Perform a single step of the Greedy BFS algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True

        if not self.priority_queue:
            self.board.path = []
            return True

        # Get the node with the smallest heuristic value
        _, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True

        self.board.set_cell_state(x, y, self.board.VISITED)

        # Explore neighbors
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                heapq.heappush(self.priority_queue, (self.heuristic(next_pos), next_pos, path + [next_pos]))
                self.visited.add(next_pos)
                self.board.set_cell_state(next_x, next_y, self.board.VISITING)

        return False
