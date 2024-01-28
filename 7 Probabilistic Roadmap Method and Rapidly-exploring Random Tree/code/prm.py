import numpy as np
import time
from scipy.spatial import KDTree
import networkx as nx
from sklearn.neighbors import NearestNeighbors

from arm_simulator import compute_end_points, create_obstacles, check_collision, draw_robot_arm
from utils import angular_distance, draw_path, print_path_steps, draw_roadmap

class PRMPlanner:
    def __init__(self, link_lengths, num_samples, k, obstacles):
        self.link_lengths = link_lengths
        self.num_samples = num_samples
        self.k = k
        self.obstacles = obstacles
        self.graph = nx.Graph()
    
    def sample_configurations(self):
        """
        Randomly samples configurations in the configuration space.
        """
        configs = []
        for _ in range(self.num_samples):
            # Random angles for each joint
            angles = [np.random.uniform(0, 2 * np.pi) for _ in self.link_lengths]
            # Check if the configuration is in collision
            if not check_collision(compute_end_points(self.link_lengths, angles), self.obstacles):
                configs.append(angles)
        return configs
    
    def build_roadmap(self):
        """
        Builds the roadmap as a graph where vertices represent non-colliding configurations
        and edges represent feasible paths between them.
        """
        # Sample configurations
        configs = self.sample_configurations()
        
        # Add configurations as nodes in the graph
        for config in configs:
            self.graph.add_node(tuple(config))
        
        # Create a KDTree for efficient nearest neighbor search
        tree = KDTree(configs)
        
        # Connect each node to its k nearest neighbors
        for config in configs:
            distances, indices = tree.query(config, k=self.k+1)  # +1 because query includes the node itself
            for i, index in enumerate(indices):
                if i > 0:  # Skip the first index because it's the node itself
                    neighbor = configs[index]
                    if not nx.has_path(self.graph, tuple(config), tuple(neighbor)):
                        # Check if path between config and neighbor is collision-free
                        if self.is_collision_free_path(config, neighbor):
                            self.graph.add_edge(tuple(config), tuple(neighbor), weight=distances[i])

    def build_roadmap_ann(self):
        """
        Builds the roadmap using an Approximate Nearest Neighbor (ANN) algorithm.
        """
        # Sample configurations
        configs = self.sample_configurations()

        # Convert configurations to a numpy array for ANN
        config_array = np.array(configs)

        # Use sklearn's NearestNeighbors to find the k nearest neighbors
        nbrs = NearestNeighbors(n_neighbors=min(len(configs), self.k+1), algorithm='auto').fit(config_array)

        # Add configurations as nodes in the graph
        for config in config_array:
            self.graph.add_node(tuple(config))

        # Find k nearest neighbors for each node
        distances, indices = nbrs.kneighbors(config_array)

        # Connect each node to its k nearest neighbors
        for idx, config in enumerate(config_array):
            for neighbor_index in indices[idx][1:]:  # Skip the first index because it's the node itself
                neighbor = config_array[neighbor_index]
                # Check if path between config and neighbor is collision-free
                if self.is_collision_free_path(config, neighbor):
                    # Add an edge if the path is collision-free
                    self.graph.add_edge(tuple(config), tuple(neighbor), weight=distances[idx][np.where(indices[idx] == neighbor_index)][0])

    
    def is_collision_free_path(self, config1, config2):
        """
        Checks if a straight-line path in the configuration space between two configurations is collision-free.

        Args:
        - config1 (list): The starting configuration.
        - config2 (list): The ending configuration.

        Returns:
        - bool: True if the path is collision-free, False otherwise.
        """
        # Interpolate between config1 and config2
        steps = 10
        for i in range(1, steps):
            intermediate_config = [config1[j] + (float(i)/steps)*(config2[j]-config1[j]) for j in range(len(config1))]
            if check_collision(compute_end_points(self.link_lengths, intermediate_config), self.obstacles):
                return False
        return True
    
    def plan_path(self, start_config, goal_config):
        """
        Plans a path from start to goal configuration using the constructed roadmap.

        Args:
        - start_config (list): The starting configuration.
        - goal_config (list): The ending configuration.

        Returns:
        - list: The planned path as a list of configurations.
        """

        # Add the start and goal configurations to the graph if they are collision-free
        if not check_collision(compute_end_points(self.link_lengths, start_config), self.obstacles):
            self.graph.add_node(tuple(start_config))
            # Connect the start configuration to the graph
            for node in self.graph.nodes:
                if self.is_collision_free_path(start_config, node):
                    self.graph.add_edge(tuple(start_config), tuple(node), weight=angular_distance(start_config, node))

        if not check_collision(compute_end_points(self.link_lengths, goal_config), self.obstacles):
            self.graph.add_node(tuple(goal_config))
            # Connect the goal configuration to the graph
            for node in self.graph.nodes:
                if self.is_collision_free_path(goal_config, node):
                    self.graph.add_edge(tuple(goal_config), tuple(node), weight=angular_distance(goal_config, node))

        # Use A* algorithm to find the shortest path in the graph from start to goal
        try:
            path = nx.astar_path(self.graph, tuple(start_config), tuple(goal_config), heuristic=angular_distance)
            return path
        except nx.NetworkXNoPath:
            return None  # Return None if no path is found
        

if __name__ == '__main__':
    np.random.seed(0)

    # Create arm
    link_lengths = [2, 1, 0.5]

    # Create obstacles
    obstacle_type = ['polygon', 'disc', 'polygon']  # Change to 'disc' for circular obstacles
    obstacle_sizes = [0.2, 0.5, 0.2]
    obstacle_positions = [(4, 1), (1.5, 1.5), (4, 4)]
    obstacles = create_obstacles(obstacle_type, obstacle_sizes, obstacle_positions)

    # Create PRM planner instance
    num_samples = 150  # Number of configurations to sample
    k = 100  # Number of nearest neighbors to consider
    prm = PRMPlanner(link_lengths, num_samples, k, obstacles)

    # Build the roadmap
    start_time = time.time()
    prm.build_roadmap()
    end_time = time.time()
    print(f"Times used in building the roadmap: {end_time-start_time}.")

    # Define start and goal configurations
    start_config = [0, 0, 0]
    goal_config = [np.pi/2, np.pi/2, np.pi/2]

    # Plan the path
    path = prm.plan_path(start_config, goal_config)

    # Visualization
    end_points = compute_end_points(link_lengths, start_config)
    draw_robot_arm(end_points, obstacles, check_collision(end_points, obstacles))
    draw_roadmap(prm.graph, link_lengths, obstacles, start_config, goal_config)
    
    if path:
        print("Path found!")
        print_path_steps(path, link_lengths)
        draw_path(path, link_lengths, obstacles)
    else:
        print("No path found.")

