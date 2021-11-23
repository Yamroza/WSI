from minimax import nowy_minimax
from pawn import Pawn
from square import Square

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

        self._grid = []

        if grid:
            self.set_grid(copy.deepcopy(grid))
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
        self._grid[pawn.y()][pawn.x()].set_lifespan(2)
        pawn.set_x(place.y())
        pawn.set_y(place.x())
        place.set_lifespan(1)

    def random_move(self, pawn):
        place = random.choice(pawn.moves())
        self.move(pawn, place)

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

    def ez_heur(self):
        if self.is_winner():
            # return 1 if self.winner == pawn1 else -1
            return 1 if self.winner == self.pawn_one else -1
        else:
            # return len(pawn1.moves()) - len(pawn2.moves())
            return len(self.pawn_one.moves()) - len(self.pawn_two.moves())

    def new_heur_move(self, pawn, depth):
        self.update_children()
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

            self.new_heur_move(self.turn, 2)
            # self.random_move(self.turn)

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

            self.change_turn()

        else:
            self.endgame()