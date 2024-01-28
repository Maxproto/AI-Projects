import time
import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI, IterativeDeepeningAI
from AlphaBetaAI import AlphaBetaAI
from AlphaBetaAIwithMoveReordering import AlphaBetaAIwithMoveReordering
from AlphaBetaAIwithTranspositionTable import AlphaBetaAIWithTT
from AlphaBetaAIwithZobristTT import AlphaBetaAIWithZobristTT
from ChessGame import ChessGame


player1 = HumanPlayer()
player2 = RandomAI(seed=1)
player3 = MinimaxAI(depth=4)
player4 = IterativeDeepeningAI(depth=4, search_time_limit=5)
player5 = AlphaBetaAI(depth=4)
player6 = AlphaBetaAIwithMoveReordering(depth=4)
player7 = AlphaBetaAIWithTT(depth=4)
player8 = AlphaBetaAIWithZobristTT(depth=4)

start_time = time.time()
game = ChessGame(player3, player2)

while not game.is_game_over():
    print(game)
    game.make_move()

print(game)
print(f"Game end after {game.board.fullmove_number} round")
end_time = time.time()
print(f'Total time used: {end_time - start_time} seconds.')

if game.board.is_checkmate():
        print("Checkmate! ", end="")
        if game.board.turn:  # If it's white's turn, black wins
            print(f"Black ({game.players[1]}) wins!")
        else:
            print(f"White ({game.players[0]}) wins!")

elif game.board.is_stalemate():
    print("Stalemate!")
elif game.board.is_insufficient_material():
    print("Draw due to insufficient material.")
elif game.board.is_seventyfive_moves():
    print("Draw due to 75 moves without capture or pawn move.")
elif game.board.is_fivefold_repetition():
    print("Draw due to fivefold repetition.")
else:
    print("The game continues...")
