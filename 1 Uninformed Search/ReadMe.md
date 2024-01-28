## Initial discussion and introduction

The state of the system in the foxes and chickens problem is described by the number of chickens, foxes, and the boat on each side of the river. However, a minimal state representation can be used to reduce the complexity of the state. If one fox, one chicken, and one boat are on the starting bank, it is implicit that the others are on the other side of the river (assuming no one has been eaten). So, this state can be described using the tuple (1, 1, 1): one chicken, one fox, and one boat, on the starting side. The initial state, therefore, is (3, 3, 1).

Given this representation, there is an upper bound on the number of states without considering legality. For each side of the river, there can be 0-3 chickens, 0-3 foxes, and 0-1 boats. So, there are 4 * 4 * 2 = 32 possible states for one side of the river. However, since the total number of chickens, foxes, and boats is constant, the state of one side of the river determines the state of the other side. Therefore, the upper bound on the number of states is 32.

<img src="intro.jpg" width="1000"/>


## Breadth-First Search (BFS) Algorithm


The BFS algorithm explores the state space level by level, visiting all neighbors of a state before moving on to the next level. It uses a queue to keep track of states to visit and a set to keep track of visited states. 

### Test Cases
Three test cases were created:
1. **Test Case 1**: Start state is (3, 3, 1), checking if the algorithm can find a solution for an equal number of foxes and chickens.
2. **Test Case 2**: Start state is (5, 5, 1), checking if the algorithm can find a solution when there are more chickens than foxes.
3. **Test Case 3**: Start state is (5, 4, 1), checking if the algorithm can find a solution when there are more foxes than chickens.

### Results
1. **Test Case 1**: The algorithm found a solution with a path length of 16 and visited 31 nodes.
2. **Test Case 2**: no solution found after visiting 14 nodes

3. **Test Case 3**: The algorithm found a solution with a path length of 16 and visited 31 nodes.

## Memoizing depth-first search
DFS already has lower memory usage compared to BFS. However, if we impletement memoizing depth-first search, we are actually saving solutions to subproblems in memory. It would be harmful since the space complexity would become O(d^2), in which we lost the advantages of DFS against BFS. 

## Path-checking depth-first search
### Does path-checking depth-first search save significant memory with respect to breadth-first search?
Yes, because it does not need to store all nodes at the current level before moving on to the next level.
### Draw an example of a graph where path-checking dfs takes much more run-time than breadth-first search
<img src="moretime.jpg" width="300"/>

In this graph, the goal is to find the shortest path from node A to node E. With BFS, the algorithm would first visit all neighbors of A (i.e., B and C), and then visit their neighbors (i.e., D and E). The algorithm would stop when it finds E, having visited a total of 5 nodes. With path-checking DFS, the algorithm would first explore as far as possible along the branch starting with B before backtracking and exploring the branch starting with C. This means it would visit nodes A, B, D, B, A, C, E, for a total of 7 visits. In this example, the path-checking DFS takes more run-time than BFS because it needs to backtrack and revisit nodes.

### On a graph, would it make sense to use path-checking dfs, or would you prefer memoizing dfs in your iterative deepening search? Consider both time and memory aspects. (Hint. If it’s not better than bfs, just use bfs.)
Yes, it generally makes sense to use path-checking DFS on a graph. Path-checking DFS helps to avoid revisiting the same nodes, which is crucial for graphs with cycles to avoid infinite loops.
I will not use Memoizing DFS in IDS because I could hardly find any advantages brought by this usage as discuss in the previous section.
Path-checking DFS involves checking the path from the root to the current node to ensure that we do not visit the same node twice. This helps to avoid cycles and redundant work, which can save time and memory, especially in graphs with many cycles. Memoizing DFS involves storing the results of expensive function calls (in this case, the nodes already visited or the paths already traversed) and returning the cached result when the same inputs occur again. Which increase the space complexity.

### Discussion question: Lossy chickens and foxes

The state for this modified problem would need to include the number of chickens, the number of foxes, the position of the boat (either at the starting side or the goal side), and the number of chickens that have been eaten so far. So, a state could be represented as a tuple (num_chickens, num_foxes, boat_position, num_chickens_eaten).

To implement a solution, I would need to modify the get_successors method to allow states where the number of foxes is greater than the number of chickens, as long as num_chickens_eaten is less than or equal to E. I would also need to modify the method to increment num_chickens_eaten appropriately when transitioning from one state to another.

The upper bound on the number of possible states for this problem would be (C + 1) * (F + 1) * 2 * (E + 1), where C is the total number of chickens, F is the total number of foxes, and E is the maximum number of chickens that can be eaten. The +1 is added to each term because it is possible to have 0 chickens, 0 foxes, and 0 chickens eaten. The * 2 term accounts for the two possible boat positions. This is an upper bound because not all combinations of chickens, foxes, and boat positions will be valid states. For example, if E is 0, then any state where the number of foxes is greater than the number of chickens on either side of the river is invalid.

# Extensions
The impletemented solution considers more cases without the limitation of having at most two animals on the boat. The if condition now checks that the total number of animals on the boat does not exceed cur_boat_size and that the number of chickens on the boat is either 0 or greater than or equal to the number of foxes.
```python
class FoxProblem:
    def __init__(self, start_state=(3, 3, 1), boat_size=2):
        ''''''
    def get_successors(self, state):
        ''''''
        for cur_boat_size in range(1, self.boat_size+1):
            for boat_num_chicken in range(cur_boat_size+1):
                if boat_num_chicken == 0 or (boat_num_chicken >= cur_boat_size - boat_num_chicken):
                    action = [boat_num_chicken, cur_boat_size-boat_num_chicken]
        ''''''

```


