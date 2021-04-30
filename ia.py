import random
import math


def evaluate(board, maximazing_player_number):
    if maximazing_player_number == 1:
        return board.player1_score - board.player2_score
    return board.player2_score - board.player1_score

def minimax(board, depth, maximazing_player, maximazing_player_number):
    if depth == 0:
        return None, evaluate(board, maximazing_player_number)
    
    moves = board.get_moves()
    best_move = random.choice(moves)

    if maximazing_player:
        max_eval = -math.inf
        for move in moves:
            board.selected_sprite = move[0]
            board.move(move[1], move[2], board.game_matriz[move[1]-1][move[2]-1])
            
            temp = board.active_player
            board.active_player = board.waiting_player
            board.waiting_player = temp
            
            current_eval = minimax(board, depth-1, False, maximazing_player_number)[1]

            board.waiting_player = board.active_player
            board.active_player = temp

            board.undo_move()

            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            
        return best_move, max_eval
    else:
        min_eval = math.inf
        for move in moves:
            board.selected_sprite = move[0]
            board.move(move[1], move[2], board.game_matriz[move[1]-1][move[2]-1])

            temp = board.active_player
            board.active_player = board.waiting_player
            board.waiting_player = temp

            current_eval = minimax(board, depth-1, True, maximazing_player_number)[1]

            board.waiting_player = board.active_player
            board.active_player = temp

            board.undo_move()

            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
        return best_move, min_eval
