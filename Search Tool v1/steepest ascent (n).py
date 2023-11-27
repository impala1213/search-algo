import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    fileName = input("Enter the file name of a function: ")
    problem = open(fileName, 'r')
    pro_line = problem.readlines()
    expression = pro_line[0].strip()
    i = 1
    varnames = []
    low = []
    up = []
    while i < len(pro_line):
        splitfile = pro_line[i].split(',')
        varnames.append(splitfile[0])
        low.append(splitfile[1])
        up.append(splitfile[2].strip())
        i+=1
    domain = [varnames, low, up]
    return expression, domain


def steepestAscent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        neighbors = mutants(current, p)
        successor, valueS = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def randomInit(p): ###
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    low = p[1][1]
    up = p[1][2]
    init = [random.uniform(int(low[i]), int(up[i])) for i in range(len(varNames))]
    return init

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def mutants(current, p): # Apply inversion
    neighbors = []
    for i in range(len(current)):
        neighbors.append(mutate(current, i, DELTA, p))  # Move up
        neighbors.append(mutate(current, i, -DELTA, p)) # Move down
    return neighbors


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = domain[1][i]     # Lower bound of i-th
    u = domain[2][i]     # Upper bound of i-th
    if int(l) <= float((curCopy[i] + d)) <= int(u):
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(best, p)
    for neighbor in neighbors[1:]:
        tempValue = evaluate(neighbor, p)
        if tempValue < bestValue:
            best = neighbor
            bestValue = tempValue
    return best, bestValue
def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple


main()
