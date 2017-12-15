class PipesGrid(object):
    """grid containing pipes"""

    def __init__(self, rows: int, cols: int):
        assert type(rows) == type(cols) == int and rows > 0 and cols > 0
        self.grid: list(list(str)) = [["" for i in range(rows)] for j in range(cols)]
