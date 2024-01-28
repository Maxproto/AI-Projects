import os
import time
import numpy as np
import pandas as pd
from prm import PRMPlanner
from arm_simulator import compute_end_points, create_obstacles, draw_robot_arm, check_collision
from utils import draw_path, draw_roadmap, print_path_steps, angular_distance


# Utility function for saving figures
def save_figure(fig, directory, filename):
    fig.savefig(f'{directory}/{filename}.png', dpi=300)

# Define a function to generate random configurations
def generate_random_configs(num_joints, num_samples):
    return [np.random.uniform(0, 2 * np.pi, num_joints) for _ in range(num_samples)]

def generate_obstacles(more_difficult=False):
    obstacle_types = ['polygon', 'disc', 'polygon']
    obstacle_sizes = [0.5, 0.5, 0.5]
    obstacle_positions = [(2, 2), (3, 3), (-4, -4)]

    if more_difficult:
        obstacle_types = ['polygon', 'disc', 'polygon', 'polygon', 'polygon']
        obstacle_sizes = [0.5, 0.5, 0.5, 0.5, 0.5]
        obstacle_positions = [(2, 2), (3, 3), (-4, -4), (-2.5, -2), (3, -2)]

    return create_obstacles(obstacle_types, obstacle_sizes, obstacle_positions)

# Define a function to draw and save robot arms with different configurations
def draw_and_save_arms(link_lengths, filename, collision_check=False):
    angles = generate_random_configs(len(link_lengths), 1)[0]
    end_points = compute_end_points(link_lengths, angles)
    obstacles = generate_obstacles()
    collision = check_collision(end_points, obstacles) if collision_check else False
    fig, ax = draw_robot_arm(end_points, obstacles, collision)
    fig.savefig(f'planar_arms_visualization/{filename}.png', dpi=300)

# Define function to perform motion planning and save the results
def perform_motion_planning(link_lengths, subdir):
    # All starting points are on x-axis
    start_config = np.zeros(len(link_lengths))
    goal_config = np.array([np.pi/2] * len(link_lengths))
    obstacles = generate_obstacles()
    prm = PRMPlanner(link_lengths, num_samples=100, k=10, obstacles=obstacles)
    prm.build_roadmap_ann()
    path = prm.plan_path(start_config, goal_config)

    if path:
        # Save robot arm configuration
        end_points = compute_end_points(link_lengths, start_config)
        fig, ax = draw_robot_arm(end_points, obstacles, False)
        save_figure(fig, f'motion_plan/{subdir}', 'robot_arm')

        # Save roadmap
        fig, ax = draw_roadmap(prm.graph, link_lengths, obstacles, start_config, goal_config)
        save_figure(fig, f'motion_plan/{subdir}', 'roadmap')

        # Save path
        fig, ax = draw_path(path, link_lengths, obstacles)
        save_figure(fig, f'motion_plan/{subdir}', 'path')

        return True
    else:
        return False
    
def compare_roadmap_construction(link_lengths, subdir, k_values):
    start_config = np.zeros(len(link_lengths))
    goal_config = np.array([np.pi/2] * len(link_lengths))
    obstacles = generate_obstacles(more_difficult=True)

    # Initialize dataframe to store comparison results
    comparison_results = pd.DataFrame(columns=['k', 'Method', 'Build Time', 'Path Found'])

    for k in k_values:
        # k-d tree Roadmap
        prm_kdtree = PRMPlanner(link_lengths, num_samples=500, k=k, obstacles=obstacles)
        start_time = time.time()
        prm_kdtree.build_roadmap()
        build_time_kdtree = time.time() - start_time
        path_kdtree = prm_kdtree.plan_path(start_config, goal_config)
        path_found_kdtree = path_kdtree is not None
        new_row_kdtree = pd.DataFrame([{
            'k': k,
            'Method': 'KDtree',
            'Build Time': build_time_kdtree,
            'Path Found': path_found_kdtree,
            'Path Length': len(path_kdtree) if path_found_kdtree else None
        }])
        comparison_results = pd.concat([comparison_results, new_row_kdtree], ignore_index=True)

        # ANN-based Roadmap
        prm_ann = PRMPlanner(link_lengths, num_samples=500, k=k, obstacles=obstacles)
        start_time = time.time()
        prm_ann.build_roadmap_ann()
        build_time_ann = time.time() - start_time
        path_ann = prm_ann.plan_path(start_config, goal_config)
        path_found_ann = path_ann is not None
        new_row_ann = pd.DataFrame([{
            'k': k,
            'Method': 'ANN-based',
            'Build Time': build_time_ann,
            'Path Found': path_found_ann,
            'Path Length': len(path_ann) if path_found_ann else None
        }])
        comparison_results = pd.concat([comparison_results, new_row_ann], ignore_index=True)
        
        # Visualization and saving images if paths are found
        if path_found_kdtree:
            fig, ax = draw_path(path_kdtree, link_lengths, obstacles)
            save_figure(fig, f'comparison/{subdir}', f'path_kdtree_k{k}')
        if path_found_ann:
            fig, ax = draw_path(path_ann, link_lengths, obstacles)
            save_figure(fig, f'comparison/{subdir}', f'path_ann_k{k}')
    
    # Save comparison results to a CSV file and print the DataFrame
    comparison_csv_path = f'comparison/{subdir}/comparison_results.csv'
    comparison_results.to_csv(comparison_csv_path, index=False)
    print(comparison_results)
    
    # Print out a message to indicate where the results have been saved
    print(f"Comparison results saved to {comparison_csv_path}")

if __name__ == '__main__':
    np.random.seed(0)

    # Ensure that the output directories exist
    os.makedirs('planar_arms_visualization', exist_ok=True)
    os.makedirs('motion_plan/2R', exist_ok=True)
    os.makedirs('motion_plan/3R', exist_ok=True)
    os.makedirs('motion_plan/4R', exist_ok=True)
    os.makedirs('comparison/3R', exist_ok=True)

    # Define link lengths for different robot arms
    link_lengths_2R = [2, 2]
    link_lengths_3R = [2, 1, 1]
    link_lengths_4R = [2, 1, 0.5, 0.5]

    # # Part 1: Draw different planar arms with different obstacles
    # draw_and_save_arms(link_lengths_2R, '2R_planar_arm', collision_check=False)
    # draw_and_save_arms(link_lengths_3R, '3R_planar_arm_collision', collision_check=True)
    # draw_and_save_arms(link_lengths_4R, '4R_planar_arm', collision_check=False)

    # # Part 2: Perform motion planning for 2R, 3R, and 4R robot arms
    # perform_motion_planning(link_lengths_2R, '2R')
    # perform_motion_planning(link_lengths_3R, '3R')
    # perform_motion_planning(link_lengths_4R, '4R')

    # Part 3: Run comparison experiments for 3R robot arms with varying k values
    k_values = [5, 10, 15, 50]
    compare_roadmap_construction(link_lengths_3R, '3R', k_values)