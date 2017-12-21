from math import log2
from random import choice

N, E, S, O = 1, 2, 4, 8
score_unit = 10


class PipesGrid(object):
    """grid containing pipes"""

    def __init__(self, rows: int, cols: int):
        assert type(rows) == type(cols) == int and rows > 0 and cols > 0
        self.score = 0
        self.rows, self.cols = rows, cols
        self.grid = [[('R', 0) for i in range(cols)] for j in range(rows)]
        for col in range(cols):
            for row in range(rows):
                if col in (0, cols - 1):
                    self.grid[row][col] = ['B', 2] if col == 0 else ['B', 8]
                else:
                    self.grid[row][col] = ['R', self.getRandomPipe()]
        for col in (0, cols - 1):
            for row in range(rows):
                self.colorConnected(self.getAllConnected(row, col))

    def rotate(self, b: int, dir: str) -> int:
        """in this function, we manipulate b as a 4 bites number"""
        assert self.isByte(b) and dir in ("r", "l")  # r for right, l for left
        if dir == "r":
            b <<= 1
            if b > 15:  # if b > 15 we have the 5th bite to 1
                b = (b & 15) | 1  # ( 1___0 & 01111 ) | 0___1 makes that bite right
        elif dir == "l":
            if b & 1:  # we test if b = xyz1
                b |= 16  # ( xyz1 | 10000 ) = 1xyz1 -> 01xyz
            b >>= 1
        return b

    def isInGrid(self, row: int, col: int) -> bool:
        return type(row) == type(col) == int and 0 <= row < self.rows and \
               0 <= col < self.cols

    def isByte(self, b: int) -> bool:
        return type(b) is int and 1 <= b <= 15

    def getAllConnected(self, row: int, col: int):
        assert self.isInGrid(row, col)
        connected = [(row, col)]
        stack = [(row, col)]
        while stack:  # while stack not empty
            r, c = stack.pop()
            for d in (N, E, S, O):
                dr = (-1, 0, 1, 0)[int(log2(d))]  # delta row
                dc = (0, 1, 0, -1)[int(log2(d))]  # delta column
                if self.isInGrid(r + dr, c + dc) and (r + dr, c + dc) not in connected and \
                        self.isConnected(self.getPipe(r, c), self.getPipe(r + dr, c + dc), d):
                    stack.append((r + dr, c + dc))
                    connected.append((r + dr, c + dc))

        return connected

    def collapse(self) -> None:
        for col in range(1, self.cols - 1):
            for row in range(self.rows):
                if self.grid[row][col][0] == "G":
                    for i in range(row, 1, -1):
                        self.grid[row][col] = self.grid[row - 1][col]
                    self.grid[0][col] = ['R', self.getRandomPipe()]
                    self.score += score_unit

    def makeRotation(self, row: int, col: int, dir: str) -> list:
        assert self.isInGrid(row, col) and dir in ('r', 'l')
        if col in (0, self.cols - 1):
            return []
        self.grid[row][col][1] = self.rotate(self.getPipe(row, col), dir)
        changed = []
        for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.isInGrid(row + dr, col + dc):
                connected = self.getAllConnected(row + dr, col + dc)
                self.colorConnected(connected)
                changed += connected
        return changed

    def colorConnected(self, connected: list((int, int))) -> None:
        """Colors all the given connected pipes"""
        pipe_color = 'R'
        columns = [pos[1] for pos in connected]
        if 0 in columns or (self.cols - 1) in columns:
            pipe_color = 'B'
        if 0 in columns and (self.cols - 1) in columns:
            pipe_color = 'G'
        for r, c in connected:
            self.grid[r][c][0] = pipe_color

    def isConnected(self, b1: int, b2: int, d: int) -> bool:
        """
             b1 is the first pipe and b2 the second
             d is the direction (N, E, S, O) from b1 to b2

             *   -------------------------------
             *      N = 0001    [log2(N) = 0]
             *      E = 0010    [log2(E) = 1]
             *      S = 0100    [log2(S) = 2]
             *      O = 1000    [log2(O) = 3]
             *   -------------------------------
             * ╔═════════╦═════════╦═════════╗
             * ║         ║         ║         ║
             * ║         ║ O b2 E  ║         ║
             * ║         ║    S    ║         ║
             * ╠═════════╬═════════╬═════════╣
             * ║         ║    N    ║         ║
             * ║  O b2 E ║ O b1 E  ║  O b2 E ║
             * ║         ║    S    ║         ║
             * ╠═════════╬═════════╬═════════╣
             * ║         ║    N    ║         ║
             * ║         ║   b2    ║         ║
             * ║         ║         ║         ║
             * ╚═════════╩═════════╩═════════╝
             When b2 is at b1's North, b1 connects if (b1 & S)
             When b2 ---------- South, b1 connects if (b1 & N)
             When b2 ---------- East , b1 connects if (b1 & W)
             When b2 ---------- West , b1 connects if (b1 & E)

             Basically, we just test if b1 has the direction and b2 its opposite.
        """
        assert self.isByte(b1) and self.isByte(b2) and d in (N, E, S, O)
        return bool((b1 & d) and (b2 & (S, O, N, E)[int(log2(d))]))

    def getPipeNumber(self, row: int, col: int):
        assert self.isInGrid(row, col)
        color, pipe = self.grid[row][col]
        # return color + (str(pipe) if pipe < 10 else ['A', 'B', 'C', 'D', 'E', 'F'][pipe - 10])
        return {'R': 0, 'G': 1, 'B': 2}[color] * 16 + pipe

    def getPipe(self, row: int, col: int) -> int:
        assert self.isInGrid(row, col)
        return self.grid[row][col][1]

    def getRandomPipe(self) -> int:
        nb_bites = choice([2 for i in range(65)] + [3 for i in range(30)] + [4 for i in range(5)])
        if nb_bites == 2:
            return choice((3, 5, 6, 9, 10, 12))
        if nb_bites == 3:
            return choice((7, 11, 13, 14))
        if nb_bites == 4:
            return 15


   # # ------------------------------------------------------------------------------
  #  def init_ini(file='meilleurs_scores.ini'):  # creates file if needed
  #      """create a .ini files for high-score with ezcli fonction """
  #      try:
   #         read_ini(file)
   #     except:
   #         d = {}
   #         for area in set([i * j for i in range(5, 20) for j in range(5, 20)]):
   #             d[area] = {}
   #             for i in range(1, 11):
   #                 d[area]['noone %s' % (i)] = 10000
   #         write_ini(file, d)
   #
   # # ------------------------------------------------------------------------------
   # def write(area, nick, score, file='meilleurs_scores.ini'):  # write user nameand his score if player do a high-score
   #     """write a .ini files for high-score with ezcli fonction """
    #    dernier_score = get(area, file)[-1]  # gets the last element of the best scores
   #     if dernier_score[0] >= score and not nick in [elem[1] for elem in get(area)]:
   #         dic = read_ini(file)
   #         dic[str(area)].pop(dernier_score[1])
   #         dic[str(area)][str(nick)] = score
   #         write_ini(file, dic)
   #         return true
   #     return false
   #
   # # ------------------------------------------------------------------------------
   # def get(area, file='meilleurs_scores.ini'):  # import of high-score for area chosen
  #      dic = read_ini(file)[str(area)]
   #     liste = [(dic[key], key) for key in dic.keys()]
   #     liste.sort()
   #     return liste