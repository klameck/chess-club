import board

visited_edges = []
pruned_edges = []

         
def evaluate(node):
    return 1

def alpha_beta(node, depth, maximizing, alpha = - float('inf'), beta =  float('inf')):

    possible_moves = node.get_legal_moves()
    
    if depth == 0 or possible_moves == 0:
        return evaluate(node)

    if maximizing:
        best_value = float("-inf")

        for i, move in enumerate(possible_moves):

            node.push_move(move)

            visited_edges.append((node.to_fen(), str(move)))

            value = alpha_beta(node, depth - 1, False, alpha, beta)
            node.pop_move()
            
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
    
            if alpha >= beta:
                for remaining_move in possible_moves[i + 1:]:
                    pruned_edges.append((node.to_fen(), str(remaining_move)))
                break
        
        return best_value
    
    else:
        best_value = float("inf")

        for i, move in enumerate(possible_moves):
        
            node.push_move(move)

            visited_edges.append((node.to_fen(), str(move)))

            value = alpha_beta(node, depth - 1, True, alpha, beta)
            node.pop_move()
            
            best_value = min(best_value, value)
            beta = min(beta, best_value)
    
            if alpha >= beta:
                for remaining_move in possible_moves[i + 1:]:
                    pruned_edges.append((node.to_fen(), str(remaining_move)))
                break
        
        return best_value

board = board.MagicBitBoard()
print("here")
print(board)

best_value = alpha_beta(board,3,True)

print(best_value)