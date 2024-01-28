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
                    v = str(i) + str(j) + str(num)
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
                clause = []
                has_true = False
                for s in line.split():
                    idx = self.var_index[s[1:]] if s[0] == '-' else self.var_index[s]
                    clause.append(-idx if s[0] == '-' else idx)
                    has_true = has_true or (self.index_val[idx] if s[0] != '-' else not self.index_val[idx])
                clauses_val.append(has_true)
                clauses.append(clause)
        return clauses, clauses_val

    def write_solution(self, sol_filename):
        """Write the solution to a file."""
        result = [int(v) if self.index_val[self.var_index[v]] else -int(v) for v in self.variables]
        with open(sol_filename, "w") as file:
            for item in result:
                file.write(str(item) + "\n")

    # ... [rest of your methods remain the same]


    def walksat(self):
        clauses = self.clauses
        var_index_val = [None]
        for _ in range(1, 730):
            var_index_val.append(random.choice([True, False]))
        count = 0
        while not self.check_clauses(var_index_val, clauses):
            count += 1
            if count>100000:
                break
            true_clause, false_clause = self.get_clauses_true(var_index_val, clauses)
            print(f'round: {count}, true clause number: {len(true_clause)}')
            random_chosen_false_clause = random.choice(false_clause)
            if random.random() > 0.9:
                flip_i = abs(random.choice(random_chosen_false_clause))
                var_index_val[flip_i] = not var_index_val[flip_i]
            else:
                max_true_num = 0
                max_true_num_i = []
                for i in random_chosen_false_clause:
                    loc_flip_i = abs(i)
                    loc_index_val = var_index_val[:]
                    loc_index_val[loc_flip_i] = not loc_index_val[loc_flip_i]
                    loc_true_num = self.cal_clauses_true_num(loc_index_val, true_clause)
                    if loc_true_num>max_true_num:
                        max_true_num = loc_true_num
                        max_true_num_i = [loc_flip_i]
                    elif loc_true_num==max_true_num:
                        max_true_num_i.append(loc_flip_i)
                flip_i = random.choice(max_true_num_i)
                var_index_val[flip_i] = not var_index_val[flip_i]

        print(self.check_clauses(var_index_val, clauses))
        self.index_val = var_index_val
        return self.check_clauses(var_index_val, clauses)

    def gsat(self):
        clauses = self.clauses
        var_index_val = [None]
        for _ in range(1, 730):
            var_index_val.append(random.choice([True, False]))
        while not self.check_clauses(var_index_val, clauses):
            if random.random() > 0.8:
                flip_i = random.randint(1, 729)
                var_index_val[flip_i] = not var_index_val[flip_i]
            else:
                max_true_num = 0
                max_true_num_i = []
                for i in range(1, 730):
                    loc_index_val = var_index_val[:]
                    loc_index_val[i] = not loc_index_val[i]
                    true_num = self.cal_clauses_true_num(loc_index_val, clauses)
                    if true_num>max_true_num:
                        max_true_num = true_num
                        max_true_num_i = [i]
                    elif true_num == max_true_num:
                        max_true_num_i.append(i)
                flip_i = random.choice(max_true_num_i)
                var_index_val[flip_i] = not var_index_val[flip_i]
                print(f'True clause number: {max_true_num}')

        print(self.check_clauses(var_index_val, clauses))
        self.index_val = var_index_val
        return self.check_clauses(var_index_val, clauses)

    def check_clauses(self, var_index_val, clauses):
        clauses_val = []
        for index, clause in enumerate(clauses):
            has_true = False
            for v in clause:
                if(v<0 and var_index_val[abs(v)]==False or v>0 and var_index_val[v]==True):
                    has_true = True
            if has_true:
                clauses_val.append(True)
            else:
                clauses_val.append(False)
        return not (False in clauses_val)

    def cal_clauses_true_num(self, var_index_val, clauses):
        true_num = 0
        for clause in clauses:
            has_true = False
            for v in clause:
                if(v<0 and var_index_val[abs(v)]==False or v>0 and var_index_val[v]==True):
                    has_true = True
            if has_true:
                true_num += 1
        return true_num

    def get_clauses_true(self, var_index_val, clauses):
        true_clause = []
        false_clause = []
        for clause in clauses:
            has_true = False
            for v in clause:
                if(v<0 and var_index_val[abs(v)]==False or v>0 and var_index_val[v]==True):
                    has_true = True
            if has_true:
                true_clause.append(clause)
            else:
                false_clause.append(clause)
        return (true_clause, false_clause)