from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from itertools import combinations

class CircuitBoardCSP(ConstraintSatisfactionProblem):
    def __init__(self, board_dim, components, use_inference, use_mrv, use_lcv):

        self.board_width, self.board_height = board_dim
        self.components = components
        self.variables = list(components.keys())
        self.comp_to_int = {comp: idx for idx, comp in enumerate(self.variables)}
        self.domains = self.get_domains()
        self.constraints = self.generate_constraints()

        super().__init__(len(components), self.domains, self.constraints, use_inference, use_mrv, use_lcv)

    def get_domains(self):
        domains = {}
        for comp, (w, h) in self.components.items():
            valid_positions = [(x, y) for x in range(self.board_width - w + 1) 
                                        for y in range(self.board_height - h + 1)]
            domains[self.comp_to_int[comp]] = valid_positions
        return domains
    
    def generate_constraints(self):
        constraints = {}
        # Iterate over each unique pair of components using combinations
        for (comp1, (w1, h1)), (comp2, (w2, h2)) in combinations(self.components.items(), 2):

            legal_positions = []
            for x1, y1 in self.domains[self.comp_to_int[comp1]]:
                for x2, y2 in self.domains[self.comp_to_int[comp2]]:
                    # Conditions for non-overlapping components
                    # If 1 is to the left of 2, then x(1) + w1 <= x(2).
                    # If 1 is to the right of 2, then x(2) + w2 <= x(1).
                    # If 1 is below 2, then y(1) + h1 <= y(2).
                    # If 1 is above 2, then y(2) + h2 <= y(1).
                    if x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1:
                        legal_positions.append(((x1, y1), (x2, y2)))

            constraints[(self.comp_to_int[comp1], self.comp_to_int[comp2])] = legal_positions

        return constraints

    def display_solution(self, assignment):
        board = [['.' for _ in range(self.board_width)] for _ in range(self.board_height)]
        for idx, (x, y) in enumerate(assignment):
            w, h = self.components[self.variables[idx]]
            for i in range(w):
                for j in range(h):
                    board[y + j][x + i] = self.variables[idx][0]

        for row in reversed(board):
            print(''.join(row))


if __name__ == '__main__':
    components = {
        'a': (3, 2),
        'b': (5, 2),
        'c': (2, 3),
        'e': (7, 1)
    }

    board_dim = (10, 3)

    circuit_csp = CircuitBoardCSP(board_dim, components,use_inference=True, use_mrv=True, use_lcv=True)
    solution = circuit_csp.solve()
    if solution:
        print("Solution found!")
        circuit_csp.display_solution(solution)
    else:
        print("No solution found!")
