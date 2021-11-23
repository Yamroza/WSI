from minimax import minimax_basic
from copy import deepcopy
import random 


class Field:
    def __init__(self, rows, x1, y1, x2, y2, mode = 1, depth = 2):
        self.rows = rows
        self.x1= x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.mode = mode
        self.depth = depth if depth else 2
        self.is_max = True 
        self.move_to_safe = None
        self.squares_list = []
        for x in range(rows): 
            lista = []
            for y in range(rows):
                lista.append([y, x, 0])
            self.squares_list.append(lista)

        self.winner = False
        self.written = False
        self.squares_list[y1][x1][2] = 'P'
        self.squares_list[y2][x2][2] = 'L'

    def move(self, is_max, x, y):
        if is_max:
            self.squares_list[self.y1][self.x1][2] = '-'
            self.x1 = x
            self.y1 = y
            self.squares_list[self.y1][self.x1][2] = 'P'
        else: 
            self.squares_list[self.y2][self.x2][2] = '-'
            self.x2 = x
            self.y2 = y
            self.squares_list[self.y2][self.x2][2] = 'L'
        self.change_turn()
    

    def change_turn(self):
        self.is_max = True if not self.is_max else False


    def available_moves(self, is_max):
        available_moves = []
        if is_max:
            for y  in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if self.x1 + x > -1 and self.x1 + x < self.rows:
                        if self.y1 + y > -1 and self.y1 + y < self.rows:
                            if not (y == 0 and x == 0):
                                if self.squares_list[self.y1 + y][self.x1 + x][2] == 0:
                                    available_moves.append(self.squares_list[self.y1 + y][self.x1 + x])
        else:
            for y  in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if self.x2 + x > -1 and self.x2 + x < self.rows:
                        if self.y2 + y > -1 and self.y2 + y < self.rows:
                            if not (y == 0 and x == 0):
                                if self.squares_list[self.y2 + y][self.x2 + x][2] == 0:
                                    available_moves.append(self.squares_list[self.y2 + y][self.x2 + x])
        return available_moves

    def children_list(self):
        children_list = []
        for move in self.available_moves(self.is_max):
            child = deepcopy(self)
            child.move_to_safe = move
            child.move(child.is_max, move[0], move[1])
            children_list.append(child)
        return children_list

    def is_winner(self):
        if self.is_max == False:
            if len(self.available_moves(False)) == 0:
                self.winner = True
                return True
            else:
                return False
        else:
            if len(self.available_moves(True)) == 0:
                self.winner = False
                return True
            else:
                return False


    def describe(self):
        for element in self.squares_list:
            print(element) 

    def random_move(self):
        moves = self.available_moves(self.is_max)
        return random.choice(moves)

    def heur_move(self, depth):
        best_move = None
        children = self.children_list()
        if self.is_max:
            best_value = -999  
            for child in children:
                if minimax_basic(child, depth) > best_value:
                    best_value = minimax_basic(child, depth)
                    best_move = child.move_to_safe
        else:
            best_value = 999  
            for child in children:
                if minimax_basic(child, depth) < best_value:
                    best_value = minimax_basic(child, depth)
                    best_move = child.move_to_safe
        return best_move

    def update(self):
        check = self.is_winner()
        if not check:
            if self.mode == 1:
                random_move = self.heur_move(self.depth)
            elif self.mode == 2:
                random_move = self.random_move()
            elif self.mode == 3:
                if self.is_max:
                    random_move = self.heur_move(self.depth)
                else:
                    random_move = self.random_move()
            else:
                if not self.is_max:
                    random_move = self.heur_move(self.depth)
                else:
                    random_move = self.random_move()
            x = random_move[0]
            y = random_move[1]
            self.move(self.is_max, x, y)
            check = self.is_winner()
        else:
            if not self.written:
                print("-----------GAME IS OVER------------")
                string = "GREEN" if self.winner else "ORANGE"
                print("WINNER IS" , string)  
                self.written = True
            else:
                pass
