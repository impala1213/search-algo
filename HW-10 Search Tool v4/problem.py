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
        ??
        self._domain = [varNames, low, up]

    def randomInit(self): # Return a random initial point as a list
        ??
        return init  # list of values

    def evaluate(self, current):
        ??
        return eval(expr)

    def mutants(self, current):
        ??
        return neighbors

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        ??
        return mutant

    def randomMutant(self, current):
        ??
        return self.mutate(current, i, d)

    def takeStep(self, x, v): # Take gradient and make update if legal
        ??
        if self.isLegal(xCopy):  # Check if 'xCopy' is within the domain
            return xCopy
        else:
            return x

    def gradient(self, x, v): # 'x' is a vector (list of valules)
        ??
        return grad

    def isLegal(self, x):   # Check if 'x' is within the domain
        ??
        return True OR False

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
        ??
        
    def calcDistanceTable(self):
        ??
        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        ??
        return init

    def evaluate(self, current):
        ??
        return tourCost

    def mutants(self, current): # Inversion only
        ??
        return neighbors

    def inversion(self, current, i, j):  ## Perform inversion
        ??
        return mutant

    def randomMutant(self, current): # Inversion only
        ??
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

