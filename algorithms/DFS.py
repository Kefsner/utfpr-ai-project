class DFS:
    def __init__(self, board):
        self.board = board
        self.stack = [((self.board.start), [self.board.start])]  # Use a list as a stack
        self.visited = set([self.board.start])
        self.end = board.end
        self.end
    
    def step(self):
        if self.board.path:
            return True
        
        if not self.stack:  # Check if the stack is empty
            self.board.path = []
            return True
        
        current, path = self.stack.pop()  # Use pop to get the last element
        x, y = current
        
        if current != self.board.start:
            self.board.set_cell_state(x, y, self.board.VISITED)

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True
        
        for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]: # This define the order of the search
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                self.stack.append((next_pos, path + [next_pos]))  # Add to the stack
                self.visited.add(next_pos)
                self.board.set_cell_state(next_x, next_y, self.board.VISITING)

        return False
