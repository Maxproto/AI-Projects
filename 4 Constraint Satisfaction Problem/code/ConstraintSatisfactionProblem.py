class ConstraintSatisfactionProblem:
    def __init__(self, num_variables, domains, constraints, use_inference, use_mrv, use_lcv):

        self.num_variables = num_variables # variable: [0,1,2,3,...]
        self.domains = {i: list(domains) for i in range(num_variables)} \
            if isinstance(domains, list) else domains.copy()

        '''
        Constraints between variables. This is a dictionary where:
        - The key is a tuple (var1, var2) representing two variables
        - The value is a list of tuples representing allowable values for (var1, var2)
        '''
        self.constraints = constraints
        self.assignment = [-1] * num_variables
        self.use_inference = use_inference
        self.use_mrv = use_mrv
        self.use_lcv = use_lcv
        self.node_count = 0

    def is_valid_assignment(self, variable, value):
        # Tentatively assign 'value' to 'variable'
        self.assignment[variable] = value

        # Iterate through all constraints
        for (var1, var2), valid_values in self.constraints.items():

            # Check if the current constraint involves the 'variable'
            if var1 == variable or var2 == variable:
            
                # If the current assignment of var1 and var2 is not in the allowable pairs 
                # and both variables have been assigned (i.e., not equal to -1)
                # then this is not a valid assignment
                if (self.assignment[var1], self.assignment[var2]) not in valid_values and self.assignment[var1] != -1 and self.assignment[var2] != -1:

                    # Reset the assignment for 'variable' and return False indicating invalid assignment
                    self.assignment[variable] = -1
                    return False
                
        # Reset the assignment for 'variable' and return True indicating valid assignment
        self.assignment[variable] = -1
        return True

    # make the domain of var1 arc-consistent with var2
    def revise(self, var1, var2):
        # If no modification on both the domains of 1 and 2, 'False' will be return
        revised = False
        for x in self.domains[var1]:
            # A value in the domain of var1 doesn't have such a supporting value in var2
            if not any([(x, y) in self.constraints[(var1, var2)] for y in self.domains[var2]]):
                self.domains[var1].remove(x)
                revised = True
        return revised
    
    # Ensure arc consistency for all variables
    def ac3(self, queue=None):
        if not queue:
            queue = list(self.constraints.keys())   # If queue isn't provided, it initializes with all the constraint pairs
        while queue:
            (var1, var2) = queue.pop(0)
            if self.revise(var1, var2):
                '''
                If at any point a domain becomes empty (no values left), it returns False, 
                indicating that the CSP can't be solved with the current assignment
                '''
                if not self.domains[var1]:
                    return False
                '''
                 If the domain of var1 is revised (values are removed),
                 we need to check all other variables that have constraints with var1 to maintain consistency.
                 The following code ensures the direction (order of the variables) matches what's in the constraints dictionary
                '''
                neighbors_forward = [w for v, w in self.constraints.keys() if v == var1]
                neighbors_backward = [v for v, w in self.constraints.keys() if w == var1]
                neighbors = set(neighbors_forward + neighbors_backward) - {var2}  # Exclude var2 from neighbors
                for var in neighbors:
                    if (var1, var) in self.constraints:
                        queue.append((var1, var))
                    else:
                        queue.append((var, var1))
        return True
    
    # MRV (Minimum Remaining Values) heuristic to select the unassigned variable with the smallest domain.
    def select_mrv_variable(self):
        unassigned_variables = [v for v, val in enumerate(self.assignment) if val == -1]
        domain_lengths = [(len(self.domains[var]), var) for var in unassigned_variables]
        _, selected_var = min(domain_lengths, key=lambda x: x[0])
        return selected_var

    # Implementing LCV (Least Constraining Value) heuristic to order the values 
    # in the domain of the given variable based on how constraining they are.
    def order_domain_values(self, variable):

        if not self.use_lcv:
            return self.domains[variable]

        # Internal function to compute the number of restrictions a value imposes on other variables
        def count_restrictions(value):
            count = 0
            
            # For each constraint that involves the current variable
            for var1, var2 in self.constraints.keys():
                if var1 == variable:
                    other_var = var2
                elif var2 == variable:
                    other_var = var1
                else:
                    continue

                # Count the number of values in the other variable's domain that are ruled out by the current value
                incompatible_values_count = 0

                for y in self.domains[other_var]:
                    # Check if the pair (value, y) violates a constraint
                    if (var1 == variable and (value, y) not in self.constraints[(var1, var2)]) or \
                    (var2 == variable and (y, value) not in self.constraints[(var1, var2)]):
                        incompatible_values_count += 1

                count += incompatible_values_count
            
            return count

        # Sort the domain values based on how constraining they are
        return sorted(self.domains[variable], key=lambda x: count_restrictions(x))

    def backtrack(self, variable=None):

        # If all variables have been assigned values, return True
        if all(val != -1 for val in self.assignment):
            return True
        
        # Variable selection based on MRV heuristic
        variable = self.select_mrv_variable() if self.use_mrv else (variable if variable is not None else 0)
        
        # Value ordering based on LCV heuristic
        ordered_domain_values = self.order_domain_values(variable) if self.use_lcv else self.domains[variable]

        for value in ordered_domain_values:
            self.node_count += 1
            if self.is_valid_assignment(variable, value):
                self.assignment[variable] = value

                # Store the original domains for all variables so they can be restored later if needed.
                saved_domains = {var: self.domains[var].copy() for var in self.domains}
                self.domains[variable] = [value]

                # Before diving deeper into the search, we first attempt to prune the domains of the variables 
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

                        # If the recursive call returned True, all subsequent variables have valid assignments
                        # So, return True
                        return True
                    
                # If the recursive call returned False, reset the 'variable' assignment to -1
                # and try the next value from the domain
                self.domains = saved_domains
                self.assignment[variable] = -1

        # If no value from the domain can be assigned to the 'variable', return False
        return False

    def solve(self):
        # Start the backtracking algorithm
        # If a solution is found, return the assignments, otherwise return None
        if self.backtrack():
            print(f"Number of nodes visited: {self.node_count}")
            return self.assignment
        return None
