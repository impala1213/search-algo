import random
import math

from setup import Setup


class Problem(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._solution = []
        self._value = 0
        self._numEval = 0

        self._pFileName = ''
        self._bestSolution = []
        self._bestMinimum = 0
        self._avgMinimum = 0
        self._avgNumEval = 0
        self._sumOfNumEval = 0
        self._avgWhen = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pFileName = parameters['pFileName']
    
    def getSolution(self):
        return self._solution

    def getValue(self):
        return self._value

    def getNumEval(self):
        return self._numEval

    def resetNumEval(self):
        self._numEval = 0

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

    def storeExpResult(self, results):
        self._bestSolution = results[0]
        self._bestMinimum = results[1]
        self._avgMinimum = results[2]
        self._avgNumEval = results[3]
        self._sumOfNumEval = results[4]
        self._avgWhen = results[5]

    def report(self):
        aType = self._aType
        if 1 <= aType <= 4:  # No need to take average for SA, GA
            print("Average number of evaluations: {0:,}" \
                  .format(round(self._avgNumEval)))
        if 5 <= aType <= 6:
            print("Average iteration of finding the best: {0:,}"
                  .format(self._avgWhen))
        print()
 
    def reportNumEvals(self):
        if 1 <= self._aType <= 4:
            print()
            print("Total number of evaluations: {0:,}"
                  .format(self._sumOfNumEval))


class Numeric(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []     # domain as a list
    
    def setVariables(self, parameters):
        fileName = input("Enter the file name of a function: ")
        problem = open(fileName, 'r')
        pro_line = problem.readlines()  # seperate with lines
        self._expression = pro_line[0].strip()  # set problem
        i = 1
        varNames = []
        low = []
        up = []
        while i < len(pro_line):
            splitfile = pro_line[i].split(',')  # start with first line
            varNames.append(splitfile[0])
            low.append(splitfile[1])
            up.append(splitfile[2].strip())

            i += 1
        self._domain = [varNames, low, up]

    def randomInit(self): # Return a random initial point as a list
        varNames = self._domain[0]  # domain: [varNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        init = [random.uniform(int(low[i]), int(up[i])) for i in
                range(len(varNames))]  # make a list with low-high(random)
        return init  # list of values
        #self._numEval += 1  # counting while 100
        expr = self._expression  # expression
        varNames = self._domain[0]  # domain: [varNames, low, up]
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])  # current = randominit -> low~high (random)
            exec(assignment)  # x1 = random
        return eval(expr)

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):  # 변수 수만큼 반복
            for d in [-self._delta, self._delta]:  # delta = 0.01
                neighbor = self.mutate(current, i, d)  # -0.1 +0.1인 neighbor 생성
                if self.isLegal(neighbor):  # neighbor가 low-high 사이라면 neighbor 리스트에 추가
                    neighbors.append(neighbor)
        return neighbors

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        mutant = current[:]
        l = self._domain[1][i]
        h = self._domain[2][i]
        if int(l) <= (int(mutant[i])+d) <= int(h):
            mutant[i] += d
        return mutant

    def randomMutant(self, current):
        i = random.randint(0, len(current) - 1)  # current = randominit
        d = random.choice([-self._delta, self._delta])
        return self.mutate(current, i, d)

    def takeStep(self, x, v): # Take gradient and make update if legal
        newX = [x[i] + self._alpha * v[i] for i in range(len(x))]
        if self.isLegal(xCopy):  # Check if 'xCopy' is within the domain
            return xCopy
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

    def isLegal(self, x):   # Check if 'x' is within the domain
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
        avgMinimum = round(self._avgMinimum, 3)
        print()
        print("Average objective value: {0:,}".format(avgMinimum))
        Problem.report(self)
        print("Best solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Best value: {0:,.3f}".format(self._bestMinimum))
        self.reportNumEvals()

    def coordinate(self):
        c = [round(value, 3) for value in self._bestSolution]
        return tuple(c)  # Convert the list to a tuple


class Tsp(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []       # A list of tuples
        self._distanceTable = []

    def setVariables(self, parameters):
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
        
    def calcDistanceTable(self):
        self.table = [[0] * self.numCities for _ in range(self.numCities)]
        for i in range(self.numCities):
            for j in range(self.numCities):
                if i != j:
                    self.table[i][j] = math.sqrt(
                        (self.locations[i][0] - self.locations[j][0]) ** 2 + (
                                    self.locations[i][1] - self.locations[j][1]) ** 2)
        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self.numCities
        self.init = list(range(n))
        random.shuffle(self.init)
        return init

    def evaluate(self, current):
       # self._numevals +=1
        tourcost = 0
        for i in range(-1, self.numCities-1):
            tourcost += self.table[current[i]][current[i+1]]
        return tourCost

    def mutants(self, current): # Inversion only
        neighbors = []
        for i in range(self.numCities):
            for j in range(i + 1, self.numCities):
                neighbors.append(self.inversion(current, i, j))
        return neighbors

    def inversion(self, current, i, j):  ## Perform inversion
        mutant = current[:]
        while i < j :
            mutant[i], mutant[j] = mutant[j], mutant[i]
            i += 1
            j += 1
        return mutant

    def randomMutant(self, current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self.numCities)] for _ in range(2))
            if i < j:
                mutant = self.inversion(current, i, j)
                break
        return mutant

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def report(self):
        avgMinimum = round(self._avgMinimum)
        print()
        print("Average tour cost: {0:,}".format(avgMinimum))
        Problem.report(self)
        print("Best tour found:")
        self.tenPerRow()  # Print 10 cities per row
        print("Best tour cost: {0:,}" \
              .format(round(self._bestMinimum)))
        self.reportNumEvals()

    def tenPerRow(self):
        solution = self._bestSolution
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

