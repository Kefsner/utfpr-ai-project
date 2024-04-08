import heapq

class GreedyBFS:
    def __init__(self, board):
        self.board = board
        self.priority_queue = []
        self.end = board.end
        # Initial push: (heuristic cost, position, path)
        heapq.heappush(self.priority_queue, (self.heuristic(board.start), board.start, [board.start]))
        self.visited = set(board.start)

    def heuristic(self, position):
        """
        Calculate the heuristic cost from a given position to the end position.
        For simplicity, we use Manhattan distance as the heuristic.
        """
        x, y = position
        end_x, end_y = self.end
        return abs(x - end_x) + abs(y - end_y)

    def step(self):
        """
        Perform one step of the Greedy Best-First Search algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True
        
        if not self.priority_queue:
            self.board.path = []
            return True

        _, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True

        if current != self.board.start:
            self.board.set_cell_state(x, y, self.board.VISITED, None)  # VISITED without order

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                self.visited.add(next_pos)
                heapq.heappush(self.priority_queue, (self.heuristic(next_pos), next_pos, path + [next_pos]))
                # Optionally, mark cells being considered for visitation
                self.board.set_cell_state(next_x, next_y, self.board.VISITING, None)  # VISITING without order

        return False
