from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search
from bfs_search import blind_robot_bfs_search

# A* Search
test_maze_blind = Maze("maze_blind.maz")
test_mp_blind = SensorlessProblem(test_maze_blind)
result = astar_search(test_mp_blind, test_mp_blind.belief_heuristic)
print(result)
test_mp_blind.animate_path(result.path)

# Self-Extension: A straight forward (but slower) BFS Search method to solve this problem (not required)
result_bfs = blind_robot_bfs_search(test_maze_blind)
print(result_bfs)

# We could see that a naive BFS search approach need more steps (nodes visited) 
# to get the result than A* search approach