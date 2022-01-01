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


class Node:
    def __init__(self, x, y, lab):
        self.x = x
        self.y = y
        self.lab = lab
        self.rows = len(lab)
        self.kids = self.check_available_moves()

    def check_available_moves(self):
        available_moves = []
        for y, x in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            if self.x + x > -1 and self.x + x < self.rows:
                if self.y + y > -1 and self.y + y < self.rows:
                    if self.lab[self.x + x][self.y + y] == 0:
                        available_moves.append([self.y+y,self.x+x])
        return available_moves


def dfs(lab):
    first = Node(0,0,lab)
    last = Node(len(lab)-1, len(lab)-1,lab)
    possible_nodes = node_dfs([], lab, first)
    is_possible = False
    for element in possible_nodes:
        if element.x == last.x and element.y == last.y:
            is_possible = True
    return is_possible


def node_dfs(visited, lab, node):
    in_list = False
    for element in visited:
        if element.x == node.x and element.y == node.y:
            in_list = True
    if not in_list:
        visited.append(node)
        for kid in node.check_available_moves():
            node_dfs(visited, lab, Node(kid[1], kid[0], lab))
    return visited


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

    def drive(self, q_table, beta, gamma, epsilon):
        steps = []
        while not self.done:
            state = self.get_state()
            if uniform(0,1) < epsilon:
                action = randint(0,3)
            else:
                action = np.argmax(q_table[state])
            reward = self.make_action(action)
            steps.append(action)
            if reward == -10:
                if action%2 == 0:
                    steps.append(action+1)
                else:
                    steps.append(action-1)
            next_state = self.get_state()
            q_table = update_q_table(q_table, state, action, beta, gamma, reward, next_state)
        return steps, q_table

    def random_drive(self, random_table):
        steps = []
        while not self.done:
            state = self.get_state()
            action = choice(random_table[state])
            reward = self.make_action(action)
            steps.append(action)
            if reward == -10:
                random_table[state].remove(action)
                if action%2 == 0:
                    steps.append(action+1)
                else:
                    steps.append(action-1)
        return steps, random_table

    def no_of_states(self):
        return self.rows ** 2

    def get_state(self):
        state = self.x * self.rows + self.y
        return state


def generate_q_table(columns, rows):
    return np.zeros((columns, rows))

def generate_random_table(states):
    random_table = []
    for _ in range(states):
        random_table.append([0,1,2,3])
    return random_table


def update_q_table(q_table, state, action, beta, gamma, reward, next_state):
    next_state_max = np.max(q_table[next_state])
    # q_table[state, action] = (1-beta) * q_table[state, action] + beta * (reward + gamma * next_state_max - q_table[state, action])
    q_table[state, action] += beta * (reward + gamma * next_state_max - q_table[state, action])

    return q_table
    

# TESTS:
def main():

    # # parameters:
    # epsilon = 0.1
    # gamma = 0.6
    # beta = 0.1      #  learning rate
    
    # # expected_steps = [3, 3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 3, 3, 3, 3, 3]
    # # steps = []
    # q_table = generate_q_table(64, 4)
    # # random_table = generate_random_table(64)
    # # iteration_no = 0
    # # interval_steps = []
    # # # while steps != expected_steps:
    # # for _ in range(10000):
    # #     taxi = Musk_Taxi(8, 5)
    # #     steps = []
    # #     steps, random_table = taxi.random_drive(random_table)
    # #     iteration_no += 1
    # #     if iteration_no % 10 == 0:
    # #         interval_steps.append(steps)
    # # print(interval_steps[-1])
        

    # interval_steps = []
    # for i in range(10000):
    #     steps = []
    #     taxi = Musk_Taxi(8, 5)
    #     steps, q_table = taxi.drive(q_table, beta, gamma, epsilon)
    #     if i % 20 == 0:
    #         interval_steps.append(steps)

    # print(interval_steps[-1])

    lab = read_lab_from_file('LAB6/saved_lab.txt')
    print(dfs(lab))

    # lab = generate_lab(8, 20)
    # save_lab_to_file(lab, 'LAB6/saved_lab.txt')
    



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