from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from itertools import product

class map_coloring_csp(ConstraintSatisfactionProblem):
    def __init__(self, territories, colors, constraints_list, use_inference, use_mrv, use_lcv):

        # A mapping from territory names to integers
        self.territory_to_int = {territory: i for i, territory in enumerate(territories)}

        # A mapping from color names to integers
        self.color_to_int = {color: i for i, color in enumerate(colors)}

        # A mapping from integers back to territory names for solution printing
        self.int_to_territory = {i: territory for territory, i in self.territory_to_int.items()}

        # A mapping from integers back to color names for solution printing
        self.int_to_color = {i: color for color, i in self.color_to_int.items()}
        
        # Convert string-based constraints into integer-based constraints
        int_constraints = self.convert_constraints_to_int(constraints_list)
        
        super().__init__(len(territories), list(self.color_to_int.values()), int_constraints, use_inference, use_mrv, use_lcv)

    def convert_constraints_to_int(self, constraints_list):
        int_constraints = {}
        all_color_combinations = list(product(self.color_to_int.values(), repeat=2))
        
        # Remove combinations where territories would have the same color
        all_color_combinations = [combo for combo in all_color_combinations if combo[0] != combo[1]]
        
        for territory1, territory2 in constraints_list:
            t1_int = self.territory_to_int[territory1]
            t2_int = self.territory_to_int[territory2]
            int_constraints[(t1_int, t2_int)] = all_color_combinations
            
        return int_constraints

    def print_solution(self, solution):
        if solution:
            print("Solution found!")
            for i, color_int in enumerate(solution):
                print(f"{self.int_to_territory[i]} is colored {self.int_to_color[color_int]}")
        else:
            print("No solution found.")


if __name__ == '__main__':
    territories = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    colors = ['red', 'green', 'blue']

    # Constraints between territories that they shouldn't have the same color
    constraints = [('WA', 'NT'), ('WA', 'SA'), ('NT', 'SA'), ('NT', 'Q'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'V'), ('Q', 'NSW'), ('NSW', 'V')]

    map_coloring_csp = map_coloring_csp(territories, colors, constraints, use_inference=True, use_mrv=True, use_lcv=True)
    solution = map_coloring_csp.solve()
    map_coloring_csp.print_solution(solution)