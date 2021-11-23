from pawn import Pawn
from square import Square
from Board import Field


def ez_heur(field):
    if field.is_max:
        return len(field.available_moves(field.is_max)) - len(field.available_moves(not field.is_max))
    else: 
        return len(field.available_moves(not field.is_max)) - len(field.available_moves(field.is_max))

def minimax_basic(field, depth):
    is_max = field.is_max
    if depth == 0:
        return ez_heur(field)
    elif field.is_winner():
        if field.winner:
            return 1
        else:
            return -1
    else:
        scores = []
        for child in field.children():
            scores.append(minimax_basic(child, depth-1))
        if is_max:
            return max(scores)
        else:
            return min(scores)
