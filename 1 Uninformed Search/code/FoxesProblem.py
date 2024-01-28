class FoxProblem:
    def __init__(self, start_state=(3, 3, 1), boat_size=2):
        self.start_state = start_state
        self.boat_size = boat_size
        self.goal_state = (0, 0, 0)
        self.num_chicken = self.start_state[0]
        self.num_fox = self.start_state[1]

    # get successor states for the given state
    def get_successors(self, state):
        successors = []
        for cur_boat_size in range(1, self.boat_size+1):
            for boat_num_chicken in range(cur_boat_size+1):
                if boat_num_chicken == 0 or (boat_num_chicken >= cur_boat_size - boat_num_chicken):
                    action = [boat_num_chicken, cur_boat_size-boat_num_chicken]
                    tmp_state = list(state)
                    if tmp_state[2] == 1:
                        tmp_state[0] -= action[0]
                        tmp_state[1] -= action[1]
                        tmp_state[2] -= 1
                    else:
                        tmp_state[0] += action[0]
                        tmp_state[1] += action[1]
                        tmp_state[2] += 1
                    if (tmp_state[0] >= tmp_state[1] or tmp_state[0] == 0) and \
                        (self.num_chicken - tmp_state[0] >= self.num_fox - tmp_state[1] or self.num_chicken - tmp_state[0] == 0) and \
                            0 <= tmp_state[0] <= self.num_chicken and \
                                0 <= tmp_state[1] <= self.num_fox:
                        successors.append(tuple(tmp_state))

        return successors

    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

if __name__ == "__main__":
    test_cp = FoxesProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
