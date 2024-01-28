import chess
from math import inf


class AlphaBetaAI():
    def __init__(self, depth):
        self.depth = depth

    def __str__(self):
        string =  f"Minimax AI with Alpha-Beta Pruning (search depth: {self.depth})"
        return string

    def choose_move(self, board):
        # starts the minimax search at the given depth,
        # we use '_' here to ignore the evaluation score of the move
        _, move = self.minimax(board, self.depth, board.turn, alpha=-float('inf'), beta=float('inf'))
        print("Minimax AI with Alpha-Beta Pruning recommending move " + str(move))
        return move
    
    # Alpha: the minimum value that the maximizing player is assured of. It starts as '-infinity' and can only increase.
    # Beta: the maximum value that the minimizing player is assured of. It starts as 'infinity' and can only decrease.
    def minimax(self, board, depth, is_max_turn, alpha, beta):

        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None
        
        moves = list(board.legal_moves)
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
