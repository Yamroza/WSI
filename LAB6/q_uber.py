from random import randint

def generate_lab(n, holes):
    lab = []
    for i in range(n):
        lab.append([])
    for row in lab:
        for i in range(n):
            row.append(0)
    made_holes = 0
    while made_holes < holes:
        x, y = randint(0, n-1), randint(0, n-1)
        if x != 0 and y != 0:
            if x != n-1 and y != -1:
                if lab[x][y] != -1:
                    lab[x][y] = 1
                    made_holes += 1
    return lab


def deep_first_search(lab) -> bool: 
    return True


class Musk_Taxi:
    def __init__(self, rows):
        self.rows = rows
        self.lab = generate_lab(self.rows, 15)
        self.x = 0
        self.y = 0
        self.x_done = 7
        self.y_done = 7
        self.available_moves = self.check_available_moves()
        
    def check_available_moves(self):
        available_moves = []
        for y  in [-1, 0, 1]:
            for x in [-1, 0, 1]:
                if self.x + x > -1 and self.x + x < self.rows:
                    if self.y + y > -1 and self.y + y < self.rows:
                        if self.lab[self.y + y][self.x + x] == 0:
                            available_moves.append([x,y])
        return available_moves

taxi = Musk_Taxi(8)
for row in taxi.lab:
    print(row)
print(taxi.available_moves)