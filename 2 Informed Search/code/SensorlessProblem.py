from Maze import Maze
from time import sleep
import numpy as np

class SensorlessProblem:

    def __init__(self, maze):
        self.maze = maze
        self.start_state = self.__get_start_state()

    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def __get_start_state(self):
        start_state = []
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    start_state.extend([x, y])
        return start_state
        
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))

    def belief_heuristic(self, state):
        return int(len(state)/2)

    def get_successors(self, curr_state):
        successors = []

        # Get the number of possible locations
        num_loc = int(len(curr_state)/2)

        # Initialize the possible movement of the robot
        actions = np.array([[-1, 0], [1, 0], [0, 1], [0, -1]]) # left, right, up, down

        # Iterate each possible actions
        for action in actions:
            
            new_state = []
            
            # Update all possible locations
            for i in range(num_loc):
                loc = np.array(curr_state[i*2: i*2+2])
                tmp_loc = loc + action

                # Check whether the robot is now in a legal position
                if self.maze.is_floor(tmp_loc[0], tmp_loc[1]):
                    new_state.append(tmp_loc[0])
                    new_state.append(tmp_loc[1])
                else:
                    new_state.append(loc[0])
                    new_state.append(loc[1])

            # Group into (x, y) pairs and remove duplicates
            pairs = [(new_state[i], new_state[i+1]) for i in range(0, len(new_state), 2)]
            unique_pairs = list(set(pairs))
            new_state = [item for sublist in unique_pairs for item in sublist]

            successors.append(new_state)
                
        return successors

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
    print(test_problem.get_successors(test_problem.start_state))
