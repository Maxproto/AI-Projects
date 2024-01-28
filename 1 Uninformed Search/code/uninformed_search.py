
from collections import deque
from SearchSolution import SearchSolution

class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def bfs_search(search_problem):
    solution = SearchSolution(search_problem, 'BFS')
    visited_state = set(search_problem.start_state)
    start_node = SearchNode(search_problem.start_state)
    nodes_queue = deque()
    nodes_queue.append(start_node)
    
    while len(nodes_queue) != 0:
        cur_node = nodes_queue.popleft()
        solution.nodes_visited += 1
        if cur_node.state == search_problem.goal_state:
            path = backchaining(cur_node)
            solution.path = path
            break

        else:
            for state in search_problem.get_successors(cur_node.state):
                if not state in visited_state:
                    visited_state.add(state)
                    new_node = SearchNode(state, cur_node)
                    nodes_queue.append(new_node)
                else:
                    continue
    
    return solution

def backchaining(node):
    path = []
    cur_node = node
    path.append(cur_node.state)
    while cur_node.parent:
        cur_node = cur_node.parent
        path.append(cur_node.state)
    return path


def dfs_search(search_problem, depth_limit=100, node=None, solution=None, path=None):
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    
    if path is None:
        path = []
    
    path.append(node.state)
    solution.nodes_visited += 1
    
    if node.state == search_problem.goal_state:
        solution.path = path.copy()
        return solution
    elif len(path) - 1 < depth_limit:
        for state in search_problem.get_successors(node.state):
            if state not in path:
                new_node = SearchNode(state, node)
                result = dfs_search(search_problem, depth_limit, new_node, solution, path)
                if result and result.path:
                    return result
    path.pop()
    return None

def ids_search(search_problem, depth_limit=100):
    solution = None
    for depth in range(depth_limit):
        solution = dfs_search(search_problem, depth)
        if solution and solution.path:
            return solution
    return None
