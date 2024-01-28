import random
from time import sleep

class RandomAI():
    def __init__(self, seed=None):
        self.rand = random.Random(seed)
        
    def __str__(self):
        string =  "Random AI"
        return string 

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = self.rand.choice(moves)
        sleep(1)
        print("Random AI recommending move " + str(move))
        return move

