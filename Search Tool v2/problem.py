import random
import math

"""
[Problem] class is complete as it is.
Do not need to modify!!!
"""
class Problem:
    def __init__(self):
        self._solution = []
        self._value = 0
        self._numEval = 0

    def setVariables(self):
        pass
    
    def randomInit(self):
        pass

    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self, current):
        pass

    def describe(self):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value

    def report(self):
        print()

        print("Total number of evaluations: {0:,}".format(self._numEval))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []     # domain as a list
        self._delta = 0.01    # Step size for axis-parallel mutation

        self._alpha = 0.01    # Update rate for gradient descent
        self._dx = 10 ** (-4) # Increment for calculating derivative
    
    def setVariables(self):
        fileName = input("Enter the file name of a function: ")
        problem = open(fileName, 'r')
        pro_line = problem.readlines()
        self._expression = pro_line[0].strip()
        i = 1
        varnames = []
        low = []
        up = []
        while i < len(pro_line):
            splitfile = pro_line[i].split(',')
            varnames.append(splitfile[0])
            low.append(splitfile[1])
            up.append(splitfile[2].strip())

            i += 1
        self._domain = [varnames, low, up]
        return self._expression, self._domain

    def getDelta(self):
        return self._delta

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._dx

    def randomInit(self): # Return a random initial point as a list
        varNames = self._domain[0] # p[1] is domain: [varNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        init = [random.uniform(int(low[i]), int(up[i])) for i in range(len(varNames))]
        return init

    def evaluate(self, current):
        self._numEval += 1
        expr = self._expression  # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)

        return eval(expr)

    def mutants(self, current):
        neighbors = []  # list of all feasible neighboring solutions
        for i in range(len(current)):
            for d in [-self._delta, self._delta]:
                neighbor = self.mutate(current, i, d)
                if self.isLegal(neighbor):
                    neighbors.append(neighbor)
        return neighbors

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        l = self._domain[1][i]  # Lower bound of i-th
        u = self._domain[2][i]  # Upper bound of i-th
        if int(l) <= (int(curCopy[i]) + d) <= int(u):
            curCopy[i] += d
        return curCopy

    def randomMutant(self, current):
        i = random.randint(0, len(current) - 1)
        d = random.choice([-self._delta, self._delta])
        return self.mutate(current, i, d,)

    def takeStep(self, x, v): # Take gradient and make update if legal
        newX = [x[i] + self._alpha * v[i] for i in range(len(x))]
        if self.isLegal(newX):
            return newX
        else:
            return x

    def gradient(self, x, v): # 'x' is a vector (list of valules)
        grad = []  # Calculate partial derivatives and combine them
        for i in range(len(x)):
            xCopy = x[:]
            xCopy[i] += self._dx
            deriv = (self.evaluate(xCopy) - self.evaluate(x)) / self._dx
            grad.append(deriv)
        return grad

    def isLegal(self, x):  # Check if 'x' is within the domain
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(x)):
            if not (int(low[i]) <= x[i] <= int(up[i])):
                return False
        return True

    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)
        print("Search space:")
        varNames = self._domain[0] # domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i]))

    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value))
        Problem.report(self)

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple



class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self.numCities = 0
        self.locations = []       # A list of tuples
        self.table = []

    def setVariables(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        self.numCities = int(infile.readline())
        self.locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self.locations.append(eval(line))  # Make a tuple and append
            line = infile.readline()
        infile.close()
        return self.numCities, self.locations
        
    def calcDistanceTable(self):
        self.table = [[0] * self.numCities for _ in range(self.numCities)]
        for i in range(self.numCities):
            for j in range(self.numCities):
                if i != j:
                    self.table[i][j] = math.sqrt(
                        (self.locations[i][0] - self.locations[j][0]) ** 2 + (self.locations[i][1] - self.locations[j][1]) ** 2)


        return self.table  # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self.numCities
        self.init = list(range(n))
        random.shuffle(self.init)
        return self.init

    def evaluate(self, current):
        self._numEval += 1
        cost = 0
        for i in range(-1, self.numCities - 1):
            cost += self.table[current[i]][current[i + 1]]
        return cost

    def mutants(self, current): # Inversion only
        neighbors = []
        for i in range(self.numCities):
            for j in range(i+1, self.numCities):
                neighbors.append(self.inversion(current, i, j))
        return neighbors
    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def randomMutant(self, current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self.numCities)
                           for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def describe(self):
        print()
        n = self.numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self.locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()  # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        Problem.report(self)

    def tenPerRow(self):
        solution = self._solution
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

