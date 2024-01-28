from display import display_sudoku_solution
import random, sys
from mySAT import SAT


if __name__ == "__main__":
    random.seed()

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    result = sat.walksat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)   