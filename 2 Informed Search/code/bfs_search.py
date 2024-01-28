###############################################################################################
##### This is a simple implementation of BFS search algorithm to solve Sensorless Problem #####
###############################################################################################

from collections import deque
from SearchSolution import SearchSolution

class BeliefNode:
    def __init__(self, state, parent, transition_cost=0):
        self.state = state
        self.parent = parent
        self.transition_cost = transition_cost

def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result

def blind_robot_bfs_search(maze):

    # Find the initial state: all the possible locations in the maze(floor)
    start_state = frozenset((x, y) for x in range(maze.width) for y in range(maze.height) if maze.is_floor(x, y))

    # Use BFS to find the solution (Movement path 
    # that make the blind robot have only 1 belief state)
    start_node = BeliefNode(start_state, None)
    queue = deque([start_node])
    visited_state = set()
    actions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # left, right, up, down
    solution = SearchSolution("BFS Blind robot problem", "BFS with no heuristic")

    while queue:
        curr_node = queue.popleft()

        # If there is one belief state, we know the robot's current location
        if len(curr_node.state) == 1:
            path = backchain(curr_node)
            path = [[coordinate for tup in fs for coordinate in tup] for fs in path]
            solution.cost = curr_node.transition_cost
            solution.path = path
            break
        
        visited_state.add(curr_node.state)
        solution.nodes_visited += 1
        
        # Iterate all the possible action
        for action in actions:
            tmp_state = set()

            # Update all the possible locations
            for x, y in curr_node.state:
                new_x, new_y = x + action[0], y + action[1]

                # Check whether the new location is valid
                if maze.is_floor(new_x, new_y):
                    tmp_state.add((new_x, new_y))
                else:
                    tmp_state.add((x, y))

            tmp_state = frozenset(tmp_state)

            if tuple(tmp_state) not in visited_state:
                new_node = BeliefNode(tmp_state, curr_node, curr_node.transition_cost+1)
                queue.append(new_node)

    return solution