from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class CS1SectionAssignment(ConstraintSatisfactionProblem):
    '''
    Domains: {student_id: available time}
    Variable: [student_id]
    Constraints: 1. {(leader_id, student_id(leader)): [(time, time),...available time pairs]} 
                 2. section size
    '''

    def __init__(self, filename, use_inference, use_lcv):
        self.domains = self.parse_input_file(filename)

        self.name_to_id = {name: idx for idx, name in enumerate(self.domains)}
        self.id_to_name = {idx: name for name, idx in self.name_to_id.items()}

        self.section_leaders = [self.name_to_id[name] for name in self.domains if name.startswith('*')]
        self.students = [self.name_to_id[name] for name in self.domains if not name.startswith('*')]
        self.section_counts = {leader: 0 for leader in self.section_leaders}

        self.domains = {self.name_to_id[name]: times for name, times in self.domains.items()}

        self.lower_bound = len(self.students) // len(self.section_leaders) - 1
        self.upper_bound = len(self.students) // len(self.section_leaders) + 1
        self.num_variables = len(self.domains)
        self.constraints = self.formulate_constraints()

        super().__init__(self.num_variables, self.domains, self.constraints, use_inference=use_inference, use_mrv=True, use_lcv=use_lcv)

    def parse_input_file(self, filename):
        domains = {}
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                name = parts[0]
                available_times = parts[1:]
                domains[name] = available_times
        return domains

    def is_valid_assignment(self, variable_id, value):
        if not super().is_valid_assignment(variable_id, value):
            return False

        if variable_id in self.students:
            assigned_leader = self.get_leader_for_time(value)
            if not assigned_leader:
                return False

            if self.section_counts[assigned_leader] >= self.upper_bound:
                return False

            # self.section_counts[assigned_leader] += 1
            # remaining_assignments = len(self.students) - sum(self.section_counts.values())
            # under_filled_sections = sum(1 for count in self.section_counts.values() if count < self.lower_bound)
            # needed_students = under_filled_sections * self.lower_bound - sum(count for count in self.section_counts.values() if count < self.lower_bound)
            # self.section_counts[assigned_leader] -= 1

            # if needed_students > remaining_assignments:
            #     return False
        return True

    def select_mrv_variable(self):
        unassigned_variables = [v for v, val in enumerate(self.assignment) if val == -1]
        domain_keys = list(self.domains.keys())
        unassigned_leaders = [var for var in unassigned_variables if domain_keys[var] in self.section_leaders]
        unassigned_students = [var for var in unassigned_variables if domain_keys[var] in self.students]

        if unassigned_leaders:
            leader_domain_lengths = [(len(self.domains[domain_keys[var]]), var) for var in unassigned_leaders]
            _, selected_var = min(leader_domain_lengths, key=lambda x: x[0])
            return selected_var

        if unassigned_students:
            student_domain_lengths = [(len(self.domains[domain_keys[var]]), var) for var in unassigned_students]
            _, selected_var = min(student_domain_lengths, key=lambda x: x[0])
            return selected_var

        raise Exception("No unassigned variable found.")

    def get_leader_for_time(self, time):
        for leader_id in self.section_leaders:
            if self.assignment[leader_id] == time:
                return leader_id
        return None

    def formulate_constraints(self):
        constraints = {}
        for i in range(len(self.section_leaders)):
            for j in range(i+1, len(self.section_leaders)):
                leader1 = self.section_leaders[i]
                leader2 = self.section_leaders[j]
                allowable_pairs = [(t1, t2) for t1 in self.domains[leader1] for t2 in self.domains[leader2] if t1 != t2]
                constraints[(leader1, leader2)] = allowable_pairs

        for student in self.students:
            for leader in self.section_leaders:
                allowable_pairs = [(t, t) for t in self.domains[student] if t in self.domains[leader]]
                constraints[(student, leader)] = allowable_pairs
        return constraints
    
    # Override the backtrack() method
    def backtrack(self, variable=None):

        if all(val != -1 for val in self.assignment):
            return True
        variable = self.select_mrv_variable() if self.use_mrv else (variable if variable is not None else 0)
        ordered_domain_values = self.order_domain_values(variable) if self.use_lcv else self.domains[variable]

        for value in ordered_domain_values:
            if self.is_valid_assignment(variable, value):

                self.assignment[variable] = value
                assigned_leader = self.get_leader_for_time(value)

                if variable in self.students:
                    self.section_counts[assigned_leader] += 1

                saved_domains = {var: self.domains[var].copy() for var in self.domains}
                self.domains[variable] = [value]

                initial_queue = []
                for neighbor in range(self.num_variables):
                    if neighbor != variable:
                        if (neighbor, variable) in self.constraints:
                            initial_queue.append((neighbor, variable))
                        elif (variable, neighbor) in self.constraints:
                            initial_queue.append((variable, neighbor))

                if not self.use_inference or self.ac3(initial_queue):

                    # Recursively try to assign values to the next variables
                    if self.backtrack(variable + 1):

                        # Checking that no section has fewer than n/k - 1 students
                        under_filled_sections = sum(1 for count in self.section_counts.values() if count < self.lower_bound)

                        if under_filled_sections > 0:
                            # Reset this variable's assignment before backtracking since the overall solution isn't valid
                            self.assignment[variable] = -1
                            if variable in self.students:
                                self.section_counts[assigned_leader] -= 1
                            continue  # Proceed with the next value in the domain
                        else:
                            # The entire solution is valid
                            return True
                                        
                # If the recursive call returned False, reset the 'variable' assignment to -1
                # and try the next value from the domain
                self.domains = saved_domains
                self.assignment[variable] = -1
                if variable in self.students:
                    self.section_counts[assigned_leader] -= 1

        # If no value from the domain can be assigned to the 'variable', return False
        return False


def main():
    problem = CS1SectionAssignment("input.txt", use_inference=True, use_lcv=True)
    solution = problem.solve()

    if solution:
        print("Successful assignment!")
        for i, val in enumerate(solution):
            print(f"{problem.id_to_name[i]}: {val}")
    else:
        print("No valid assignment found.")

if __name__ == "__main__":
    main()
