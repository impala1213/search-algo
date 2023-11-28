import random
import math
from setup import Setup


class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0   # Type of problem
        self._numExp = 0  # Total number of experiments

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:
            print("Mutation step size:", self._delta)


class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitStuck = 0  # Max evaluations allowed for no improvement
        self._numRestart = 0         # Number of restart

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2 <= self._aType <= 3:  # First-Choice, Stochastic
            print("Max evaluations with no improvement: {0:,} iterations"
                  .format(self._limitStuck))

    def run(self):
        pass

    def randomRestart(self, p):          # 'alg' is the chosen hill climber
        ??
        p.storeResult(bestSolution, bestMinimum)


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        ??
        p.storeResult(current, valueC)

    def bestOf(self, neighbors, p):
        ??
        return best, bestValue


class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        ??
        p.storeResult(current, valueC)


class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        ??
        p.storeResult(current, valueC)

    def stochasticBest(self, neighbors, p):
        ??
        return nextSolution, nextValue


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        HillClimbing.displaySetting(self)
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
        ??
        p.storeResult(currentP, valueC)


class MetaHeuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitEval = 0     # Total # evaluations until temination
        self._whenBestFound = 0 # This is actually a result of experiment

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self._limitEval))

    def run(self):
        pass


class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._numSample = 100  # Number of samples used to determine 
                               #  initial temperature
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)

    def run(self, p):
        ??
        p.storeResult(best, valueBest)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        ??
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))

