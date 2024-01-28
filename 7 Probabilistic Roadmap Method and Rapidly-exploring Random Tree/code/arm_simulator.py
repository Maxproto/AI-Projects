import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString

def compute_end_points(link_lengths, angles):
    """
    Computes the end points of each link in a planar robot arm.
    
    Args:
    - link_lengths (list): A list of lengths for each link in the robot arm.
    - angles (list): A list of angles (in radians) for each joint in the robot arm.

    Returns:
    - List of tuples: Each tuple represents the (x, y) coordinates of the end point of each link.
    """

    # Initialize the starting point of the arm.
    x, y = 0, 0

    # List to store the end points of each link.
    end_points = [(x, y)]

    # Accumulate the angle as we move through each joint.
    total_angle = 0

    for length, angle in zip(link_lengths, angles):
        total_angle += angle
        x += length * np.cos(total_angle)
        y += length * np.sin(total_angle)
        end_points.append((x, y))

    return end_points

def create_obstacles(obstacle_types, obstacle_sizes, obstacle_positions):
    """
    Creates a list of obstacles represented as Shapely objects.

    Args:
    - obstacle_types (list): A list of type of obstacle ('disc' or 'polygon').
    - obstacle_sizes (list): A list of sizes for each obstacle.
    - obstacle_positions (list): A list of positions where each obstacle is located.

    Returns:
    - List of Shapely objects representing the obstacles.
    """

    obstacles = []
    for obstacle_type, size, position in zip(obstacle_types, obstacle_sizes, obstacle_positions):
        if obstacle_type == 'disc':
            obstacles.append(Point(position).buffer(size))  # Creates a circle (disc) as an obstacle
        elif obstacle_type == 'polygon':
            # Creates a square polygon as an obstacle centered at position
            obstacles.append(Polygon([(position[0] - size, position[1] - size),
                                      (position[0] - size, position[1] + size),
                                      (position[0] + size, position[1] + size),
                                      (position[0] + size, position[1] - size)]))
    return obstacles

def check_collision(link_end_points, obstacles):
    """
    Checks if there is a collision between the robot arm and any of the obstacles.

    Args:
    - link_end_points (list of tuples): The end points of each link in the robot arm.
    - obstacles (list of Shapely objects): The obstacles in the workspace.

    Returns:
    - bool: True if there is a collision, False otherwise.
    """
    
    # Create line segments for each link in the robot arm
    arm_segments = [LineString([link_end_points[i], link_end_points[i+1]]) for i in range(len(link_end_points) - 1)]

    for segment in arm_segments:
        for obstacle in obstacles:
            if segment.intersects(obstacle):
                return True  # Collision detected

    return False  # No collision detected

def draw_robot_arm(end_points, obstacles=None, collision=False):
    """
    Draws the robot arm with the obstacles and indicates collisions.
    The base of the arm will be at location (0, 0).

    Args:
    - end_points (list of tuples): The end points of each link in the robot arm.
    - obstacles (list of Shapely objects): The obstacles in the workspace.
    - collision (bool): True if there is a collision, False otherwise.
    """
    
    # Unzip the end points into separate x and y coordinate lists.
    x_coords, y_coords = zip(*end_points)

    # Initialize plot
    fig, ax = plt.subplots(figsize=(8, 8))

    if collision:
        fig.patch.set_facecolor('#ffcccb')

    # Draw the robot arm
    ax.plot(x_coords, y_coords, marker='o', color='red' if collision else 'black')

    # Draw the obstacles
    if obstacles:
        for obstacle in obstacles:
            x, y = obstacle.exterior.xy
            ax.fill(x, y, alpha=0.5, fc='gray')

    plt.title("Robot Arm Configuration" + (" with Obstacles" if obstacles else "") + (" - Collision Detected" if collision else ""))
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.axis("equal")

    # Show the plot
    plt.show()

    return fig, ax

if __name__ == '__main__':
    link_lengths = [2, 2, 1]
    angles = [0, np.pi/4, np.pi/4] 

    obstacle_type = ['polygon', 'disc']
    obstacle_sizes = [1, 0.3]
    obstacle_positions = [(3, 2), (0.5, 0.5)]
    
    # Compute the end points of the arm for the given configuration
    end_points = compute_end_points(link_lengths, angles)

    # Draw the robot arm
    draw_robot_arm(end_points)

    # Create obstacles
    obstacles = create_obstacles(obstacle_type, obstacle_sizes, obstacle_positions)

    # Check for collision
    collision = check_collision(end_points, obstacles)

    # Draw the robot arm and indicate collisions
    draw_robot_arm(end_points, obstacles, collision)
