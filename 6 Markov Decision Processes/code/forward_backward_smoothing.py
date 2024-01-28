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
    beliefs = []

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

        beliefs.append(new_belief)
        belief = new_belief

    return beliefs

def backward(sensor_readings, maze):
    # Initialize backward message
    backward_message = np.ones((4, 4))
    backward_messages = [backward_message]

    for reading in reversed(sensor_readings[:-1]):  # No need to compute for first reading
        new_backward_message = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                if maze[i][j] != 'w':
                    for action in ['N', 'S', 'E', 'W']:
                        new_i, new_j = transition_model((i, j), action, maze)
                        prob_transition = 0.25  # Since we assume uniform probability of actions
                        prob_sensor = sensor_accuracy[maze[new_i][new_j]][reading]
                        new_backward_message[i][j] += prob_transition * prob_sensor * backward_message[new_i][new_j]
        
        # Normalize the backward message
        new_backward_message /= np.sum(new_backward_message)
        backward_messages.insert(0, new_backward_message)
        backward_message = new_backward_message

    return backward_messages

def forward_backward(sensor_readings, maze):
    forward_messages = filtering(sensor_readings, maze)
    backward_messages = backward(sensor_readings, maze)

    # Smooth the estimates
    smooth_estimates = []
    for t in range(len(sensor_readings)):
        smooth_estimate = forward_messages[t] * backward_messages[t]
        smooth_estimate /= np.sum(smooth_estimate)
        smooth_estimates.append(smooth_estimate)

    return smooth_estimates

# Function to print the maze
def print_maze(maze):
    print("Maze layout:")
    for row in maze:
        print(' '.join(row))
    print()

# Update the main function to compare filtering and forward-backward smoothing
def main(maze_colors, sensor_readings):
    # Print out the initial maze
    print(f'Sensor readings: {sensor_readings}')
    maze_colors = np.array(maze_colors)
    print_maze(maze_colors)

    # Run filtering and store the forward messages (beliefs)
    beliefs = filtering(sensor_readings, maze_colors)

    # Run forward-backward smoothing based on the sensor readings
    smooth_estimates = forward_backward(sensor_readings, maze_colors)

    # Compare filtering and smoothing estimates
    for t in range(len(sensor_readings)):
        print(f"Filtering distribution at time {t}:")
        print(beliefs[t])
        print()

        print(f"Smoothed distribution at time {t}:")
        print(smooth_estimates[t])
        print()

        # Here we could compute the maximum probability (the confidence) in the belief state for each method
        # to illustrate the smoothing effect
        filtering_confidence = np.max(beliefs[t])
        smoothing_confidence = np.max(smooth_estimates[t])
        print(f"Confidence increase due to smoothing at time {t}: "
              f"{smoothing_confidence - filtering_confidence}")
        print()

if __name__ == '__main__':
    main(maze_colors, sensor_readings_sequence)