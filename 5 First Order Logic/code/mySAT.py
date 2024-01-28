import random

class SAT:

    SIZE = 9
    
    def __init__(self, filename):
        self.filename = filename
        self.variables, self.var_index, self.index_val = self._generate_variables()
        self.clauses, self.clauses_val = self._load_clauses()

    def _generate_variables(self):
        """Generate variables for Sudoku grid."""
        variables = []
        var_index = {}
        index_val = [None]
        idx = 1

        for i in range(1, SAT.SIZE + 1):
            for j in range(1, SAT.SIZE + 1):
                for num in range(1, SAT.SIZE + 1):
                    v = f"{i}{j}{num}"
                    variables.append(v)
                    var_index[v] = idx
                    index_val.append(False)
                    idx += 1

        return variables, var_index, index_val

    def _load_clauses(self):
        """Load clauses from file."""
        clauses = []
        clauses_val = []

        with open(self.filename, "r") as f:
            for line in f:
                clause, has_true = [], False

                for s in line.split():
                    idx = self.var_index[s[1:]] if s[0] == '-' else self.var_index[s]
                    clause.append(-idx if s[0] == '-' else idx)
                    has_true |= (self.index_val[idx] if s[0] != '-' else not self.index_val[idx])

                clauses_val.append(has_true)
                clauses.append(clause)

        return clauses, clauses_val

    def write_solution(self, sol_filename):
        """Write the solution to a file."""
        result = [int(v) if self.index_val[self.var_index[v]] else -int(v) for v in self.variables]

        with open(sol_filename, "w") as file:
            for item in result:
                file.write(f"{item}\n")

    def walksat(self):
        var_index_val = [None] + [random.choice([True, False]) for _ in range(1, 730)]
        count = 0

        while not self.check_clauses(var_index_val):
            count += 1
            if count > 100000:
                break

            true_clause, false_clause = self.get_clauses_true(var_index_val)
            print(f'round: {count}, true clause number: {len(true_clause)}')
            
            random_chosen_false_clause = random.choice(false_clause)

            if random.random() > 0.9:
                flip_i = abs(random.choice(random_chosen_false_clause))
            else:
                flip_i = self._get_best_flip(var_index_val, true_clause, random_chosen_false_clause)

            var_index_val[flip_i] = not var_index_val[flip_i]

        self.index_val = var_index_val
        return self.check_clauses(var_index_val)

    def gsat(self):
        var_index_val = [None] + [random.choice([True, False]) for _ in range(1, 730)]

        while not self.check_clauses(var_index_val):
            if random.random() > 0.8:
                flip_i = random.randint(1, 729)
            else:
                flip_i = self._get_best_flip_global(var_index_val)

            var_index_val[flip_i] = not var_index_val[flip_i]
            print(f'True clause number: {self.cal_clauses_true_num(var_index_val)}')

        self.index_val = var_index_val
        return self.check_clauses(var_index_val)

    def _get_best_flip(self, var_index_val, true_clause, random_chosen_false_clause):
        max_true_num, max_true_num_i = 0, []

        for i in random_chosen_false_clause:
            loc_flip_i = abs(i)
            loc_index_val = var_index_val.copy()
            loc_index_val[loc_flip_i] = not loc_index_val[loc_flip_i]
            loc_true_num = self.cal_clauses_true_num(loc_index_val, true_clause)

            if loc_true_num > max_true_num:
                max_true_num, max_true_num_i = loc_true_num, [loc_flip_i]
            elif loc_true_num == max_true_num:
                max_true_num_i.append(loc_flip_i)

        return random.choice(max_true_num_i)

    def _get_best_flip_global(self, var_index_val):
        max_true_num, max_true_num_i = 0, []

        for i in range(1, 730):
            loc_index_val = var_index_val.copy()
            loc_index_val[i] = not loc_index_val[i]
            true_num = self.cal_clauses_true_num(loc_index_val)

            if true_num > max_true_num:
                max_true_num, max_true_num_i = true_num, [i]
            elif true_num == max_true_num:
                max_true_num_i.append(i)

        return random.choice(max_true_num_i)

    def check_clauses(self, var_index_val, clauses=None):
        if clauses is None:
            clauses = self.clauses

        return all(self._is_clause_true(clause, var_index_val) for clause in clauses)

    def _is_clause_true(self, clause, var_index_val):
        return any(v < 0 and not var_index_val[abs(v)] or v > 0 and var_index_val[v] for v in clause)

    def cal_clauses_true_num(self, var_index_val, clauses=None):
        if clauses is None:
            clauses = self.clauses

        return sum(self._is_clause_true(clause, var_index_val) for clause in clauses)

    def get_clauses_true(self, var_index_val):
        true_clause, false_clause = [], []

        for clause in self.clauses:
            (true_clause if self._is_clause_true(clause, var_index_val) else false_clause).append(clause)

        return true_clause, false_clause
