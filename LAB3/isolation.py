#  s ∈ S to stan i informacja kto wykonuje ruch, , np. ustawienie figur na szachownicy
#  p ∈ P funkcja następnika, reprezentuje ruchy (posunięcia w grze), p : S → S lista lista stanów
# spełniających reguły gry
# • s0 ∈ S to stan początkowy, np. ustawienie początkowe figur na szachownicy
# • T ⊆ S -to zbiór stanów terminalnych, np. mat w szachach
# • w to funkcja wypłaty zdefiniowana dla stanów terminalnych s ∈ T, np.
# w(s) =
# 1 zwycięstwo gracza
# 0 remis
# −1 przegrana

# def Minimax(s,d)          // d - głębokość przeszukiwania
# if s ∈ T or d = 0 then
# return h(s)               // heurystyka lub wypłata
# end
# U := successors(s)
# for u in U do
# w(u) = Minimax(u, d-1 )
# end
# if Max-move then          // ruch gracza Max
# return max(w(u))
# else
# return min(w(u))
# end


import pygame
import time
import random
<<<<<<< HEAD
import copy
from pygame.locals import *
=======
from copy import deepcopy
>>>>>>> 463882ab18fef296802a96f32f2609aba54bba96

LIGHT_BLUE = (50, 185, 250)
DARK_BLUE = (45, 145, 180)
ORANGE = (255, 180, 35)
GREEN = (45, 200, 35)
BLACK = (0,0,0)
WHITE = (255,255,255)

LINE_WIDTH = 1
WIDTH = HEIGHT = 420
<<<<<<< HEAD
FPS = 3
=======
FPS = 4
>>>>>>> 463882ab18fef296802a96f32f2609aba54bba96

pygame.init()
pygame.display.list_modes()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isolation")



# stan gry = [turn, rows, (x1, y1), (x2, y2), dla każdego pola: (x_pola, y_pola, lifespan_pola)]
# dzieciaki stanu gry:
#   - trzeba utworzyć listę ruchów możliwych:
# def dzieciaki(stan_gry):
#       available_moves = []
#         for i in [-1, 0, 1]:
#             for j in [-1, 0, 1]:  
#                 if stan_gry[0] = maxi:
#                    if stan_gry[2][0] + j > -1 and stan_gry[2][1] + i > -1 and stan_gry[2][0] + j < stan_gry[1] and stan_gry[2][1] + i < stan_gry[1]:
#                     try:
#                         if stan_gry[ stan_gry[1] * (stan_gry[2][1] + i) + stan_gry[2][0] + j +3][2] == 0:
#                               available_moves.append(stan_gry[ stan_gry[1] * (stan_gry[2][1] + i) + stan_gry[2][0] + j +3])
#                     except:
#                         pass
#                 else:
#                    if stan_gry[3][0] + j > -1 and stan_gry[3][1] + i > -1 and stan_gry[3][0] + j < stan_gry[1] and stan_gry[3][1] + i < stan_gry[1]:
#                     try:
#                         if stan_gry[ stan_gry[1] * (stan_gry[3][1] + i) + stan_gry[3][0] + j +3][2] == 0:
#                               available_moves.append(stan_gry[ stan_gry[1] * (stan_gry[3][1] + i) + stan_gry[3][0] + j +3])
#                     except:
#                         pass
#  tworzenie dzieciaków:
#       for move in available_moves:
#           move (stan_gry, move) : CZYLI:

#       for move in available_moves:
#       dzieciak = copy.deepcopy(stan_gry)
#       if dzieciak[0] == maxi:
        # dzieciak[2][0] = move[0]                          #         pawn.set_x(place.y())
        # dzieciak[2][1] = move[1]                          #         pawn.set_y(place.x())
        # dzieciak[0] = mini                                #         self.change_turn()
        # dzieciak[(dzieciak[2][1] + move[1]) * dzieciak[1] + dzieciak[2][0] + move[0]][2] = 1 #         place.set_lifespan(1)
        # else:
        # dzieciak[2][0] = move[0]
        # dzieciak[2][1] = move[1]
        # dzieciak[0] = maxi
        # for element in dzieciak:
        #     if element == move:
        #         element[2] = 2                            #         self._grid[pawn.y()][pawn.x()].set_lifespan(2)


def minimax(stan_gry, turn, depth):
    dzieci = dzieciaki(stan_gry)










