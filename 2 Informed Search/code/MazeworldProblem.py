from Maze import Maze
from time import sleep
import numpy as np

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = [0] + self.maze.robotloc # The first number represent the current moving robot

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])
        print(f"self.maze.robotloc: {self.maze.robotloc}")

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)
            print(str(self.maze))

    def manhattan_heuristic(self, state):
        num_robots = int(len(self.goal_locations) / 2)
        total_cost = 0
        for robot in range(num_robots):
            dis_x = abs(state[robot*2+1] - self.goal_locations[robot*2])
            dis_y = abs(state[robot*2+2] - self.goal_locations[robot*2+1])
            cost = dis_x + dis_y
            total_cost += cost
        return total_cost

    def get_successors(self, curr_info):
        # Initialize the successors list
        successors = []

        # Initialize the possible movement of the robot
        actions = np.array([[0, 0], [-1, 0], [1, 0], [0, 1], [0, -1]]) # no movement, left, right, up, down

        # Get the index of moving robot and number of robots
        robot = curr_info[0]
        num_robot = int((len(curr_info) - 1) / 2)

        # Get the current location of the moving robot
        curr_loc = np.array(curr_info[robot*2+1: robot*2+3])

        # Iterate each possible actions
        for action in actions:

            # Move the robot
            tmp_loc = curr_loc + action

            # Check whether the robot is now in a legal position
            if self.maze.is_floor(tmp_loc[0], tmp_loc[1]) and (not self.maze.has_robot(tmp_loc[0], tmp_loc[1]) or list(action) == [0, 0]):

                # Update the moving robot location in the state list
                tmp_info = curr_info[:]
                tmp_info[robot*2+1] = tmp_loc[0]
                tmp_info[robot*2+2] = tmp_loc[1]

                # Change the moving robot to the next robot
                tmp_info[0] = (tmp_info[0] + 1) % num_robot
                # Update the successors list
                successors.append(tmp_info)

        return successors
    

# A bit of test code.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_mp.get_successors([0, 1, 0, 1, 2, 2, 1]))
