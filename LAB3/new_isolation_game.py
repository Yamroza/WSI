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
import copy
from pygame.locals import *
from minimax import nowy_minimax
from pawn import Pawn
from square import Square
from Board import Field

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


def main():
    global FPS
    run = True
    clock = pygame.time.Clock()
    field = Field(WIN,4,0,0,3,3)
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
