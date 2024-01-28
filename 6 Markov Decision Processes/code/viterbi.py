import numpy as np

# Define the maze structure with walls (w) and the color of each cell
# Let's assume that a 'w' can be anywhere in the maze except the edges.
maze_colors = [
    ['r', 'g', 'b', 'y'],
    ['g', 'w', 'y', 'r'],
    ['b', 'y', 'r', 'w'],
    ['y', 'r', 'g', 'b']
]
maze_colors = np.array(maze_colors)

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

def viterbi(sensor_readings, maze):
    rows, cols = maze.shape
    n_states = rows * cols - np.sum(maze == 'w')  # number of valid (non-wall) states

    # Create a mapping from maze (row, col) to state index and back
    state_to_idx = {}
    idx_to_state = {}
    counter = 0
    for i in range(rows):
        for j in range(cols):
            if maze[i, j] != 'w':  # Ignore wall states
                state_to_idx[(i, j)] = counter
                idx_to_state[counter] = (i, j)
                counter += 1

    V = np.zeros((n_states, len(sensor_readings)))  # Viterbi probability matrix
    P = np.zeros((n_states, len(sensor_readings)), dtype=int)  # Path pointer matrix

    # Initialize with the first sensor reading
    for (i, j), idx in state_to_idx.items():
        V[idx, 0] = sensor_accuracy[maze[i, j]][sensor_readings[0]] if maze[i, j] == sensor_readings[0] else 0

    # Recursion step
    for t in range(1, len(sensor_readings)):
        for (i, j), idx in state_to_idx.items():
            if maze[i, j] != 'w':
                max_prob = -1
                max_state = -1
                for action in ['N', 'S', 'E', 'W']:
                    new_i, new_j = transition_model((i, j), action, maze)
                    if maze[new_i, new_j] != 'w':
                        prev_idx = state_to_idx[(new_i, new_j)]
                        prob_transition = 1  # Assuming equal transition probability
                        prob_sensor = sensor_accuracy[maze[i, j]][sensor_readings[t]]
                        prob = V[prev_idx, t-1] * prob_transition * prob_sensor
                        if prob > max_prob:
                            max_prob = prob
                            max_state = prev_idx
                V[idx, t] = max_prob
                P[idx, t] = max_state

    # Termination: Find the state with the highest probability at the last timestep
    last_idx = np.argmax(V[:, -1])
    path = [idx_to_state[last_idx]]

    # Path tracing
    for t in range(len(sensor_readings) - 1, 0, -1):
        last_idx = P[last_idx, t]
        path.insert(0, idx_to_state[last_idx])

    return path, V, state_to_idx


# Function to print the maze
def print_maze(maze):
    print("Maze layout:")
    for row in maze:
        print(' '.join(row))
    print()

def main(maze_colors, sensor_readings):
    # Print out the initial maze
    print(f'Sensor readings: {sensor_readings}')
    print_maze(maze_colors)

    # Find the most likely sequence of states using the Viterbi algorithm
    viterbi_path, V, state_to_idx = viterbi(sensor_readings, maze_colors)

    print("Viterbi probabilities for each state at each time step:")
    for t in range(len(sensor_readings)):
        print(f"Time {t}:")
        for state, idx in state_to_idx.items():
            probability = V[idx, t]
            print(f"    State {state}, Color {maze_colors[state]}, Probability {probability:.4f}")
        print()

    print("Most likely sequence of states with probabilities:")
    for t, state in enumerate(viterbi_path):
        state_idx = state_to_idx[state]
        probability = V[state_idx, t]
        print(f"Time {t}: State {state}, Color {maze_colors[state]}, Probability {probability:.4f}")

if __name__ == '__main__':
    main(maze_colors, sensor_readings_sequence)
