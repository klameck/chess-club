import board
from eval import evaluate

visited_edges = []
pruned_edges = []
global best_value
best_value = None

def alpha_beta(node, depth, maximizing, alpha = - float('inf'), beta =  float('inf')):
    global best_value
    if best_value == None:
        if maximizing:
            best_value = float("-inf")
        else:
            best_value = float("inf")
    possible_moves = node.get_legal_moves()
    
    if depth == 0 or possible_moves == 0:
        return evaluate(node)

    if maximizing:
        for i, move in enumerate(possible_moves):
            # if move not in visited_edges and move not in pruned_edges [?]
            node.push_move(move)

            visited_edges.append((node.to_fen(), str(move)))

            value = alpha_beta(node, depth - 1, False, alpha, beta)
            node.pop_move()

            #print(f"depth: {depth}, \tmove: {i} \tmaximizing: {maximizing}, \tbest value: {best_value}, \tnew value: {value}, \talpha: {alpha}, \tbeta: {beta}")

            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if value >= beta:
                for remaining_move in possible_moves[i + 1:]:
                    pruned_edges.append((node.to_fen(), str(remaining_move)))
                break
        
        return best_value
    
    else:
        for i, move in enumerate(possible_moves):
        
            node.push_move(move)

            visited_edges.append((node.to_fen(), str(move)))

            value = alpha_beta(node, depth - 1, True, alpha, beta)
            node.pop_move()
            
            best_value = min(best_value, value)
            beta = min(beta, best_value)
    
            if value <= alpha:
                for remaining_move in possible_moves[i + 1:]:
                    pruned_edges.append((node.to_fen(), str(remaining_move)))
                break
        
        return best_value

if __name__ == "__main__":

    board = board.MagicBitBoard("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
    print(board)

    best_value = alpha_beta(board,3,True)

    print(best_value)