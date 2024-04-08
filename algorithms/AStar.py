
import heapq

class AStar:
    def __init__(self, board):
        self.board = board
        self.end = board.end
        # The priority queue will store tuples of (f_cost, h_cost, position, path)
        self.priority_queue = []
        start_h_cost = self.heuristic(board.start)
        heapq.heappush(self.priority_queue, (start_h_cost, start_h_cost, board.start, [board.start]))
        self.visited = set()

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
        Perform one step of the A* algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True
        
        if not self.priority_queue:
            self.board.path = []
            return True

        _, h_cost, current, path = heapq.heappop(self.priority_queue)
        x, y = current

        if current in self.visited:
            return False

        self.visited.add(current)

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
                new_g_cost = len(path)  # Assuming a uniform cost of 1 per step
                new_h_cost = self.heuristic(next_pos)
                f_cost = new_g_cost + new_h_cost
                heapq.heappush(self.priority_queue, (f_cost, new_h_cost, next_pos, path + [next_pos]))
                # Optionally, mark cells being considered for visitation
                self.board.set_cell_state(next_x, next_y, self.board.VISITING, None)  # VISITING without order

        return False
