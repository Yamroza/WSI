import pygame
from field  import Field_w_p

LIGHT_BLUE = (50, 185, 250)
DARK_BLUE = (45, 145, 180)
ORANGE = (255, 180, 35)
GREEN = (45, 200, 35)
BLACK = (0,0,0)
WHITE = (255,255,255)

LINE_WIDTH = 1
WIDTH = HEIGHT = 420
FPS = 3

pygame.init()
pygame.display.list_modes()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isolation")

class Game:
    def __init__(self, win, field):
        self.win = win
        self.field = field
        self.size = HEIGHT/self.field.rows

    def update(self):
        self.win.fill(LIGHT_BLUE)
        for row in range(0, self.field.rows):
            for col in range(row % 2, self.field.rows, 2):
                pygame.draw.rect(self.win, DARK_BLUE, (col * self.size, row * self.size, self.size, self.size))

        for x in range(self.field.rows):
            for y in range(self.field.rows):
                if self.field.sqr_list[x][y][2] == "-":
                    pygame.draw.rect(self.win, BLACK, (y * self.size, x * self.size, self.size, self.size))

        pygame.draw.circle(self.win, BLACK, ((self.field.x1 + 0.5) * self.size , (self.field.y1 + 0.5) * self.size), self.size/2.8)
        pygame.draw.circle(self.win, BLACK, ((self.field.x2 + 0.5) * self.size , (self.field.y2 + 0.5) * self.size), self.size/2.8)

        pygame.draw.circle(self.win, ORANGE, ((self.field.x1 + 0.5) * self.size , (self.field.y1 + 0.5) * self.size), self.size/3)
        pygame.draw.circle(self.win, GREEN, ((self.field.x2 + 0.5) * self.size , (self.field.y2 + 0.5) * self.size), self.size/3)

        self.field.update()

def main():
    global FPS
    run = True
    clock = pygame.time.Clock()
    field = Field_w_p(4, 0, 0, 3, 3, 3)
    game = Game(WIN, field)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        game.update()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
