import random
from collections import deque

def is_reachable(maze):
    start = (0, 0)
    visited = set([start])
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == '.' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return len(visited) == sum(row.count('.') for row in maze)

def generate_maze(width, height, wall_count):
    maze = [['.' for _ in range(width)] for _ in range(height)]
    
    walls_added = 0
    while walls_added < wall_count:
        x, y = random.randint(0, height - 1), random.randint(0, width - 1)
        if maze[x][y] == '.':
            maze[x][y] = '#'
            if is_reachable(maze):
                walls_added += 1
            else:
                maze[x][y] = '.'

    robot_positions = []
    for _ in range(3):
        while True:
            x, y = random.randint(0, height-1), random.randint(0, width-1)
            if maze[height-y-1][x] == '.' and (x, y) not in robot_positions:
                robot_positions.append((x, y))
                break

    return maze, robot_positions

def generate_goals(maze, robot_positions, count=3):
    goal_positions = []
    for _ in range(count):
        while True:
            x, y = random.randint(0, len(maze)-1), random.randint(0, len(maze[0])-1)
            if maze[height-y-1][x] == '.' and (x, y) not in robot_positions and (x, y) not in goal_positions:
                goal_positions.append((x, y))
                break
    return goal_positions

def save_to_file(filename, maze, robot_positions, goal_positions):
    with open(filename, 'w') as f:
        for row in reversed(maze):
            f.write("".join(row))
            f.write("\n")
        for x, y in robot_positions:
            f.write(f"\\robot {x} {len(maze) - 1 - y}\n")
        for x, y in goal_positions:
            print(f"\\goal {x} {len(maze) - 1 - y}\n")

if __name__ == "__main__":
    width, height = 60, 60
    wall_count = int(width*height/2)
    maze, robot_positions = generate_maze(width, height, wall_count)
    goal_positions = generate_goals(maze, robot_positions, 3)
    filename = f"maze_{width}x{height}.maz"
    save_to_file(filename, maze, robot_positions, goal_positions)
    print(f"Maze saved to {filename}")