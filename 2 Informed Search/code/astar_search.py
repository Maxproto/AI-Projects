from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost
        # you write this part

    def priority(self):
        # you write this part
        return self.heuristic + self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


#  Take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.

def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):

    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)
    close_set = set()
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # While the open set is not empty
    while pqueue:

        # Pop the node with lowest cost
        curr_node = heappop(pqueue)
        # print(f'curr_node.state: {curr_node.state}')

        # Check against the close_set and discard if already processed
        if tuple(curr_node.state) in close_set:
            continue

        solution.nodes_visited += 1
        # Put the state into close set whenever we process a node
        close_set.add(tuple(curr_node.state))

        # Get the current location and check: if the node is the goal, follow its parents back
        if str(search_problem) == "Mazeworld problem: ":
            curr_loc = curr_node.state[1:]
            if curr_loc == list(search_problem.goal_locations):
                solution.cost = curr_node.transition_cost
                solution.path = backchain(curr_node)
                break
        elif str(search_problem) == "Blind robot problem: ":
            curr_loc = curr_node.state[:]
            if curr_node.heuristic == 1:
                solution.cost = curr_node.transition_cost
                solution.path = backchain(curr_node)
                break
        else:
            curr_loc = curr_node.state[:]
            if curr_loc == list(search_problem.goal_locations):
                solution.cost = curr_node.transition_cost
                solution.path = backchain(curr_node)
                break
        
        # Update the current maze
        search_problem.maze.robotloc = curr_loc

        # Iterate all the states after legal movement of current robot
        for state in search_problem.get_successors(curr_node.state):

            # If the state is not in the close set
            if not tuple(state) in close_set:
                
                if str(search_problem) == "Mazeworld problem: ":
                    # Make the cost function the total fuel expended by the robots.
                    if state[1:] == curr_loc:
                        # No fuel(cost) if the robot waits a turn
                        tmp_transition_cost = curr_node.transition_cost
                    else:
                        # Expends one unit of fuel(cost) if the robot moves
                        tmp_transition_cost = curr_node.transition_cost + 1
                else:
                    tmp_transition_cost = curr_node.transition_cost + 1

                # Create a new node
                tmp_node = AstarNode(state, heuristic_fn(state)
                                        , curr_node, tmp_transition_cost)

                # We still push the node onto the pqueue even if a more
                # costly version of that state exists in the queue
                heappush(pqueue, tmp_node)

    return solution






            






    