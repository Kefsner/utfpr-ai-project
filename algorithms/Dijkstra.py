import heapq

class Dijkstra:
    def __init__(self, board):
        self.board = board
        self.priority_queue = []  # Using a heap as a priority queue
        self.start = self.board.start
        self.end = self.board.end
        self.visited = set([self.start])
        # Starting with the start node in the queue with a distance of 0
        heapq.heappush(self.priority_queue, (0, self.start, [self.start]))  # (cost, position, path)

    def step(self):
        """
        Performs a single step of the Dijkstra algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True

        if not self.priority_queue:
            self.board.path = []
            return True

        # Get the node with the smallest distance
        current_cost, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        # Mark visiting status on the board
        if current != self.start:
            self.board.set_cell_state(x, y, self.board.VISITED)

        # Check if the current node is the destination
        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True

        # Explore neighbors
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            if self.board.is_valid_position(next_x, next_y) and (next_x, next_y) not in self.visited:
                next_cost = current_cost + self.board.get_cell_cost(next_x, next_y)
                heapq.heappush(self.priority_queue, (next_cost, (next_x, next_y), path + [(next_x, next_y)]))
                self.visited.add((next_x, next_y))
                self.board.set_cell_state(next_x, next_y, self.board.VISITING)

        return False
