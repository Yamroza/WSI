class Pawn:
    def __init__(self, x, y, colour):
        self._x = x
        self._y = y
        self._loser = False
        self._moves = []
        self._colour = colour

    def colour(self):
        return self._colour

    def x(self):
        return self._x

    def y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def moves(self):
        return self._moves

    def add_move(self, krotka):
        self._moves.append(krotka)

    def clear_moves(self):
        self._moves = []

    def update_moves(self, lista):
        self.clear_moves()
        for element in lista:
            self.add_move(element)
