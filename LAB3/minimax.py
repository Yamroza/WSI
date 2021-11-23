def nowy_minimax(is_max, board, depth):
    board.update_both_moves_list()
    if depth == 0 or board.is_winner():
        return board.ez_heur()
    else:
        scores = []
        board.update_children()
        for child in board.children:
            scores.append(nowy_minimax(not is_max, child, depth-1))
        if is_max:
            return max(scores)
        else:
            return min(scores)