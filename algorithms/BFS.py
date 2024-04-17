from collections import deque
from memory_profiler import profile

class BFS:
    def __init__(self, board):
        self.board = board
        self.queue = deque([((self.board.start), [self.board.start])])
        self.visited = set([self.board.start])
        self.end = board.end
    
    def step(self):
        """
        Returns:
        - True if the algorithm has finished
        - False if the algorithm has not finished
        """
        if self.board.path:
            return True
        
        if not self.queue:
            self.board.path = []
            return True
        
        current, path = self.queue.popleft()
        x, y = current
        if current != self.board.start:
            self.board.set_cell_state(x, y, self.board.VISITED)

        if current == self.end:
            self.board.path = path
            self.board.mark_path(path)
            return True
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            if self.board.is_valid_position(next_x, next_y) and next_pos not in self.visited:
                self.queue.append((next_pos, path + [next_pos]))
                self.visited.add(next_pos)
                self.board.set_cell_state(next_x, next_y, self.board.VISITING)

        return False