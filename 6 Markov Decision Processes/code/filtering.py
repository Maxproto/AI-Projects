import numpy as np

# Define the maze structure with walls (w) and the color of each cell
# Let's assume that a 'w' can be anywhere in the maze except the edges.
maze_colors = [
    ['r', 'g', 'b', 'y'],
    ['g', 'w', 'y', 'r'],
    ['b', 'y', 'r', 'w'],
    ['y', 'r', 'g', 'b']
]

# Change the sensor readings here
sensor_readings_sequence = ['b', 'r', 'g', 'b', 'y']

# Sensor model probabilities
sensor_accuracy = {
    'r': {'r': 0.88, 'g': 0.04, 'b': 0.04, 'y': 0.04},
    'g': {'r': 0.04, 'g': 0.88, 'b': 0.04, 'y': 0.04},
    'b': {'r': 0.04, 'g': 0.04, 'b': 0.88, 'y': 0.04},
    'y': {'r': 0.04, 'g': 0.04, 'b': 0.04, 'y': 0.88}
}

# Transition model for the robot's movements, considering walls
def transition_model(state, action, maze):
    # Map actions to changes in position
    action_effects = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }
    
    new_state = list(state)
    if action in action_effects:
        dx, dy = action_effects[action]
        new_state[0] += dx
        new_state[1] += dy

        # Check for walls or out-of-bounds and revert to original state if move is not possible
        if (new_state[0] < 0 or new_state[0] >= 4 or
            new_state[1] < 0 or new_state[1] >= 4 or
            maze[new_state[0]][new_state[1]] == 'w'):
            new_state = state
    
    return tuple(new_state)

def filtering(sensor_readings, maze):
    # Calculate the number of non-wall squares dynamically
    non_wall_squares = np.sum(maze != 'w')
    initial_belief = 1 / non_wall_squares if non_wall_squares else 0

    # Initialize belief distribution
    belief = np.full((4, 4), initial_belief)
    belief[maze == 'w'] = 0  # Walls have zero probability

    for reading in sensor_readings:
        # Prediction step (move uniformly in any direction)
        new_belief = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                if maze[i][j] != 'w':  # Ignore walls for prediction
                    for action in ['N', 'S', 'E', 'W']:
                        new_i, new_j = transition_model((i, j), action, maze)
                        new_belief[new_i][new_j] += belief[i][j] * 0.25
        
        # Update step based on sensor reading
        for i in range(4):
            for j in range(4):
                if maze[i][j] != 'w':  # Walls do not get updated
                    color = maze[i][j]
                    new_belief[i][j] *= sensor_accuracy[color][reading]
        
        # Normalize the belief distribution
        total_belief = np.sum(new_belief)
        if total_belief > 0:
            new_belief /= total_belief

        # Print new belief distribution
        print(f"Belief after sensing {reading}:")
        print(new_belief)
        print()

        belief = new_belief


# Function to print the maze
def print_maze(maze):
    print("Maze layout:")
    for row in maze:
        print(' '.join(row))
    print()

# Main function
def main(maze_colors, sensor_readings):
    # Print out the initial maze
    print(f'Sensor readings: {sensor_readings}')

    maze_colors = np.array(maze_colors)
    print_maze(maze_colors)

    # Run filtering based on the sensor readings
    filtering(sensor_readings, maze_colors)

if __name__ == '__main__':
    main(maze_colors, sensor_readings_sequence)
