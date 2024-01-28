from Maze import Maze
from time import sleep
import numpy as np
from itertools import product

class MazeworldProblem:

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = self.maze.robotloc

    def __str__(self):
        string =  "Mazeworld problem (Simultaneous): "
        return string

    def animate_path(self, path):
        self.maze.robotloc = tuple(self.start_state[:])
        print(f"self.maze.robotloc: {self.maze.robotloc}")

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[:])
            sleep(1)
            print(str(self.maze))

    def manhattan_heuristic(self, state):
        num_robots = int(len(self.goal_locations) / 2)
        total_cost = 0
        for robot in range(num_robots):
            dis_x = abs(state[robot*2] - self.goal_locations[robot*2])
            dis_y = abs(state[robot*2+1] - self.goal_locations[robot*2+1])
            cost = dis_x + dis_y
            total_cost += cost
        return total_cost

    def get_successors(self, curr_info):

        # Initialize the possible movement of the robot
        actions = np.array([[0, 0], [-1, 0], [1, 0], [0, 1], [0, -1]]) # no movement, left, right, up, down

        # Get the number of robots
        num_robot = int(len(curr_info) / 2)


        robot_loc_list = []
        for robot in range(num_robot):
            curr_robot_loc_list = []
            # Get the current location of the moving robot
            curr_loc = np.array(curr_info[robot*2: robot*2+2])

            # Iterate each possible actions
            for action in actions:

                # Move the robot
                tmp_loc = curr_loc + action

                # Check whether the robot is on the floor or not
                if self.maze.is_floor(tmp_loc[0], tmp_loc[1]):

                    # Add the possible location into the list of current robot
                    curr_robot_loc_list.append([tmp_loc[0], tmp_loc[1]])

            robot_loc_list.append(curr_robot_loc_list)
        

        combinations = list(product(*robot_loc_list))
        valid_combinations = []
        for combination in combinations:
            # Convert each location in the combination to a tuple (to make it hashable)
            # and create a set of the locations.
            unique_locations = set(map(tuple, combination))
            
            # Check if the number of unique locations is the same as the length of the combination
            # (this ensures no location is repeated)
            if len(unique_locations) == len(combination):
                valid_combinations.append(combination)

        # Flatten the valid combinations to get the desired output format
        successors = []
        for combination in valid_combinations:
            flattened_location = []
            for loc in combination:
                for coord in loc:
                    flattened_location.append(coord)
            successors.append(flattened_location)

        return successors
    
# A bit of test code.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_mp.get_successors([1, 0, 1, 2, 2, 1]))
