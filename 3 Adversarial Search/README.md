# Assignment 3: Chess AI

*To run the experiments:*
*simply change the player to the AI you want to use in test_chess.py*

### 1. Minimax and cutoff test

* **Minimax (Depth-limited minimax search)**

  Minimax is a depth-first, depth-limited search procedure, and is the prevaling strategy for searching game trees. Minimax searches down to a certain depth, and treats the nodes at that depth as if they were terminal nodes, invoking a heuristic function (called a static evaluation function) to determine their values.
  
  **Minimax search code**

```python
    def minimax(self, board, depth, is_max_turn):
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
```

​	The cutoff test is this part of the code:
```python
	if depth == 0 or board.is_game_over():
​		return self.evaluate_board(board), None​	
```

### 2. Evaluation function

The below evaluation function used in this project primarily gauges the board's state based on material balance and specific game-ending scenarios. Initially, it checks for checkmate, assigning an infinite value favoring the victorious side. It then assesses draw situations such as stalemate, insufficient material, seventy-five-move rule, and fivefold repetition, returning a neutral score of `0` for these. Subsequently, it assigns values to each chess piece (Pawn: 1, Knight/Bishop: 3, Rook: 5, Queen: 9, King: 0) and computes an aggregate score based on the pieces' presence on the board. A positive score indicates white's advantage, negative for black's advantage, and zero suggests a balanced board.

```python
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
```

### 3. Iterative deepening

I created a `IterativeDeepeningAI` class is an enhancement of the `MinimaxAI` class, employing an iterative deepening approach to the minimax algorithm. By incrementally searching deeper into the game tree, it offers flexibility in response time. Upon initialization, it accepts a `depth` and `search_time_limit` as parameters, with the latter specifying the maximum allowed duration for the search. When choosing a move, the algorithm commences its search, incrementing the depth in each iteration. If the search at a particular depth exceeds the time limit or no legal moves remain, it halts. Throughout the process, the best move encountered is continually updated, ensuring that even if the search is prematurely interrupted, the best move found up to that point can still be returned.

```python
class IterativeDeepeningAI(MinimaxAI):  # Inherit from MinimaxAI class
    def __init__(self, depth, search_time_limit):
        super().__init__(depth)  # Use the MinimaxAI's init method
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
        return self.best_move
```

### 4. Alpha-Beta Pruning

**Extending Minimax**

Alpha (the assured minimum value for the maximizing player) and beta (the assured maximum value for the minimizing player) are used to prune branches in the game tree, reducing the number of positions evaluated. If a path being explored is deemed suboptimal compared to already explored paths, the search down that path is cut off early, saving computation time.

```python
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

```

**Move Reordering**

To incorporate a move reordering strategy to enhance search efficiency, we create an initialization method (`__init__`) that sets the search depth and a predefined table (`mvvlva_table`) to rank the value of chess pieces based on the MVV-LVA (Most Valuable Victim - Least Valuable Aggressor) heuristic. The AI also employs a specialized sorting method (`mvvlva_sort`) to prioritize capture moves using the MVV-LVA heuristic. This method also considers the "en passant" rule, a special pawn capture move in chess, ensuring that moves are evaluated correctly and optimizing the search process by examining more promising moves first.

```python
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
```

### 5. Transposition table

To incorporate a Transposition table, we do the followings:

- **Initialization**: Sets up an empty dictionary (`table`) to store board states and their corresponding values.
- **store()**: Saves the evaluation value and the best move for a given board state into the table, using the board's hash as a key.
- **retrieve()**: Fetches the stored evaluation value and best move for a given board state. If the board state isn't in the table, it returns `None`.

```python
class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, board, value, best_move):
        board_hash = hash(str(board))
        self.table[board_hash] = (value, best_move)

    def retrieve(self, board):
        board_hash = hash(str(board))
        return self.table.get(board_hash, None)
```

By using a transposition table, the AI leverages the principle that certain board positions can be reached through different move sequences. By caching these evaluations, the AI can drastically reduce its search time and computational effort in subsequent searches.

### 6. Extensions

**Zobrist Hash Transposition Table**

 Upon initialization, we generates a unique random 64-bit number for every potential combination of piece color, piece type, and board square, storing them in the `zobrist_table`. The `hash_board` method calculates the hash value for a given board state. It starts with an initial hash of 0 and iteratively XORs the hash with the Zobrist number of every piece present on the board. The result is a unique hash representing the current configuration of the chessboard, facilitating rapid board state lookups and comparisons.

```python
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
```

### 7. Results

All the detail experiment result have been saved in the 'txt' files whose names starting with 'RESULT_'. I run all the experiment versus the Random AI(random seed set to 1. All AI has a fix search depth 4.

|           | Minimax | Iterative Deepening | AB Pruning | AB with Move Reordering | AB with Naive TT | AB with Zobrist TT |
| --------- | ------- | ------------------- | ---------- | ----------------------- | ---------------- | ------------------ |
| Result    | Win     | Win                 | Win        | Win                     | Win              | Win                |
| Time(sec) | 640     | 665                 | 39         | 42                      | 34               | 31                 |
| Rounds    | 26      | 26                  | 26         | 29                      | 20               | 20                 |

- **Minimax**: This baseline algorithm won the game in 26 rounds but took a significant 640 seconds to do so.
- **Iterative Deepening**: Built upon Minimax, it also won in 26 rounds, slightly longer at 665 seconds.
- **AB Pruning**: Using the Alpha-Beta pruning optimization, the algorithm won in just 39 seconds over 26 rounds, showcasing a massive time efficiency gain over vanilla Minimax.
- **AB with Move Reordering**: By incorporating move reordering with Alpha-Beta pruning, the algorithm still won but took 42 seconds. Interestingly, the game lasted 29 rounds, slightly longer than its predecessor.
- **AB with Naive TT**: Integrating a naive transposition table with Alpha-Beta pruning, the algorithm secured victory in only 20 rounds and 34 seconds, making it faster in terms of rounds played.
- **AB with Zobrist TT**: Enhancing the transposition table with Zobrist hashing, this method was the fastest, winning in 20 rounds but in a slightly shorter 31 seconds.

Overall, while each algorithm achieved a win, the time efficiency and rounds to victory varied, highlighting the impact of different optimizations on the algorithm's performance.