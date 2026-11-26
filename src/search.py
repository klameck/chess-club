import board
from eval import evaluate2


#### Problemo: 
# Ich glaube die Positional tables sind teils falsch. Es kommen mainly negative evals raus, was nicht immer sinn ergibt.


def alpha_beta(node, depth, alpha = - float('inf'), beta =  float('inf')):    
    maximizing = node.side_to_move == "WHITE"
    possible_moves = node.get_legal_moves()
    best_move = None

    #leave node and terminal positions
    if len(possible_moves) == 0:
    
        return 0, None

    if depth == 0:
        return evaluate2(node), None

    if maximizing:
        best_value = float("-inf")

        for move in possible_moves:
            
            node.push_move(move)
            value, _ = alpha_beta(node, depth - 1, alpha, beta)
            node.pop_move()

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)

            if value >= beta:
                break
        
        return best_value, best_move
    
    else:
        best_value = float("inf")
        for move in possible_moves:
        
            node.push_move(move)
            value, _ = alpha_beta(node, depth - 1, alpha, beta)
            node.pop_move()
            
            if value < best_value:
                best_value = value
                best_move = move

            beta = min(beta, best_value)
    
            if value <= alpha:
                break
        
        return best_value, best_move

if __name__ == "__main__":

    board = board.MagicBitBoard()#"r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
    board.print_board()

    score, move = alpha_beta(board, 3)
    print(score, move)

