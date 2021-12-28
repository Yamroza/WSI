import pygame
from random import randint
from q_uber import Musk_Taxi

LIGHT_BLUE = (50, 185, 250)
DARK_BLUE = (45, 145, 180)
ORANGE = (255, 180, 35)
GREEN = (45, 200, 35)
BLACK = (0,0,0)
RED = (255, 0, 0)

WIDTH = HEIGHT = 420
FPS = 1

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Uber")


class Game:
    def __init__(self, win, taxi):
        self.win = win
        self.taxi = taxi
        self.size = HEIGHT/self.taxi.rows

    def update(self):
        self.win.fill(LIGHT_BLUE)
        for row in range(0, self.taxi.rows):
            for col in range(row % 2, self.taxi.rows, 2):
                pygame.draw.rect(self.win, DARK_BLUE, (col * self.size, row * self.size, self.size, self.size))

        for x in range(self.taxi.rows):
            for y in range(self.taxi.rows):
                if self.taxi.lab[x][y] == 1:
                    pygame.draw.rect(self.win, RED, (y * self.size, x * self.size, self.size, self.size))
                    pygame.draw.rect(self.win, BLACK, ((y + 0.03)* self.size, (x + 0.03) * self.size, self.size * 0.95, self.size * 0.95))


        pygame.draw.circle(self.win, BLACK, ((self.taxi.x + 0.5) * self.size , (self.taxi.y + 0.5) * self.size), self.size/2.8)
        pygame.draw.circle(self.win, GREEN, ((self.taxi.x + 0.5) * self.size , (self.taxi.y + 0.5) * self.size), self.size/3)


def main():
    global FPS
    run = True
    clock = pygame.time.Clock()
    taxi = Musk_Taxi(5, 10)
    game = Game(WIN, taxi)
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
