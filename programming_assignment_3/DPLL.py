"""
After reading in your KB, call function DPLL(clauses, model), with model initially set to the empty truth assignment 
over all propositional symbols appearing in the KB.

A model can be represented by a hash table that maps propositions (strings) to truth values (1=True,-1=False,0=unknown)
You may also include extra literals (strings) in the command line, which should be appended to the KB (as unit clauses)

When the program first starts, print out the command line (to save the output file). Whenever assign a variable in the model, print out tracing information.

DPLL (in the slides):
Search for complete truth assignment (like CSP)
KB = {}
Props are = {variables name}
initial state = {?,?,?}
goal states = {F,F,T,T,T}

PROCEDURES: convert propositional KB into CNF,start with an empty truth assignment, 
try binding one more variable at a time, back-track whenever a clause is violated, 
quit when a complete assignments is found that satisfies all claues.

unit-clause heurisitc - given a partial assignment, if there is a clause where all but 1 literal is False and the last is ?, then add the 
approriate truth value to the model


"""

class DPLL_solver:

    clauses = []
    models = {}
    result_model = {}
    model_size = 0
    facts = []
    call_count =0
    def parser(self, filename, fact=[]):
        with open(filename, 'r') as file:
            for line in file:
                line_split = line.split()
                line_parser = []
                for item in line_split:
                    if item == "#":
                        break
                    else:
                        line_parser.append(item)
                        temp = item
                        if temp[0]=='-':
                            temp = temp[1:]
                        if temp not in self.models:
                            self.models[temp] = 0
                if len(line_parser) > 1:
                    self.clauses.append(line_parser)
                # elif len(line_parser) == 1:
                #     self.facts.append(line_parser)
                #     if line_parser[0][0]=='-':
                #         line_parser[0]=line_parser[0][1:]
                #         self.models[line_parser[0]] = -1
                #     else:
                #         self.models[line_parser[0]] = 1
        for fact in facts:
            if fact[0]=='-':
                fact=fact[1:]
                self.models[fact] = -1
            else:
                self.models[fact] = 1
        print(self.clauses)
        print()
        print(self.models)
        self.model_size = len(self.models)
        print(self.model_size)
        return 


    def check_clause(self, clause, model):
        overall_result = -1
        unknow = 0
        first_unknown_value = ''
        unknown_list = []
        for i in range(len(clause)):
            temp = clause[i]
            if temp[0]=='-':
                # Negative clause
                temp=temp[1:]
                if model[temp] == 0:
                    if unknow==0:
                        first_unknown_value = temp
                    unknow += 1
                    unknown_list.append('-'+temp)
                elif model[temp] == 1:
                    continue
                elif model[temp] == -1:
                    overall_result = 1
            else:
                # Positive clause
                if model[temp] == 0:
                    if unknow==0:
                        first_unknown_value = temp
                    unknow += 1
                    unknown_list.append(temp)
                elif model[temp] == 1:
                    overall_result = 1
                elif model[temp] == -1:
                    continue
        if unknow > 0 and overall_result == -1:
            # There are still unknow, cannot conclude if overall result is False
            overall_result = 0
        return overall_result, first_unknown_value, unknown_list

        
        
    def DPLL(self, model={}, unit_clause_heuristic=False):
        # Make a deep copy of the model to avoid altering the original dictionary
        self.call_count += 1
        unknown_count = 0
        # write function for if some clauses are false then false and if every clauses are true -> then true 
        next_variable = ''
        min_unknow_length = self.model_size + 1
        for clause in self.clauses:
            clause_result, unknow_value, unknown_list = self.check_clause(clause,model)
            if unit_clause_heuristic:
                if clause_result == -1:
                    return False
                len_unknown_list = len(unknown_list)
                if clause_result==0 and len_unknown_list > 0 and min_unknow_length > len_unknown_list:
                    min_unknow_length = len_unknown_list
                    next_variable = unknown_list[0]
                if clause_result==0:
                    unknown_count+=1
            else:
                if clause_result == -1:
                    return False
                if clause_result==0:
                    if unknown_count==0:
                        next_variable=unknow_value
                    unknown_count+=1
        if (unknown_count == 0 and next_variable==''):
            self.result_model = model.copy()
            return True
        if unit_clause_heuristic:
            if next_variable[0]=='-':
                next_variable = next_variable[1:]
                model_false = model.copy()
                model_false[next_variable] = -1
                self.print_value(model_false, next_variable, -1)
                return self.DPLL(model_false, unit_clause_heuristic)
            else:
                model_true = model.copy()
                model_true[next_variable] = 1
                self.print_value(model_true, next_variable, 1)
                return self.DPLL(model_true, unit_clause_heuristic)
        else:
            #assigning it first to T and then F (a choice-point)
            model_true = model.copy()
            model_true[next_variable] = 1
            self.print_value(model_true, next_variable, 1)
            temp = self.DPLL(model_true, unit_clause_heuristic)
            if temp:
                return True
            model_false = model.copy()
            model_false[next_variable] = -1
            self.print_value(model_false, next_variable, -1)
            return self.DPLL(model_false, unit_clause_heuristic) 
    

    def print_value(self, model, variable, value):
        print("model: ", model)
        print("Trying ", variable, '=', 'T' if value ==1 else 'F')

    def print_count(self, model, status):
        final_ans = []
        for val in model:
            print (val,':',model[val])
            if model[val] == 1:
                final_ans.append(val)
        if final_ans != []:
            print('just the True proposition:')
            print(' '.join(str(x) for x in final_ans))
            print('total DPLL calls:',self.call_count)
        else:
            print('This problem is unsatisfiable')
        if status != '':
            print(status,'=True')


if __name__ == "__main__":
    status = ''
    input = input().split()
    file = input[1]
    facts = input[2:]
    if facts != [] and facts[-1] == '+UCH':
        status = facts[-1]
        facts = facts[:-1]
    print('this is the facts',facts)
    test = DPLL_solver()
    test.parser(file, facts)
    if status != '':
        test.DPLL(test.models, True)
    else:
        test.DPLL(test.models, False)
    test.print_count(test.result_model, status)
    