from MazeworldProblem import MazeworldProblem
from Maze import Maze

# from uninformed_search import bfs_search
from astar_search import astar_search
# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems
# Single-robot
test_maze2 = Maze("maze2.maz")
test_mp = MazeworldProblem(test_maze2, (3, 1))
result = astar_search(test_mp, null_heuristic)
print(result)

# Multi-robot 
test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# additional tests
print("result of maze with size 10*10")
test_maze3 = Maze("maze_10x10.maz")
test_mp = MazeworldProblem(test_maze3, (1 ,5, 4, 9, 5, 7))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)

print("result of maze with size 15*15")
test_maze3 = Maze("maze_15x15.maz")
test_mp = MazeworldProblem(test_maze3, (12, 7, 5, 14, 6, 1))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)

print("result of maze with size 20*20")
test_maze3 = Maze("maze_20x20.maz")
test_mp = MazeworldProblem(test_maze3, (13, 8, 12, 12, 7, 4))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)

print("result of maze with size 30*30")
test_maze3 = Maze("maze_30x30.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 2, 21, 28, 8))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)

print("result of maze with size 60*60")
test_maze3 = Maze("maze_60x60.maz")
test_mp = MazeworldProblem(test_maze3, (19, 39, 30, 39, 45, 40))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)



