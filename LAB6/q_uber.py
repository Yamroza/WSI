from random import randint, choice, uniform
import numpy as np


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
        self.holes = holes
        # self.lab = generate_lab(self.rows, holes)
        self.lab = read_lab_from_file('LAB6/saved_lab.txt')
        self.x = 0
        self.y = 0
        self.x_done = self.rows - 1
        self.y_done = self.rows - 1
        self.done = False
        self.available_moves = self.check_available_moves()
        

    def check_available_moves(self):
        available_moves = []
        for y, x in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            if self.x + x > -1 and self.x + x < self.rows:
                if self.y + y > -1 and self.y + y < self.rows:
                    if self.lab[self.x + x][self.y + y] == 0:
                        available_moves.append([self.y+y,self.x+x])
        return available_moves


    def make_action(self, action):
        previous_position = self.x, self.y
        if action == 0: 
            self.x += 1
        elif action == 1: 
            self.x -= 1
        elif action == 2: 
            self.y -= 1
        elif action == 3: 
            self.y += 1
        if self.y == self.y_done and self.x == self.x_done:
            self.done = True
            return 20
        elif self.x == self.rows or self.y == self.rows or self.x < 0 or self.y < 0:
            self.x, self.y = previous_position
            return -10
        elif self.lab[self.x][self.y] == 1:
            self.done = True
            return -10
        else:
            return -1

            

    def is_done(self):
        if self.y == self.y_done and self.x == self.x_done:
            return True

    def no_of_states(self):
        # real number of states is decreased by number of holes, but 
        # here it's easier to leave them and never use them than to delete them
        return self.rows ** 2

    def get_state(self):
        # every state number is unique
        state = self.x * self.rows + self.y
        return state


class Random_car:
    def __init__(self, musk_taxi = Musk_Taxi(5, 3)):
        self.taxi = musk_taxi

    def steps(self):
        steps = 0
        while not self.taxi.is_done():
            move = choice(self.taxi.check_available_moves())
            self.taxi.y, self.taxi.x = move
            steps += 1
        return steps


def generate_q_table(columns, rows):
    return np.zeros((columns, rows))

def update_q_table(q_table, state, action, beta, gamma, reward, new_state):
    new_state_max = np.max(q_table[new_state])
    q_table[state, action] = (1-beta) * q_table[state, action] + beta * (reward + gamma * new_state_max - q_table[state, action])
    

# TESTS:
def main():

    # parameters:
    epsilon = 0.1
    gamma = 0.6
    beta = 0.1      #  learning rate

    taxi = Musk_Taxi(5, 5)
    q_table = generate_q_table(taxi.no_of_states(), 4)

    interval_steps = []
    for i in range(100):
        steps = []
        taxi = Musk_Taxi(5, 5)
        while not taxi.done:
            state = taxi.get_state()
            if uniform(0,1) < epsilon:
                action = randint(0,3)
            else:
                action = np.argmax(q_table[state])
            if i % 20 == 0:
                steps.append(action)
            reward = taxi.make_action(action)
            new_state = taxi.get_state()
            update_q_table(q_table, state, action, beta, gamma, reward, new_state)
        if i % 20 == 0:
            interval_steps.append(steps)

    print(interval_steps[-1])
    # taxi = Musk_Taxi(5, 5)
    # for row in taxi.lab:
    #     print(row)
    # steps = 0
    # while not taxi.done:
    #     state = taxi.get_state()
    #     if uniform(0,1) < epsilon:
    #         action = randint(0,3)
    #     else:
    #         action = np.argmax(q_table[state])
    #     reward = taxi.make_action(action)
    #     new_state = taxi.get_state()
    #     update_q_table(q_table, state, action, beta, gamma, reward, new_state)
    #     steps += 1
    

    # print(steps)


    # random_car = Random_car()
    # steps = random_car.steps()
    # print(steps)

if __name__ == "__main__":
    main()

# AKCJE:
# action 1 - w dół
# action 2 - w górę
# action 3 - w lewo
# action 4 - w prawo

# KARY:
# poza pole? : -10
# w stażystę : -10
# ruch po prostu : -1
# dotrze do celu : +20 