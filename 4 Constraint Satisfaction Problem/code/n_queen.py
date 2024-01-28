def is_safe(board, row, col, n):
    """Check if it's safe to place a queen at board[row][col]."""
    
    # Check the column
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check upper right diagonal
    for i, j in zip(range(row, -1, -1), range(col, n)):
        if board[i][j] == 1:
            return False

    return True


def solve_n_queens(board, row, n):
    """Use backtracking to solve N Queens problem."""
    if row >= n:
        return True

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            if solve_n_queens(board, row + 1, n):
                return True
            board[row][col] = 0  # backtrack

    return False


def print_board(board):
    """Print the board."""
    for row in board:
        print(' '.join('Q' if x else '.' for x in row))
    print("\n")


def n_queens(n):
    """Solve the N Queens problem."""
    board = [[0 for _ in range(n)] for _ in range(n)]
    
    if not solve_n_queens(board, 0, n):
        print("Solution does not exist!")
        return

    print_board(board)


if __name__ == "__main__":
    N = 8
    n_queens(N)
