import pygame
import time
import random

LIGHT_BLUE = (50, 185, 250)
DARK_BLUE = (45, 145, 180)
ORANGE = (255, 180, 35)
GREEN = (45, 200, 35)
BLACK = (0,0,0)
WHITE = (255,255,255)

LINE_WIDTH = 1
WIDTH = HEIGHT = 420
FPS = 5

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isolation")


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
    def __init__(self, win, rows, x1, y1, x2, y2):
        self._win = win
        self.rows = rows
        self.SQUARE_SIZE = HEIGHT/rows
        self._grid = []
        self.pawn_one = Pawn(x1, y1, GREEN)
        self.pawn_two = Pawn(x2, y2, ORANGE)
        self.winner = None
        self.turn = self.pawn_one

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
        self.update_moves_list(self.pawn_one)
        self.update_moves_list(self.pawn_two)

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

    def random_move(self, pawn):
        place = random.choice(pawn.moves())
        self._grid[pawn.y()][pawn.x()].set_lifespan(2)
        pawn.set_x(place.y())
        pawn.set_y(place.x())
        place.set_lifespan(1)

    def heur_move(self, pawn):
        pass

    def endgame(self):
        x, y = WIDTH//2, HEIGHT//2
        stringo = "Pionek zielony wygrał" if self.winner == self.pawn_one else "Pionek pomarańczowy wygrał"
        self.draw_text(x+2, y-2, stringo, WHITE, 40)

    def update(self):

        self.update_moves_list(self.pawn_one)
        self.update_moves_list(self.pawn_two)

        if not self.is_winner():
            if self.turn == self.pawn_one:
                self.random_move(self.pawn_one)
            else:
                self.random_move(self.pawn_two)

            self._win.fill(LIGHT_BLUE)
            for row in range(0, self.rows):
                for col in range(row % 2, self.rows, 2):
                    pygame.draw.rect(self._win, DARK_BLUE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

            for n in range(self.rows):
                for m in range(self.rows):
                    if self._grid[n][m].lifespan() == 2:
                        pygame.draw.rect(self._win, BLACK, (m * self.SQUARE_SIZE, n * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))


            pygame.draw.circle(self._win, self.pawn_one.colour(), ((self.pawn_one.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_one.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)
            pygame.draw.circle(self._win, self.pawn_two.colour(), ((self.pawn_two.x() + 0.5) * self.SQUARE_SIZE , (self.pawn_two.y()+0.5) * self.SQUARE_SIZE), self.SQUARE_SIZE/3)

            # for n in range(self.rows):
            #     for m in range(self.rows):
            #         self.draw_text((m + 0.5) * self.SQUARE_SIZE, (n + 0.5) * self.SQUARE_SIZE, self._grid[n][m].lifespan(), WHITE, 20)

            # if self.turn == self.pawn_one:
            #     for element in self.pawn_one.moves():
            #         print(element.x(), element.y())
            #     print("KONIEC PIERWSZEGO")
            # else:
            #     for element in self.pawn_two.moves():
            #         print(element.x(), element.y())
            #     print("KONIEC DRUGIEGO")

            self.change_turn()

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
    field = Field(WIN, 4,0,0,3,3)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        field.update()
        pygame.display.update()

    pygame.quit()

class Stan:
    def __init__(self, pawns):
        self.pawns = pawns
        self.heur = self.heuristic()

    def heuristic(self):
        return 1


if __name__ == "__main__":
    main()
