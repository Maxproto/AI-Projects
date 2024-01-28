from time import sleep
# Maze file format:
#    # is a wall
#    . is a floor

class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.rows

    def __init__(self, mazefilename):

        self.robotloc = []
        # read the maze file into a list of strings
        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                #print("command")
                # there's only one command, \robot, so assume it is that
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
                self.robotloc.append(x)
                self.robotloc.append(y)
            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)

        self.map = list("".join(lines))


    def index(self, x, y):
        return (self.height - y - 1) * self.width + x


    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.map[self.index(x, y)] == "."


    def has_robot(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        for i in range(0, len(self.robotloc), 2):
            rx = self.robotloc[i]
            ry = self.robotloc[i + 1]
            if rx == x and ry == y:
                return True

        return False


    # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self):
        print(self.robotloc)
        renderlist = list(self.map)

        robot_number = 0
        for index in range(0, len(self.robotloc), 2):

            x = self.robotloc[index]
            y = self.robotloc[index + 1]

            renderlist[self.index(x, y)] = robotchar(robot_number)
            robot_number += 1

        return renderlist


    def __str__(self):

        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s+= renderlist[self.index(x, y)]

            s += "\n"

        return s


def robotchar(robot_number):
    return chr(ord("A") + robot_number)


if __name__ == "__main__":
    test_maze1 = Maze("maze1.maz")
    print(test_maze1)
    print(test_maze1.width)
    print(test_maze1.height)

    #test_maze2 = Maze("maze2.maz")
    #print(test_maze2)

    test_maze3 = Maze("maze3.maz")
    print(test_maze3)

    print(test_maze3)
    print(test_maze3.robotloc)

    print(test_maze3.is_floor(2, 3))
    print(test_maze3.is_floor(-1, 3))
    print(test_maze3.is_floor(1, 0))
    print(test_maze3.is_floor(1, 2))
    print(test_maze3.is_floor(0, 0))
    print(test_maze3.has_robot(1, 0))
