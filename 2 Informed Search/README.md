## A-star search

*To test the require problem:*
*Run test_mazeworld.py & test_sensorless.py & BONUS_test_simultaneous.py*

*To generate random maze:*
*run random_maze.py*

A* search is an efficient, informed search algorithm. This algorithm effectively searches in areas that seem promising. This judgment is based on an estimation function that calculates the cost to get to the goal from the given state.

In my Python implementation of A*, I use a combination of the actual cost (`g(n)`) from the start node to the current node and a heuristic (`h(n)`) that estimates the cost from the current node to the goal.

```python
class AstarNode:
    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        return self.heuristic + self.transition_cost
```

The main algorithm for A* search:
During this search, we utilize a priority queue, efficiently implemented using a heap. When considering adding a state to the frontier, it is checked if it has been visited at a cheaper cost. If it has not, it is added to the frontier, and the cost is updated

## Multi-robot coordination

### Representation of System State with Robots

##### 1. Representing the state of the system with \( k \) robots:

For each robot, you would need two numbers (its x and y coordinates) to represent its position on a 2D grid. Therefore, for \( k \) robots, the state can be represented as:

state = (turn, x1, y1, x2, y2, ..., xk, yk)

Where `(x1, y1)` are the coordinates of the first robot, `(x2, y2)` are the coordinates of the second robot, and so on. And 'turn' means which robot to take action.

##### 2. Upper bound on the number of states:

Given a grid with \( n \) squares and \( k \) robots, the upper bound on the number of states is given by: k! * (n choose k)

Where `k!` represents the factorial of \( k \) (indicating arrangements of distinct robots) and `(n choose k)` is the combination of placing \( k \) robots in \( n \) squares.

##### 3. Estimate of collision states:

If there are \( w \) wall squares, the number of open squares is \( n-w \). For \( k \) robots: Number of states without collisions = (n-w) * (n-w-1) * ... * (n-w-k+1)

##### 4. Feasibility of a breadth-first search:

For large \( n \) (e.g., 100x100) and several robots (e.g., 10), a straightforward BFS would explore a vast number of states. Given the computational complexity and memory requirements, it's likely infeasible for all start and goal pairs.

##### 5. Monotonic Heuristic Function:

A useful heuristic might be the sum of the Manhattan distances from each robot to its goal. A heuristic is monotonic if, for every node \( n \) and every successor \( n' \) of \( n \), the estimated cost of reaching the goal from \( n \) is no greater than the cost of getting to \( n' \) plus the estimated cost of reaching the goal from \( n' \). The Manhattan distance adheres to this property, making it a suitable choice.

##### 6. Extra test

###### Result of maze with size 15*15

number of nodes visited: 108443

solution length: 111

cost: 54



###### Result of maze with size 20*20

number of nodes visited: 6156725

solution length: 197

cost: 82



###### Result of maze with size 30*30

number of nodes visited: 3309539

solution length: 264

cost: 113

##### 7. The 8-puzzle can be thought of as a special case of the robot problem described earlier. 

###### The key similarities are:

**Grid-based Movement:** Both problems revolve around movement within a grid. The 8-puzzle is a 3x3 grid, and the robot problem can be on an n*×*n grid.

**Limited Movement:** In both cases, movement is constrained. In the 8-puzzle, the empty space can move up, down, left, or right, swapping with the adjacent number. This mirrors the robot's movement on the grid.

**Goal State:** Both problems require reaching a specific arrangement or state. For the 8-puzzle, it's a particular number arrangement. For the robot problem, it's getting all robots to specific goal locations.

Given these similarities, we can view the 8-puzzle as a robot problem where there's only one "robot" (the empty space), and its goal is to navigate numbers to their target positions.

###### Heuristic for the 8-Puzzle:

The Manhattan distance, as mentioned earlier for the robot problem, is also a popular and effective heuristic for the 8-puzzle. For each tile in the 8-puzzle, the Manhattan distance calculates the total number of moves (up, down, left, or right) it would take for that tile to reach its goal position, ignoring all other tiles. The heuristic for a given state would be the sum of the Manhattan distances for all tiles.

This heuristic is admissible (it never overestimates the true cost) and is quite efficient for the 8-puzzle. So, yes, the heuristic function chosen is good for the 8-puzzle.

##### 8. Disjoint Sets in the 8-Puzzle State Space:

The 8-puzzle's state space indeed consists of two disjoint sets. This means that for any given configuration, it either belongs to the "solvable" set or the "unsolvable" set. No sequence of legal moves can change a configuration from one set to the other.

#### Modifying the Program:

To prove the existence of these two disjoint sets, one could modify the program to:

1. **Parity Check:** Compute the parity (even or odd) of the number of inversions in the puzzle. An inversion is when a tile precedes another tile with a lower number on it. If the blank is on an even row counting from the bottom (second or bottom), and the number of inversions is odd, then the puzzle is solvable. Conversely, if the blank is on an odd row (top) and the number of inversions is even, then the puzzle is solvable. All other configurations are unsolvable.
2. **Exploration:** Implement a search that explores all possible configurations stemming from an initial state. If it never reaches the goal state, then the initial configuration is in the unsolvable set.

By integrating the parity check, before even starting the search, one can quickly determine if a given configuration is solvable, saving computational resources.



## Blind robot with Pacman physics

#### Extension: I also implement a BFS search algorithm to solve Sensorless Problem and compare it with the A* algorithm, it shows that A* algorithm could save a lot of time.

## Literature Review 

- Standley, T. 2010. Finding optimal solutions to cooperative pathfinding problems. In The Twenty-Fourth AAAI Conference on Artificial Intelligence (AAAI’10), 173–178.

- This study presents a solution to the cooperative pathfinding issue and introduces two enhancements to the typical A* algorithm, which traditionally generates an exponential number of nodes in its open list.

  The paper proposes an algorithm that segregates agents into subsets. This division ensures that the optimal routes computed for every subset don't overlap with those of others.

  A key innovation is the Simple Independence Detection (SID) algorithm. Initially, SID assumes that all agent paths will be distinct. However, when conflicts arise, it utilizes operator decomposition to cooperatively adjust the overlapping routes.

  The standard method's efficiency declines sharply with the growth of the problem size. On the other hand, operator decomposition demonstrates consistent performance, managing more substantial challenges effectively.
