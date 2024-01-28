import chess
import time

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth # sets the depth of the search
        self.minimax_calls = 0  # Track the number of calls to minimax
        self.max_depth_reached = 0  # Track the maximum depth reached
        pass

    def __str__(self):
        string =  f"Minimax AI (search depth: {self.depth})"
        return string
    
    def choose_move(self, board):
        # starts the minimax search at the given depth,
        # we use '_' here to ignore the evaluation score of the move
        _, move = self.minimax(board, self.depth, board.turn) 
        print("Minimax AI recommending move " + str(move))
        print(f"Minimax was called {self.minimax_calls} times")
        print(f"Maximum depth reached was {self.max_depth_reached}")
        return move

    def minimax(self, board, depth, is_max_turn):
        self.minimax_calls += 1
        self.max_depth_reached = max(self.max_depth_reached, self.depth - depth + 1)
        # Cut off test
        # If we've reached the maximum depth or the game is over, we return a static evaluation.
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None
        
        moves = list(board.legal_moves)
        best_move = None

        # Maximizing player's turn (white in this case), we loop over all legal moves,
        # simulate each one, and pick the one with the highest evaluation.
        if is_max_turn:
            max_eval = float('-inf')
            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth-1, not is_max_turn)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        
        # Minimizing player's turn (black), we loop over all legal moves,
        # simulate each one, and pick the one with the lowest evaluation.
        else:
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval, _ = self.minimax(board, depth-1, not is_max_turn)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
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
    

''' 
Iterative Deepening Minimax AI
Start with a shallow depth and progressively increase the depth
'''
class IterativeDeepeningAI(MinimaxAI):
    def __init__(self, depth, search_time_limit):
        super().__init__(depth)
        self.search_time_limit = search_time_limit
        self.best_move = None

    def choose_move(self, board):
        start_time = time.time()

        for depth in range(1, self.depth + 1):
            if time.time() - start_time > self.search_time_limit:  # If elapsed time is more than the limit
                break
            _, move = self.minimax(board, depth, board.turn)
            if move:
                self.best_move = move
                print(f"Depth {depth}: Best move found is {move}")
            else:  # In case there are no legal moves or other stopping criteria
                break


        print("Iterative Deepening AI recommending move " + str(self.best_move))
        print(f"Minimax was called {self.minimax_calls} times")
        print(f"Maximum depth reached was {self.max_depth_reached}")
        return self.best_move