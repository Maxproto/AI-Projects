import chess


class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board() 
        self.players = [player1, player2]
        print(f'Game Start!\n'
            f'White (Upper Case): {player1}\n'
            f'Black (Lower Case): {player2}')

    def make_move(self):

        player = self.players[1 - int(self.board.turn)] # True indicates it's white's turn and False indicates it's black's turn  
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        move_str = "White to move" if self.board.turn else "Black to move" # board.turn start with true (so the player 1 (white) always go first)

        return board_str + "\n" + 'Round: ' + str(self.board.fullmove_number) + '\n' + move_str + "\n"
