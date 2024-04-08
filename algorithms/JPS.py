import heapq

class JPS:
    def __init__(self, board):
        self.board = board
        self.end = board.end
        self.priority_queue = []
        start_h_cost = self.heuristic(board.start)
        heapq.heappush(self.priority_queue, (start_h_cost, start_h_cost, board.start, [board.start]))

    def heuristic(self, position):
        """Manhattan distance"""
        x, y = position
        end_x, end_y = self.end
        return abs(x - end_x) + abs(y - end_y)

    def jump(self, current, direction, path):
        """
        Attempt to jump in the specified direction from the current node.
        Returns the new position if a jump point is found, None otherwise.
        """
        next_position = (current[0] + direction[0], current[1] + direction[1])
        if not self.board.is_valid_position(*next_position):
            return None  # Hit an obstacle or the edge of the grid

        if next_position == self.end:
            return next_position  # Reached the goal
        
        # Check for forced neighbors along the jump to identify a jump point
        # This part is simplified; full implementation requires checking adjacent cells for forced neighbors

        # Continue jumping in the current direction
        return self.jump(next_position, direction, path + [next_position])

    def step(self):
        """
        Perform one step of the JPS algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if not self.priority_queue:
            self.board.path = []
            return True

        _, h_cost, current, path = heapq.heappop(self.priority_queue)

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Cardinal directions only for simplicity
            jump_point = self.jump(current, direction, path)
            if jump_point and jump_point not in path:
                new_g_cost = len(path)  # Assuming uniform cost
                new_h_cost = self.heuristic(jump_point)
                f_cost = new_g_cost + new_h_cost
                heapq.heappush(self.priority_queue, (f_cost, new_h_cost, jump_point, path + [jump_point]))

        return False
