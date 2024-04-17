import heapq

class Dijkstra:
    def __init__(self, board):
        self.board = board
        self.priority_queue = []
        heapq.heappush(self.priority_queue, (0, self.board.start, [self.board.start]))  # (cost, position, path)
        self.visited = set()
        self.end = board.end

    def step(self):
        """
        Perform one step of the Dijkstra algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True
        
        if not self.priority_queue:
            self.board.path = []
            return True

        cost, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        # Mark the current cell as visited with its cost
        if current != self.board.start:
            self.board.set_cell_state(x, y, self.board.VISITED, cost)

        if current in self.visited:
            return False

        self.visited.add(current)

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                new_cost = cost + 1
                heapq.heappush(self.priority_queue, (new_cost, next_pos, path + [next_pos]))
                self.board.set_cell_state(next_x, next_y, self.board.VISITING, new_cost)

        return False
