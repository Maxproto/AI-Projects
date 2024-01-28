import random
import chess

class ZobristHash:
    def __init__(self):
        self.zobrist_table = self._init_zobrist_table()

    def _init_zobrist_table(self):
        # For each piece type for each color on each square (64 squares)
        table = {}
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in range(1, 7):  # Pawn, Knight, Bishop, Rook, Queen, King
                for square in chess.SQUARES:
                    # # Assign a random 64-bit number to the current combination of color, piece, and square
                    table[(color, piece_type, square)] = random.getrandbits(64)
        return table
    
    def hash_board(self, board):
        """
        Computes the Zobrist hash of the given board
        By XOR'ing the Zobrist numbers of the pieces on the board.
        """
        # Start with an initial hash value of 0.
        h = 0
        # Iterate over all the squares of the chessboard.
        for square in chess.SQUARES:
            # Get the piece present on the current square.
            piece = board.piece_at(square)
            # If there's a piece on the current square, update the hash.
            if piece:
                # XOR the current hash with the Zobrist number of the piece at the current square.
                h ^= self.zobrist_table[(piece.color, piece.piece_type, square)]
        return h
    
class TranspositionTable:
    def __init__(self):
        self.table = {}
        self.zobrist = ZobristHash()

    def store(self, board, value, best_move):
        board_hash = self.zobrist.hash_board(board)
        self.table[board_hash] = (value, best_move)

    def retrieve(self, board):
        board_hash = self.zobrist.hash_board(board)
        return self.table.get(board_hash, None)
    
class AlphaBetaAIWithZobristTT:
    def __init__(self, depth):
        self.depth = depth
        self.tt = TranspositionTable()

    def __str__(self):
        string =  f"Minimax AI with Alpha-Beta Pruning and Zobrist TT (search depth: {self.depth})"
        return string
    
    def choose_move(self, board):
        # starts the minimax search at the given depth,
        # we use '_' here to ignore the evaluation score of the move
        _, move = self.minimax(board, self.depth, board.turn, alpha=-float('inf'), beta=float('inf'))
        print("Minimax AI with Alpha-Beta Pruning and Zobrist TT recommending move " + str(move))
        return move
    
    def minimax(self, board, depth, is_max_turn, alpha, beta):
        # Check whether the current board state is in Transposition Table
        stored_info = self.tt.retrieve(board)
        if stored_info is not None:
            stored_value, stored_best_move = stored_info
            return stored_value, stored_best_move
        
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

            # Store the board state and evaluation score in Transposition Table before returning
            self.tt.store(board, max_eval, best_move)
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
            self.tt.store(board, min_eval, best_move)
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
