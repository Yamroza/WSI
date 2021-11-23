class Square:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._lifespan = 0 # 0-dostępny 1-zajęty 2-wykluczony

    def x(self):
        return self._x

    def y(self):
        return self._y

    def lifespan(self):
        return self._lifespan

    def set_lifespan(self, new_lifespan):
        self._lifespan = new_lifespan

    def get_description(self):
        pass