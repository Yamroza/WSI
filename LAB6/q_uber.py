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
        if x == 0 and y == 0 or x == n-1 and y == n-1:
            pass
        else:
            if lab[x][y] != 1:
                lab[x][y] = 1
                made_holes += 1
    return lab


def deep_first_search(lab) -> bool: 
    return True

def save_lab_to_file(lab, file_name):
    with open(file_name, 'w') as data:
        for row in lab:
            line = ""
            for element in row:
                line += str(element) + " "
            line += '\n'
            data.write(line)

def read_lab_from_file(file_name):
    lab = []
    with open(file_name, 'r') as data:
        content = data.read()
        for number, line in enumerate(content.splitlines()):
            lab.append([])
            for element in range(len(line.split())):
                lab[number].append(int(line.split()[element]))
    return lab

class Musk_Taxi:
    def __init__(self, rows, holes):
        self.rows = rows
        self.lab = generate_lab(self.rows, holes)
        self.x = 0
        self.y = 0
        self.x_done = 7
        self.y_done = 7
        self.available_moves = self.check_available_moves()
        
    def check_available_moves(self):
        available_moves = []
        for y, x in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            if self.x + x > -1 and self.x + x < self.rows:
                if self.y + y > -1 and self.y + y < self.rows:
                    if self.lab[self.x + x][self.y + y] == 0:
                        available_moves.append([self.y+y,self.x+x])
        return available_moves


# TESTS:
def main():
    # taxi = Musk_Taxi(8, 15)
    # for row in taxi.lab:
    #     print(row)
    # print(taxi.available_moves)

    lab = generate_lab(5,5)
    save_lab_to_file(lab, 'saved_lab.txt')

    lab = read_lab_from_file('saved_lab.txt')
    for row in lab:
        print(row)


if __name__ == "__main__":
    main()