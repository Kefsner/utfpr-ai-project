class DFS:
    def __init__(self, board):
        self.board = board
        self.stack = [((self.board.start), [self.board.start], 1)]  # Use a list as a stack
        self.visited = set([self.board.start])
        self.end = board.end
        self.end
        self.order = 1
    
    def step(self):
        """
        Perform one step of the DFS (Depth-First Search) algorithm.

        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True
        
        if not self.stack:  # Check if the stack is empty
            self.board.path = []
            return True
        
        current, path, order = self.stack.pop()  # Use pop to get the last element
        x, y = current
        
        if current != self.board.start:
            self.board.set_cell_state(x, y, self.board.VISITED, order)

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True
        
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:  # Optional: Change the order to explore differently
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                self.stack.append((next_pos, path + [next_pos], self.order))  # Add to the stack
                self.visited.add(next_pos)
                self.board.set_cell_state(next_x, next_y, self.board.VISITING, self.order)
                self.order += 1

        return False
