import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
from arm_simulator import compute_end_points

# Define a function to compute angular distance between two sets of angles
def angular_distance(theta1, theta2):
    """
    Compute the angular distance between two sets of angles, taking into account
    the 2π periodicity and the direction of the shortest path.

    Args:
    - theta1 (list): A list of angles (in radians) for the first configuration.
    - theta2 (list): A list of angles (in radians) for the second configuration.

    Returns:
    - float: The angular distance between the two configurations.
    """
    dist = 0
    for ang1, ang2 in zip(theta1, theta2):
        # Difference in angles, modulo 2π
        diff = np.abs((ang1 - ang2) % (2 * np.pi))
        # Take the shorter distance around the circle
        dist += min(diff, 2 * np.pi - diff)
    return dist


def draw_path(path, link_lengths, obstacles):
    """
    Draws the entire path of the robot arm with the starting, middle, and ending configurations
    in different colors. Adds dotted arrows to indicate the movement of the end effector.
    Makes the robot arm lines thicker for better visibility.

    Args:
    - path (list): The planned path as a list of configurations.
    - link_lengths (list): Lengths of each link in the arm.
    - obstacles (list of Shapely objects): The obstacles in the workspace.
    """
    fig, ax = plt.subplots(figsize=(12, 12))

    # Function to draw a dotted arrow between two points
    def draw_dotted_arrow(start, end):
        # Adjust the start and end to avoid overlap with the arm's endpoint
        arrow_start = np.array(start) + np.sign(np.array(end) - np.array(start)) * 0.03
        arrow_end = np.array(end) - np.sign(np.array(end) - np.array(start)) * 0.03
        arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='->', color='gray',
                                mutation_scale=15, linestyle='dotted', linewidth=1)
        ax.add_patch(arrow)

    # Draw the obstacles
    for obstacle in obstacles:
        x, y = obstacle.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='gray', ec='black')

    # Color settings for start, middle, and end configurations
    colors = ['black', 'blue', 'red']

    # Draw the path
    for idx, config in enumerate(path):
        # Determine the color based on the position in the path
        color = colors[0] if idx == 0 else (colors[2] if idx == len(path) - 1 else colors[1])
        
        end_points = compute_end_points(link_lengths, config)
        x_coords, y_coords = zip(*end_points)

        # Draw the robot arm configuration with thicker lines
        ax.plot(x_coords, y_coords, marker='o', color=color, linewidth=2.5)

        # Draw dotted arrows between end effectors if not the first configuration
        if idx > 0:
            prev_end_effector = compute_end_points(link_lengths, path[idx - 1])[-1]
            curr_end_effector = end_points[-1]
            draw_dotted_arrow(prev_end_effector, curr_end_effector)

    # Set plot title and labels
    plt.title("Robot Arm Path Visualization")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.axis("equal")  # Ensures the scale of x and y axes are the same

    # Show the plot
    plt.show()
    
    return fig, ax

def draw_roadmap(graph, link_lengths, obstacles, start_config, goal_config):
    """
    Draws the roadmap of the PRM planner with nodes and edges, including the obstacles,
    and highlights the start and goal configurations.

    Args:
    - graph (networkx.Graph): The roadmap graph.
    - link_lengths (list): Lengths of each link in the arm.
    - obstacles (list): The obstacles in the workspace.
    - start_config (tuple): Starting configuration of the robot arm.
    - goal_config (tuple): Goal configuration of the robot arm.
    """
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the obstacles
    for obstacle in obstacles:
        x, y = obstacle.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='gray', ec='black')

    # Draw the roadmap nodes
    for node in graph:
        end_points = compute_end_points(link_lengths, node)
        ax.plot(end_points[-1][0], end_points[-1][1], 'o', color='blue')
    
    # Draw the roadmap edges
    for (node1, node2) in graph.edges:
        end_points1 = compute_end_points(link_lengths, node1)
        end_points2 = compute_end_points(link_lengths, node2)
        ax.plot([end_points1[-1][0], end_points2[-1][0]], [end_points1[-1][1], end_points2[-1][1]], 'gray', linestyle='dotted', linewidth=0.5)

    # Highlight the start and goal configurations
    start_end_points = compute_end_points(link_lengths, start_config)
    goal_end_points = compute_end_points(link_lengths, goal_config)
    ax.plot(start_end_points[-1][0], start_end_points[-1][1], 'o', color='green', markersize=10, label='Start')
    ax.plot(goal_end_points[-1][0], goal_end_points[-1][1], 'o', color='red', markersize=10, label='Goal')

    # Set plot title and labels
    plt.title("PRM Roadmap Visualization")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()

    plt.show()

    return fig, ax

def print_path_steps(path, link_lengths):
    """
    Prints out each step in the path with more informative details.

    Args:
    - path (list): The planned path as a list of configurations.
    - link_lengths (list): Lengths of each link in the arm.
    """
    print(f"Path with {len(path)} steps:")
    for step, config in enumerate(path):
        end_points = compute_end_points(link_lengths, config)
        # The end effector position is the last element in the end_points list
        end_effector_pos = end_points[-1]
        print(f"Step {step + 1}/{len(path)}: Configuration = {np.round(config, 2)}, End effector position = {np.round(end_effector_pos, 2)}")