def nowy_minimax(is_max, board, depth):
    board.update_both_moves_list()
    if depth == 0 or board.is_winner():
        return board.ez_heur()
    else:
        scores = []
        update_children(board)
        for child in board.children:
            scores.append(nowy_minimax(not is_max, child, depth-1))
        if is_max:
            return max(scores)
        else:
            return min(scores)

def update_children(board):
        board.children = []
        for move in board.turn.moves():
            child = deepcopy(board)
            board.move(board.turn, move)
            board.next_move = move
            board.children.append(board)
            board.undo_move()








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


class Field:
    def __init__(self, win, rows, x1, y1, x2, y2, grid = None):
        self._win = win
        self.rows = rows
        self.SQUARE_SIZE = HEIGHT/rows
        self.pawn_one = Pawn(x1, y1, GREEN)
        self.pawn_two = Pawn(x2, y2, ORANGE)
        self.winner = None
        self.turn = self.pawn_one
        self.children = []
        self.next_move = None
        self.last_move = None 

        self._grid = []

        if grid:
            self.set_grid(deepcopy(grid))
        else:
            for n in range(rows):
                self._grid.append([])
                for m in range(rows):
                    self._grid[n].append(Square(n, m))

            self._grid[y1][x1].set_lifespan(1)
            self._grid[y2][x2].set_lifespan(1)

        self._win.fill(LIGHT_BLUE)
        for row in range(0, self.rows):
            for col in range(row % 2, self.rows, 2):
                pygame.draw.rect(self._win, DARK_BLUE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

        pygame.draw.circle(self._win, self.pawn_one.colour(), ((self.pawn_one.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_one.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)
        pygame.draw.circle(self._win, self.pawn_two.colour(), ((self.pawn_two.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_two.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)

        self.update_both_moves_list()

    def state(self):
        status = []
        
        return status


    def set_grid(self, grid):
        self._grid = grid

    def grid(self):
        return self._grid

    def win(self):
        return self._win

    def draw_text(self, x, y, napis, col, size):
        font = pygame.font.SysFont("Impact", size)
        tekst = str(napis)
        text = font.render(tekst, True, col)
        textbox = text.get_rect()
        textbox.center = (x, y)
        self._win.blit(text, textbox)

    def update_moves_list(self, pawn):
        pawn.clear_moves()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if pawn.x() + j > -1 and pawn.y() + i > -1 and pawn.x() + j < self.rows and pawn.y() + i < self.rows:
                    try:
                        if self._grid[pawn.y() + i][pawn.x() + j].lifespan() == 0:
                            pawn.add_move(self._grid[pawn.y() + i][pawn.x() + j])
                    except:
                        pass

    def update_both_moves_list(self):
        self.update_moves_list(self.pawn_one)
        self.update_moves_list(self.pawn_two)

    def change_turn(self):
        self.turn = self.pawn_one if self.turn == self.pawn_two else self.pawn_two

    def is_winner(self):
        flag = False
        if len(self.pawn_one.moves()) == 0:
            self.winner = self.pawn_two
            flag = True
        elif len(self.pawn_two.moves()) == 0:
            self.winner = self.pawn_one
            flag = True
        return flag

    def move(self, pawn, place):
        self.last_move = place
        self._grid[pawn.y()][pawn.x()].set_lifespan(2)
        pawn.set_x(place.y())
        pawn.set_y(place.x())
        place.set_lifespan(1)
<<<<<<< HEAD
=======
        self.change_turn()

    def undo_move(self):
        self.change_turn()
        x = self.turn.x()
        y = self.turn.y()
        self.move(self.turn, self.last_move)
        self._grid[y][x].set_lifespan(0)

>>>>>>> 463882ab18fef296802a96f32f2609aba54bba96

    def random_move(self, pawn):
        place = random.choice(pawn.moves())
        self.move(pawn, place)

<<<<<<< HEAD
    def update_children(self):
        self.children = []
        for move in self.turn.moves():
            # x1 = copy.deepcopy(self.pawn_one.x())
            # y1 = copy.deepcopy(self.pawn_one.y())
            # x2 = copy.deepcopy(self.pawn_two.x())
            # y2 = copy.deepcopy(self.pawn_two.y())
            # child = Field(self._win, self.rows, self.pawn_one.x(), self.pawn_one.y(), self.pawn_two.x(), self.pawn_two.y(), self._grid)
            # child = Field(self._win, self.rows, x1, y1, x2, y2, self._grid)
            child = copy.deepcopy(self)
            # child.turn = copy.deepcopy(self.turn)
            child.move(child.turn, move)
            child.next_move = move
            child.change_turn()
            self.children.append(child)
=======

    # def update_children(self):
    #     self.children = []
    #     for move in self.turn.moves():
    #         self.move(self.turn, move)
    #         self.next_move = move
    #         self.children.append(self)
    #         self.undo_move()


    # def update_children(self):
    #     self.children = []
    #     for move in self.turn.moves():
    #         # x1 = copy.deepcopy(self.pawn_one.x())
    #         # y1 = copy.deepcopy(self.pawn_one.y())
    #         # x2 = copy.deepcopy(self.pawn_two.x())
    #         # y2 = copy.deepcopy(self.pawn_two.y())
    #         child = Field(self._win, self.rows, self.pawn_one.x(), self.pawn_one.y(), self.pawn_two.x(), self.pawn_two.y(), self._grid)
    #         # child = Field(self._win, self.rows, x1, y1, x2, y2, self._grid)
    #         child.turn = copy.deepcopy(self.turn)
    #         child.move(self.turn, move)
    #         child.next_move = move
    #         child.change_turn()
    #         self.children.append(child)
>>>>>>> 463882ab18fef296802a96f32f2609aba54bba96

    def ez_heur(self):
        if self.is_winner():
            # return 1 if self.winner == pawn1 else -1
            return 1 if self.winner == self.pawn_one else -1
        else:
            # return len(pawn1.moves()) - len(pawn2.moves())
            return len(self.pawn_one.moves()) - len(self.pawn_two.moves())

    def new_heur_move(self, pawn, depth):
        # self.update_children()
        update_children(self)
        if pawn == self.pawn_one:
            maxi = True
            best_score = -9999
            for child in self.children:
                if nowy_minimax(maxi, self, depth) > best_score:
                    best_score = nowy_minimax(maxi, self, depth)
                    best_move = child.next_move
        else:
            maxi = False
            best_score = 9999
            for child in self.children:
                if nowy_minimax(maxi, self, depth) < best_score:
                    best_score = nowy_minimax(maxi, self, depth)
                    best_move = child.next_move
        self.move(pawn, best_move)
















    def endgame(self):
        x, y = WIDTH//2, HEIGHT//3
        stringo = "Pionek zielony wygrał" if self.winner == self.pawn_one else "Pionek pomarańczowy wygrał"
        self.draw_text(x+2, y-2, stringo, WHITE, 40)


















    def update(self):

        self.update_both_moves_list()

        if not self.is_winner():

            # self.new_heur_move(self.turn, 2)
            self.random_move(self.turn)

            self._win.fill(LIGHT_BLUE)
            for row in range(0, self.rows):
                for col in range(row % 2, self.rows, 2):
                    pygame.draw.rect(self._win, DARK_BLUE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

            for n in range(self.rows):
                for m in range(self.rows):
                    if self._grid[n][m].lifespan() == 2:
                        pygame.draw.rect(self._win, BLACK, (m * self.SQUARE_SIZE, n * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

            pygame.draw.circle(self._win, BLACK, ((self.pawn_one.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_one.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/2.8)
            pygame.draw.circle(self._win, BLACK, ((self.pawn_two.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_two.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/2.8)

            pygame.draw.circle(self._win, self.pawn_one.colour(), ((self.pawn_one.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_one.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)
            pygame.draw.circle(self._win, self.pawn_two.colour(), ((self.pawn_two.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_two.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)

            for n in range(self.rows):
                for m in range(self.rows):
                    self.draw_text((m + 0.5) * self.SQUARE_SIZE, (n + 0.5) * self.SQUARE_SIZE, self._grid[n][m].lifespan(), WHITE, 20)

            # if self.turn == self.pawn_one:
            #     for element in self.pawn_one.moves():
            #         print(element.x(), element.y())
            #     print("KONIEC PIERWSZEGO")
            # else:
            #     for element in self.pawn_two.moves():
            #         print(element.x(), element.y())
            #     print("KONIEC DRUGIEGO")

        else:
            self.endgame()












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


def main():
    global FPS
    run = True
    clock = pygame.time.Clock()
<<<<<<< HEAD
    field = Field(WIN,4,0,0,3,3)
=======
    field = Field(WIN,5,0,0,4,4)
>>>>>>> 463882ab18fef296802a96f32f2609aba54bba96
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        field.update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


# remis 
