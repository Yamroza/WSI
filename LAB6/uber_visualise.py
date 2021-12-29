import pygame
from random import randint
from PIL import Image
from q_uber import Musk_Taxi
import os

LIGHT_BLUE = (50, 185, 250)
DARK_BLUE = (45, 145, 180)
ORANGE = (255, 180, 35)
GREEN = (45, 200, 35)
BLACK = (0,0,0)
RED = (255, 0, 0)
GRAY = (80,80,80)

WIDTH = HEIGHT = 840
FPS = 5

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Uber")


class Game:
    def __init__(self, win, taxi):
        self.win = win
        self.taxi = taxi
        self.size = HEIGHT/self.taxi.rows
        self.steps = [3, 3, 3, 0, 3, 3, 0, 3, 3, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 3, 3, 3, 3, 3]
        self.iter = 0
        image = Image.open('LAB6/car.jpg')
        new_image = image.resize((int(self.size), int(self.size)))
        new_image.save('LAB6/car12.jpg')
        self.car_image = pygame.image.load('LAB6/car12.jpg')
        image = Image.open('LAB6/lantern.jpg')
        new_image = image.resize((int(self.size*0.94), int(self.size*0.94)))
        new_image.save('LAB6/lantern12.jpg')
        self.lantern_image = pygame.image.load('LAB6/lantern12.jpg')

    def update(self):
        self.win.fill(BLACK)
        for row in range(0, self.taxi.rows):
            for col in range(0, self.taxi.rows):
                pygame.draw.rect(self.win, LIGHT_BLUE, ((col+0.03) * self.size, (row+0.03) * self.size, self.size*0.94, self.size*0.94))

        for x in range(self.taxi.rows):
            for y in range(self.taxi.rows):
                if self.taxi.lab[x][y] == 1:
                    self.win.blit(self.lantern_image, ((y+0.03) * self.size, (x+0.03) * self.size))

        self.win.blit(self.car_image, (self.taxi.y * self.size, self.taxi.x * self.size))
        pygame.draw.circle(self.win, BLACK, ((self.taxi.y_done + 0.5) * self.size , (self.taxi.x_done + 0.5) * self.size), self.size/2.8)
        pygame.draw.circle(self.win, RED, ((self.taxi.y_done + 0.5) * self.size , (self.taxi.x_done + 0.5) * self.size), self.size/3)

        self.taxi.make_action(self.steps[self.iter])
        if self.iter < len(self.steps) - 1:
            self.iter += 1    


def main():
    global FPS
    run = True
    clock = pygame.time.Clock()
    taxi = Musk_Taxi(8, 10)
    game = Game(WIN, taxi)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        game.update()
        pygame.display.update()
    pygame.quit()
    os.remove('LAB6/car12.jpg')
    os.remove('LAB6/lantern12.jpg')


if __name__ == "__main__":
    main()
