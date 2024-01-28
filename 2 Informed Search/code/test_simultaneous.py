from simultaneous import MazeworldProblem
from Maze import Maze
from astar_search import astar_search

def null_heuristic(state):
    return 0

test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)