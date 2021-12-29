from random import randint, choice, uniform
from typing import AsyncIterator
import numpy as np
from numpy.core.fromnumeric import argmax

EPSILON = 0.1
GAMMA = 0.6
ALPHA = 0.1 #  learning rate (beta u Wawrzyńskiego)

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
        self.lab = read_lab_from_file('saved_lab.txt')
        self.x = 0
        self.y = 0
        self.x_done = self.rows - 1
        self.y_done = self.rows - 1
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
        # w dół
        if action == 0:     
            if self.x + 1 == self.rows or self.lab[self.x + 1][self.y] == 1:
                return -10
            else:
                self.x += 1
                if self.y == self.y_done and self.x == self.x_done:
                    return 20
                else:
                    return -1
        # w górę
        elif action == 1:   
            if self.x - 1 < 0 or self.lab[self.x - 1][self.y] == 1:
                return -10
            else:
                self.x -= 1
                if self.y == self.y_done and self.x == self.x_done:
                    return 20
                else:
                    return -1
        # w lewo
        elif action == 2:   
            if self.y - 1 < 0 or self.lab[self.x][self.y - 1] == 1:
                return -10
            else:
                self.y -= 1
                if self.y == self.y_done and self.x == self.x_done:
                    return 20
                else:
                    return -1
        # w prawo
        elif action == 3:   
            if self.y + 1 == self.rows or self.lab[self.x][self.y + 1] == 1:
                return -10 
            else:
                self.y += 1
                if self.y == self.y_done and self.x == self.x_done:
                    return 20
                else:
                    return -1
    

    def is_done(self):
        if self.y == self.y_done and self.x == self.x_done:
            return True

    def no_of_states(self):
        return self.rows ** 2

    def get_state(self):
        state = self.x * self.rows + self.y
        return state

    def q_table(self):
        q_table = np.zeros((self.no_of_states(), 4))


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


# TESTS:
def main():
    taxi = Musk_Taxi(5, 5)
    q_table = np.zeros((taxi.no_of_states(), 4))

    for _ in range(100):
        taxi = Musk_Taxi(5, 5)
        done = False

        while not done:
            state = taxi.get_state()
            if uniform(0,1) < EPSILON:
                action = randint(0,3)
            else:
                action = np.argmax(q_table[state])
            reward = taxi.make_action(action)
            done = taxi.is_done()
            new_state = taxi.get_state()
            new_state_max = np.max(q_table[new_state])
            q_table[state, action] = (1-ALPHA) * q_table[state, action] + ALPHA * (reward + GAMMA * new_state_max - q_table[state, action])

    taxi = Musk_Taxi(5, 5)
    for row in taxi.lab:
        print(row)
    done = False
    steps = 0
    while not done:
        state = taxi.get_state()
        if uniform(0,1) < EPSILON:
            action = randint(0,3)
        else:
            action = np.argmax(q_table[state])
        reward = taxi.make_action(action)
        done = taxi.is_done()
        new_state = taxi.get_state()
        new_state_max = np.max(q_table[new_state])
        q_table[state, action] = (1-ALPHA) * q_table[state, action] + ALPHA * (reward + GAMMA * new_state_max - q_table[state, action])
        steps += 1

    print(steps)



    # for row in taxi.lab:
    #     print(row)
    # print(taxi.available_moves)

    # reward = taxi.make_action(0)
    # print("Reward: ", reward)
    # print(taxi.x, ", " , taxi.y)
    # for row in taxi.lab:
    #     print(row)

    # reward = taxi.make_action(3)
    # print("Reward: ", reward)
    # print(taxi.x, ", " , taxi.y)
    # for row in taxi.lab:
    #     print(row)

    # lab = generate_lab(5,5)
    # save_lab_to_file(lab, 'saved_lab.txt')

    # lab = read_lab_from_file('saved_lab.txt')
    # for row in lab:
    #     print(row)


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