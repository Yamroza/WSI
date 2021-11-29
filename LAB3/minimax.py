def basic_heuristic(field):
    one_moves = field.available_moves(True)
    two_moves = field.available_moves(False)
    if field.is_max:
        return len(one_moves) 
    else: 
        return - len(two_moves)


def differ_heuristic(field):
    one_moves = field.available_moves(True)
    two_moves = field.available_moves(False)

    if field.is_max:
        return len(one_moves) - len(two_moves)
    else: 
        return - (len(two_moves) - len(one_moves))


def off_heuristic(field):
    one_moves = field.available_moves(True)
    two_moves = field.available_moves(False)
    if field.is_max:
        return len(one_moves) - 2 * len(two_moves)
    else: 
        return - (len(two_moves) - 2 * len(one_moves))


def deff_heuristic(field):
    one_moves = field.available_moves(True)
    two_moves = field.available_moves(False)
    if field.is_max:
        return 2 *len(one_moves) - len(two_moves)
    else: 
        return - (2 * len(two_moves) - len(one_moves))


def minimax(field, depth):
    is_max = field.is_max
    ist = field.is_winner()
    if depth == 0:
        return off_heuristic(field)
    elif ist:
        if field.winner:
            return 100
        else:
            return -100
    else:
        scores = []
        for child in field.children_list():
            scores.append(minimax(child, depth-1))
        if is_max:
            return max(scores)
        else:
            return min(scores)
