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
        # self.available_moves = self.check_available_moves()
        
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
            steps.append(action)
            reward = self.make_action(action)
            next_state = self.get_state()
            q_table = update_q_table(q_table, state, action, beta, gamma, reward, next_state)
        return steps, q_table
            
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


# class Random_car(Musk_Taxi):
#     def __init__(self, musk_taxi = Musk_Taxi(8, 3)):
#         self.taxi = musk_taxi

#     def steps(self):
#         steps = 0
#         while not self.taxi.is_done():
#             move = choice(self.taxi.check_available_moves())
#             self.taxi.y, self.taxi.x = move
#             steps += 1
#         return steps

#     def check_available_moves(self):
#         available_moves = []
#         for y, x in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
#             if self.taxi.x + x > -1 and self.taxi.x + x < self.rows:
#                 if self.taxi.y + y > -1 and self.taxi.y + y < self.rows:
#                     if self.lab[self.taxi.x + x][self.taxi.y + y] == 0:
#                         available_moves.append([self.taxi.y+y,self.taxi.x+x])
#         return available_moves


def generate_q_table(columns, rows):
    return np.zeros((columns, rows))

def update_q_table(q_table, state, action, beta, gamma, reward, next_state):
    next_state_max = np.max(q_table[next_state])
    # q_table[state, action] = (1-beta) * q_table[state, action] + beta * (reward + gamma * next_state_max - q_table[state, action])
    q_table[state, action] += beta * (reward + gamma * next_state_max - q_table[state, action])

    return q_table
    

# TESTS:
def main():

    # parameters:
    # epsilon = 0.1
    # gamma = 0.6
    # beta = 0.1      #  learning rate
    
    data = open('taxi_data.txt', 'a')
    # line = "epsilon;gamma;beta;iterations"
    # data.write(line)
    expected_steps = [3, 3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 3, 3, 3, 3, 3]
    for epsilon in [0.15, 0.3]:
        for gamma in [0.4, 0.6, 0.8]:
            for beta in [0.1, 0.3, 0.5]:
                steps = []
                q_table = generate_q_table(64, 4)
                iteration_no = 0
                while steps != expected_steps:
                    taxi = Musk_Taxi(8, 5)
                    steps = []
                    steps, q_table = taxi.drive(q_table, beta, gamma, epsilon)
                    iteration_no += 1
                line = ("\n" + str(epsilon) + ";" + str(gamma) + ";" + str(beta) + ";" + str(iteration_no))
                data.write(line)
    data.close()

    # interval_steps = []
    # for i in range(10000):
    #     steps = []
    #     taxi = Musk_Taxi(8, 5)
    #     steps, q_table = taxi.drive(q_table, beta, gamma, epsilon)
    #     if i % 20 == 0:
    #         interval_steps.append(steps)

    # print(interval_steps[-1])



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