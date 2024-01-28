import chess
from math import inf

'''
Here we use MVV-LVA (Most Valuable Victim - Least Valuable Aggressor), 
a simple heuristic to generate or sort capture moves in a reasonable order.

'''

class AlphaBetaAIwithMoveReordering():
    def __init__(self, depth):
        self.depth = depth
        self.mvvlva_table = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100
    }

    def __str__(self):
        string =  f"Minimax AI with Alpha-Beta Pruning (Move Reordering) (search depth: {self.depth})"
        return string

    def choose_move(self, board):
        # starts the minimax search at the given depth,
        # we use '_' here to ignore the evaluation score (heuristic) of the move
        _, move = self.minimax(board, self.depth, board.turn, alpha=-float('inf'), beta=float('inf'))
        print("Minimax AI with Alpha-Beta Pruning(Move Reoredering) recommending move " + str(move))
        return move
    
    '''
    Here we consider the en passant capture
    the capture by a pawn of an enemy pawn on the same rank and an adjacent file that 
    has just made an initial two-square advance. The capturing pawn moves to the square 
    that the enemy pawn passed over, as if the enemy pawn had advanced only one square.
    When a pawn performs an en-passant capture, the captured pawn is not on the move.to_square, 
    but on a different square.
    '''
    def mvvlva_sort(self, board, moves):
        def score(move):
            if board.is_capture(move):
                if board.is_en_passant(move):
                    victim_value = self.mvvlva_table[chess.PAWN]
                else:
                    victim_value = self.mvvlva_table[board.piece_at(move.to_square).piece_type]
                aggressor_value = self.mvvlva_table[board.piece_at(move.from_square).piece_type]
                return victim_value - aggressor_value  # MVV-LVA: Larger values will come first
            return 0  # Non-captures are treated equally
        return sorted(moves, key=score, reverse=True)
    
    # Alpha: the minimum value that the maximizing player is assured of. It starts as '-infinity' and can only increase.
    # Beta: the maximum value that the minimizing player is assured of. It starts as 'infinity' and can only decrease.
    def minimax(self, board, depth, is_max_turn, alpha, beta):

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None
        
        moves = self.mvvlva_sort(board, list(board.legal_moves))
        best_move = None

        # A maximizing node
        if is_max_turn: 
            max_eval = float('-inf')
            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth-1, not is_max_turn, alpha, beta)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                # prune the remaining moves for this node because the minimizing player 
                # has a better (lesser) value elsewhere, so they won't choose this path.
                if beta <= alpha: # Beta cut-off
                    break # We end the searching process for maximizing node

            return max_eval, best_move
        
        # A minimizing node
        else:
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth-1, not is_max_turn, alpha, beta)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                # prune the remaining moves for this node because the maxmizing player 
                # has a better (larger) value elsewhere, so they won't choose this path.
                if beta <= alpha: # Alpha cut-off
                    break # We end the searching process for minimizing node
            return min_eval, best_move

    def evaluate_board(self, board):

        if board.is_checkmate():
            if board.turn:
                return -float('inf')  # Black wins
            else:
                return float('inf')   # White wins
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return 0  # Draw

        # setting simple piece values. Pawn: 1, Knight/Bishop: 3, Rook: 5, Queen: 9
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0  # King value is not considered as we evaluate checkmate directly.
        }

        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.WHITE:
                    evaluation += piece_values[piece.piece_type]
                else:
                    evaluation -= piece_values[piece.piece_type]

        return evaluation
